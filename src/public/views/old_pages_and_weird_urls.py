from django.http import HttpResponsePermanentRedirect
from django.urls import reverse


def old_pages_and_weird_urls(request):
    path = request.get_full_path()

    if path.startswith('/fr/parametres'):
        return HttpResponsePermanentRedirect(reverse("bot_commands", kwargs={"command": "settings"}))

    return HttpResponsePermanentRedirect('/')
