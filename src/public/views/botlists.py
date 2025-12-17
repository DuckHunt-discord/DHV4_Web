from django.shortcuts import render

from botdata.models import BotList


def botlists(request):
    bls = BotList.objects.exclude(embed_code='')
    return render(request, "public/botlists.jinja2", {"botlists": bls})
