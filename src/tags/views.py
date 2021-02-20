from django.shortcuts import render

# Create your views here.
from tags.models import get_tag


def index(request):
    return render(request, 'tags/index.jinja2')


def tag(request, tag_name):
    return render(request, 'tags/tag.jinja2', {'tag': get_tag(tag_name), 'requested_name': tag_name})