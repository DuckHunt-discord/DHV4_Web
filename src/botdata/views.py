import random

from django.db.models import Prefetch, Q, Count
from django.shortcuts import render, get_object_or_404
from .models import DiscordGuild, DiscordChannel, DiscordUser, Player

# Create your views here.

def guilds(request):
    enabled_channels_qs = DiscordChannel.objects.filter(enabled=True)
    guilds_list = DiscordGuild.objects \
        .annotate(enabled_channels_count=Count('channels', filter=Q(channels__enabled=True))) \
        .filter(enabled_channels_count__gt=0) \
        .prefetch_related(Prefetch("channels", queryset=enabled_channels_qs.annotate(player_count=Count("players")))) \
        .order_by('vip', 'pk')

    return render(request, "botdata/guilds.jinja2", {"guilds": guilds_list})


def guild(request, pk: int):
    current_guild = get_object_or_404(DiscordGuild, pk=pk)
    return render(request, "botdata/guild.jinja2", {"guild": current_guild})


def channel(request, pk: int):
    current_channel = get_object_or_404(DiscordChannel, pk=pk)
    current_players = Player.objects.filter(channel=current_channel).select_related("member__user").order_by(
        '-experience')
    return render(request, "botdata/channel.jinja2", {"channel": current_channel, "players": current_players})


def channel_settings(request, pk: int):
    current_channel = get_object_or_404(DiscordChannel, pk=pk)
    return render(request, "botdata/channel_settings.jinja2", {"channel": current_channel})


def player(request, channel_pk: int, user_pk: int):
    from .achievements import achievements
    # TODO: Replace that by an API call
    current_channel = get_object_or_404(DiscordChannel, pk=channel_pk)
    current_user = get_object_or_404(DiscordUser, pk=user_pk)
    current_player = get_object_or_404(Player, member__user=current_user, channel=current_channel)

    barcode = random.choice([
        "DonaldDuck",
        "KillBill",
        "WantBread",
        "DuckDuckGo",
        "DaffyDuck",
        "HelloThere",
        "ANNIHILATE",
    ])

    # Charts

    return render(request, "botdata/player.jinja2",
                  {"channel": current_channel, "current_user": current_user, "player": current_player,
                   "achievements": achievements, "barcode": barcode})
