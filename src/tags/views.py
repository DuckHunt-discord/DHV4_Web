from django.http import Http404
from django.shortcuts import render

# Create your views here.
from tags.models import get_tag, Tag


def index(request):
    tags = Tag.objects.all()
    return render(request, 'tags/index.jinja2', {'tags': tags})


def tag(request, tag_name):
    requested_tag = get_tag(tag_name)

    if not requested_tag:
        raise Http404("Tag not found.")

    return render(request, 'tags/tag.jinja2', {'tag': requested_tag, 'requested_name': tag_name})
