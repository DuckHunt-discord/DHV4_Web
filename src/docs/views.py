from django.http import Http404, FileResponse
from django.shortcuts import render
import pathlib
import markdown
from django.urls import reverse
from django.utils.safestring import mark_safe

from docs.md_processors.bootstrap import BootstrapExtension, get_fake_title_extension
from docs.md_processors.hints import HintExtension
from docs.md_processors.remove_md_links_extension import get_extension
from django.shortcuts import redirect

MARKDOWN_FILES = pathlib.Path(__file__).parent.absolute() / "markdown_files/"


def parse_summary(request):
    summary_file = MARKDOWN_FILES / "SUMMARY.md"
    absolute_path = request.build_absolute_uri(reverse('docs:index'))

    if "localhost" not in absolute_path and "127.0.0.1" not in absolute_path:
        absolute_path = absolute_path.replace('http://', 'https://')

    with open(summary_file, "r") as f:
        parsed_summary = markdown.markdown(f.read(),
                                           extensions=['tables',
                                                       'fenced_code',
                                                       HintExtension(),
                                                       BootstrapExtension(),
                                                       get_fake_title_extension(level_from=0)(),
                                                       get_extension(absolute_path=absolute_path)()],
                                           )
    parsed_summary = mark_safe(parsed_summary)
    return parsed_summary


# Create your views here.
def summary(request):
    summary_file = MARKDOWN_FILES / "SUMMARY.md"

    gh_file = "https://github.com/DuckHunt-discord/duckhunt.me-docs/blob/master/SUMMARY.md"

    return render(request, "docs/summary.jinja2", {"file": summary_file,
                                                   "parsed_content": parse_summary(request),
                                                   "gh_file": gh_file, })


def display_page(request, path, ctx=None):
    splitted_path = path.strip('/').split('/')
    category = '/'.join(splitted_path[:-1])
    page = splitted_path[-1]
    if ctx is None:
        ctx = {}

    if category:
        file = f"{category}/{page}.md"
    else:
        file = f"{page}.md"

    gh_file = "https://github.com/DuckHunt-discord/duckhunt.me-docs/blob/master/" + file

    file = MARKDOWN_FILES / file

    if not file.exists():
        raise Http404(f"This page {path} does not exist in the documentation. Can you create it ?")

    with open(file, "r") as f:
        parsed = markdown.markdown(f.read(),
                                   extensions=['tables',
                                               'fenced_code',
                                               HintExtension(),
                                               BootstrapExtension(),
                                               get_fake_title_extension(level_from=3)(),
                                               get_extension()()]
                                   )
        parsed = mark_safe(parsed)

    return render(request, "docs/index.jinja2", {"page": page, "category": category, "file": file,
                                                 "parsed_content": parsed, "parsed_summary": parse_summary(request),
                                                 "gh_file": gh_file, **ctx})


def assets(request, file):
    return FileResponse(open(MARKDOWN_FILES / '.gitbook/assets' / file, "rb"))


def index_redirect(request):
    return redirect(reverse('docs:index'), permanent=True)