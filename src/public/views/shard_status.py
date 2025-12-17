from django.conf import settings
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .utils import MINUTE, get_from_api


@cache_page(5 * MINUTE)
def shard_status(request, shard_id):
    status_url = settings.DH_API_URL + "/status"
    api_status = get_from_api(status_url)

    for shard in api_status["shards_status"]:
        if shard["shard_id"] == shard_id:
            break
    else:
        shard = None

    return render(request, "public/shard_status.jinja2", {"status": api_status, "shard": shard})
