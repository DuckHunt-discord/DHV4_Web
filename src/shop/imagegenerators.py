from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill


class ThumbnailList(ImageSpec):
    processors = [ResizeToFill(400, 400)]
    format = 'JPEG'
    options = {'quality': 60}


class ThumbnailMini(ImageSpec):
    processors = [ResizeToFill(200, 200)]
    format = 'JPEG'
    options = {'quality': 85}


register.generator('shop:thumbnail_list', ThumbnailList)
register.generator('shop:thumbnail_mini', ThumbnailMini)
