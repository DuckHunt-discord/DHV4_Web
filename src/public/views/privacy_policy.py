from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .utils import DAY


@cache_page(3 * DAY)
def privacy_policy(request):
    return render(request, "public/privacy_policy.jinja2", {})
