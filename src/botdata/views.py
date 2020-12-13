from django.db.models import Prefetch, Q, Count
from django.shortcuts import render
from .models import DiscordGuild, DiscordChannel


# Create your views here.

def guilds(request):
    enabled_channels_qs = DiscordChannel.objects.filter(enabled=True)
    guilds_list = DiscordGuild.objects \
        .annotate(
            enabled_channels_count=Count('channels', filter=Q(channels__enabled=True))
        ) \
        .filter(enabled_channels_count__gt=0) \
        .prefetch_related(Prefetch("channels", queryset=enabled_channels_qs.annotate(
            player_count=Count("players")
        )))\
        .order_by('vip', 'pk')

    return render(request, "botdata/guilds.jinja2", {"guilds": guilds_list})


def guild(request, pk: int):
    return render(request, "botdata/guilds.jinja2")


def channel(request, pk: int):
    return render(request, "botdata/guilds.jinja2")


def player(request, channel_pk: int, user_pk: int):
    return render(request, "botdata/guilds.jinja2")
