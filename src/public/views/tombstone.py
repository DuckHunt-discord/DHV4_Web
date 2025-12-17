import io
import logging
import unicodedata

from django.contrib.staticfiles import finders
from django.http import Http404, HttpResponse
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from fontTools.ttLib import TTFont  # type: ignore

TOMBSTONE_TEXT_BOX = (245, 184, 753, 689)
DEFAULT_TOMBSTONE_REASON = "Forgot to Duck"
MAX_FONT_SIZE = 200
MIN_FONT_SIZE = 8
RIP_SCALE = 1.2
REASON_SCALE = 0.9
logger = logging.getLogger(__name__)
_FONT_CACHE = {}
_TTFONT_CACHE = {}
_EMOJI_FONT_CACHE = {}
_FONT_CANDIDATES = None
_CHAR_FONT_CACHE = {}
_CHAR_METRICS_CACHE = {}


def _find_static(path: str):
    resolved = finders.find(path)
    if not resolved:
        logger.warning("Static asset not found: %s", path)
    return resolved


def _font_candidates():
    # Cache resolved candidates to avoid repeated filesystem lookups per request.
    global _FONT_CANDIDATES
    if _FONT_CANDIDATES is None:
        font_dir = "public/font"
        specific = [
            f"{font_dir}/Cinzel-Bold.ttf",
            f"{font_dir}/Cinzel-Regular.ttf",
            f"{font_dir}/NotoSerif-VariableFont_wdth,wght.ttf",
            f"{font_dir}/NotoEmoji-VariableFont_wght.ttf",
            f"{font_dir}/NotoEmoji-Regular.ttf",
        ]
        resolved_specific = [p for rel in specific if (p := _find_static(rel))]
        _FONT_CANDIDATES = [
            *resolved_specific,
            "DejaVuSerif-Bold.ttf",
            "DejaVuSerif.ttf",
            "DejaVuSans-Bold.ttf",
            "DejaVuSans.ttf",
        ]
    return _FONT_CANDIDATES


def _fonts_for_size(size: int):
    fonts = []
    for candidate in _font_candidates():
        cache_key = (candidate, size)
        if cache_key in _FONT_CACHE:
            fonts.append(_FONT_CACHE[cache_key])
            continue
        if hasattr(candidate, "exists") and not candidate.exists():
            continue
        try:
            font = ImageFont.truetype(str(candidate), size=size)
            _FONT_CACHE[cache_key] = font
            fonts.append(font)
            logger.debug("Loaded tombstone font %s at size %s", candidate, size)
        except OSError:
            continue
    if not fonts:
        logger.warning("Falling back to default font for tombstone (size=%s)", size)
        fonts.append(ImageFont.load_default())

    # Pre-populate emoji font cache for this font set
    fonts_key = tuple(id(f) for f in fonts)
    if fonts_key not in _EMOJI_FONT_CACHE:
        _EMOJI_FONT_CACHE[fonts_key] = (
            [f for f in fonts if "emoji" in str(getattr(f, "path", getattr(f, "font", ""))).lower()],
            [f for f in fonts if "emoji" not in str(getattr(f, "path", getattr(f, "font", ""))).lower()]
        )

    return fonts


def _load_tombstone_font(size: int):
    """Returns the first available font for the given size."""
    return _fonts_for_size(size)[0]


def _ttfont_for_imagefont(font):
    path = getattr(font, "path", getattr(font, "font", None))
    if not path:
        return None
    cached = _TTFONT_CACHE.get(path)
    if cached is not None:
        return cached
    try:
        tt = TTFont(path)
        _TTFONT_CACHE[path] = tt
        return tt
    except Exception as exc:
        logger.debug("Could not load TTFont for %s: %s", path, exc)
        _TTFONT_CACHE[path] = None
        return None


def _is_emoji_char(char: str) -> bool:
    cp = ord(char)
    if cp >= 0x1F000:
        return True
    if 0x2600 <= cp <= 0x27BF:
        return True
    if 0x1F1E6 <= cp <= 0x1F1FF:
        return True
    if unicodedata.category(char) == "So":
        return True
    return False


def _select_font_for_char(char: str, fonts, measure_draw: ImageDraw.ImageDraw):
    fonts_key = tuple(id(f) for f in fonts)
    font_cache = _CHAR_FONT_CACHE.setdefault(fonts_key, {})
    if char in font_cache:
        return font_cache[char]

    if char.strip() == "":
        font_cache[char] = fonts[0]
        return fonts[0]

    # Emoji font cache is pre-populated in _fonts_for_size
    emoji_fonts, non_emoji_fonts = _EMOJI_FONT_CACHE[fonts_key]
    font_order = emoji_fonts + non_emoji_fonts if _is_emoji_char(char) else fonts

    for font in font_order:
        ttfont = _ttfont_for_imagefont(font)
        if ttfont:
            try:
                if any(ord(char) in table.cmap for table in ttfont["cmap"].tables):
                    font_cache[char] = font
                    return font
            except Exception as exc:
                logger.debug("TTFont cmap check failed for %s: %s", font, exc)

        bbox = measure_draw.textbbox((0, 0), char, font=font)
        if bbox and (bbox[2] - bbox[0] > 0 or bbox[3] - bbox[1] > 0):
            font_cache[char] = font
            return font

    fallback = fonts[-1]
    font_cache[char] = fallback
    return fallback


def _font_metrics_for_char(char: str, fonts, measure_draw: ImageDraw.ImageDraw):
    fonts_key = tuple(id(f) for f in fonts)
    metrics_cache = _CHAR_METRICS_CACHE.setdefault(fonts_key, {})
    if char in metrics_cache:
        return metrics_cache[char]

    font = _select_font_for_char(char, fonts, measure_draw)
    bbox = measure_draw.textbbox((0, 0), char, font=font)
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]
    metrics_cache[char] = (font, char_width, char_height)
    return metrics_cache[char]


def _measure_text(text: str, fonts, measure_draw: ImageDraw.ImageDraw):
    width = 0
    max_height = 0
    for char in text:
        _, char_width, char_height = _font_metrics_for_char(char, fonts, measure_draw)
        width += char_width
        max_height = max(max_height, char_height)
    return width, max_height


def _choose_layout(name: str, reason: str, text_width_limit: int, text_height_limit: int, measure_draw: ImageDraw.ImageDraw):
    max_size = min(text_height_limit, MAX_FONT_SIZE)
    low, high = MIN_FONT_SIZE, max_size
    best = None

    while low <= high:
        size = (low + high) // 2
        font = _load_tombstone_font(size)
        layout = _layout_for_font(font, name, reason, text_width_limit, measure_draw)
        if not layout:
            high = size - 1
            continue

        lines, block_width, block_height, spacing, reason_gap, reason_start_index = layout
        fits = block_width <= text_width_limit and block_height <= text_height_limit
        if fits:
            best = (font, lines, block_width, block_height, spacing, reason_gap, reason_start_index)
            low = size + 1  # try to grow
        else:
            high = size - 1  # shrink

    if best:
        return best

    fallback_font = _load_tombstone_font(MIN_FONT_SIZE)
    layout = _layout_for_font(fallback_font, name, reason, text_width_limit, measure_draw)
    if not layout:
        layout = ([], 0, 0, 0, 2, 0)
    lines, block_width, block_height, spacing, reason_gap, reason_start_index = layout
    return fallback_font, lines, block_width, block_height, spacing, reason_gap, reason_start_index


def _layout_for_font(font: ImageFont.FreeTypeFont, name: str, reason: str, text_width_limit: int, measure_draw: ImageDraw.ImageDraw):
    size_for_spacing = getattr(font, "size", MIN_FONT_SIZE)
    line_spacing = max(2, int(size_for_spacing * 0.18))
    reason_gap = max(line_spacing, int(size_for_spacing * 0.4))

    base_fonts = _fonts_for_size(size_for_spacing)
    rip_fonts = _fonts_for_size(max(int(size_for_spacing * RIP_SCALE), size_for_spacing + 1))
    reason_fonts = _fonts_for_size(max(MIN_FONT_SIZE, int(size_for_spacing * REASON_SCALE)))
    rip_lines = ["R.I.P."]

    # Share cache across wrapping and measuring for this layout
    measure_cache = {}
    name_lines = _wrap_text(name, base_fonts, text_width_limit, measure_draw, measure_cache)
    if len(name_lines) > 1:
        return None

    reason_lines = _wrap_text(reason, reason_fonts, text_width_limit, measure_draw, measure_cache)
    if len(reason_lines) > 2:
        return None

    # Build lines with their measurements
    lines_with_measurements = []
    for line_text, line_font in [(l, rip_fonts) for l in rip_lines] + \
                                 [(l, base_fonts) for l in name_lines] + \
                                 [(l, reason_fonts) for l in reason_lines]:
        cache_key = (line_text, tuple(id(f) for f in line_font))
        if cache_key not in measure_cache:
            measure_cache[cache_key] = _measure_text(line_text, line_font, measure_draw)
        width, height = measure_cache[cache_key]
        is_reason = line_text in reason_lines
        lines_with_measurements.append((line_text, line_font, is_reason, width, height))

    widths = [w for _, _, _, w, _ in lines_with_measurements]
    heights = [h for _, _, _, _, h in lines_with_measurements]

    base_spacing = line_spacing * (len(lines_with_measurements) - 1 if len(lines_with_measurements) > 1 else 0)
    extra_reason_spacing = reason_gap if reason_lines else 0
    total_height = sum(heights) + base_spacing + extra_reason_spacing
    max_line_width = max(widths) if widths else 0
    reason_start_index = len(rip_lines) + len(name_lines)
    return lines_with_measurements, max_line_width, total_height, line_spacing, reason_gap, reason_start_index


def _wrap_text(text: str, fonts, max_width: int, measure_draw: ImageDraw.ImageDraw, measure_cache=None):
    clean_text = text.strip() or ""
    if measure_cache is None:
        measure_cache = {}

    fonts_key = tuple(id(f) for f in fonts)

    def text_width(content: str) -> int:
        cache_key = (content, fonts_key)
        if cache_key not in measure_cache:
            measure_cache[cache_key] = _measure_text(content, fonts, measure_draw)
        return measure_cache[cache_key][0]

    def split_long_word(word: str):
        parts = []
        current = ""
        for char in word:
            candidate = current + char
            if text_width(candidate) <= max_width or not current:
                current = candidate
            else:
                parts.append(current)
                current = char
        if current:
            parts.append(current)
        return parts or [word]

    words = [w for w in clean_text.split(" ") if w]
    if not words:
        return [clean_text] if clean_text else [""]

    lines = []
    current_line = ""

    for word in words:
        candidate = word if not current_line else f"{current_line} {word}"
        if text_width(candidate) <= max_width:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
                current_line = ""
            split_parts = split_long_word(word)
            lines.extend(split_parts[:-1])
            current_line = split_parts[-1]

    if current_line:
        lines.append(current_line)

    return lines or [clean_text]


def tombstone(request):
    name = (request.GET.get("name") or "Unknown hunter").strip()
    reason = (request.GET.get("reason") or DEFAULT_TOMBSTONE_REASON).strip() or DEFAULT_TOMBSTONE_REASON

    base_image_path = _find_static("public/tombstone.jpg") or _find_static("tombstone.jpg")
    if not base_image_path:
        logger.error("Tombstone base image not found in staticfiles.")
        raise Http404("Tombstone template not found.")

    with Image.open(base_image_path) as img:
        base_image = img.convert("RGBA")

    x0, y0, x1, y1 = TOMBSTONE_TEXT_BOX
    text_width_limit = x1 - x0
    text_height_limit = y1 - y0

    measure_draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    font, lines, block_width, block_height, spacing, reason_gap, reason_start_index = _choose_layout(
        name, reason, text_width_limit, text_height_limit, measure_draw
    )

    if block_height > text_height_limit and len(lines) > 1:
        old_spacing = spacing
        spacing = max(1, int(spacing * text_height_limit / block_height))
        block_height = block_height - (old_spacing - spacing) * (len(lines) - 1)

    text_mask = Image.new("L", base_image.size, 0)
    mask_draw = ImageDraw.Draw(text_mask)

    if block_height > text_height_limit:
        start_y = y0
    else:
        start_y = y0 + (text_height_limit - block_height) / 2

    logger.debug(
        "Rendering tombstone for name=%s reason=%s font=%s size=%s lines=%s block=%sx%s",
        name,
        reason,
        getattr(font, "path", getattr(font, "font", None)),
        getattr(font, "size", None),
        len(lines),
        block_width,
        block_height,
    )

    for idx, (line, line_fonts, is_reason, width, height) in enumerate(lines):
        if is_reason and idx == reason_start_index:
            start_y += reason_gap

        start_x = x0 + (text_width_limit - width) / 2

        cursor_x = start_x
        for char in line:
            font_for_char = _select_font_for_char(char, line_fonts, measure_draw)
            bbox = measure_draw.textbbox((0, 0), char, font=font_for_char)
            char_width = bbox[2] - bbox[0]
            mask_draw.text((cursor_x, start_y), char, font=font_for_char, fill=255)
            cursor_x += char_width

        start_y += height + spacing

    # Darken existing stone texture inside the glyphs instead of flat color fills.
    blur_radius = 1.1
    softened = text_mask.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    darker_stone = ImageEnhance.Brightness(base_image).enhance(0.4)
    carved_base = Image.composite(darker_stone, base_image, softened)

    inner_shadow = ImageChops.offset(softened, -1, -1)
    highlight_mask = ImageChops.offset(softened, 1, 1)

    shadow_layer = Image.new("RGBA", base_image.size, (5, 5, 5, 180))
    shadow_layer.putalpha(inner_shadow)

    highlight_layer = Image.new("RGBA", base_image.size, (180, 180, 180, 20))
    highlight_layer.putalpha(highlight_mask)

    carved = Image.alpha_composite(carved_base, shadow_layer)
    carved = Image.alpha_composite(carved, highlight_layer)

    # Apply a multiply pass only where text exists, keeping the rest of the stone unchanged.
    multiply_target = ImageEnhance.Brightness(base_image).enhance(0.8)
    multiplied_carved = ImageChops.multiply(carved, multiply_target)
    carved = Image.composite(multiplied_carved, carved, softened)

    composed = carved.convert("RGB")

    buffer = io.BytesIO()
    composed.save(buffer, format="JPEG", quality=95)
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/jpeg")
