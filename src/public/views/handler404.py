from django.http import HttpResponse
from django.template import loader


def handler404(request, exception=None):
    content = loader.render_to_string('public/404.jinja2', None, request)
    return HttpResponse(content, None, 404)
