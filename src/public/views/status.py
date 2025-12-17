from django.conf import settings
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .utils import MINUTE, get_from_api


@cache_page(2 * MINUTE)
def status(request):
    status_url = settings.DH_API_URL + "/status"
    api_status = get_from_api(status_url)

    return render(request, "public/status.jinja2", {"status": api_status})
