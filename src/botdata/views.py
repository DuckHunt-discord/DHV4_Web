import random

from django.core.paginator import Paginator, Page
from django.db.models import Prefetch, Q, Count, Exists, OuterRef, Max
from django.shortcuts import render, get_object_or_404
from .models import DiscordGuild, DiscordChannel, DiscordUser, Player


# Create your views here.

class CustomPage(Page):
    def included_range(self, start, stop, step=1):
        return range(max(0, start), min(self.paginator.num_pages, stop), step)

    def get_pages_to_show(self):
        shown_numbers = []

        current_page = self.number

        round_offset = current_page % 10

        shown_numbers.extend(self.included_range(current_page-(5+round_offset), current_page+(10-round_offset))[:10])
        shown_numbers.extend(self.included_range(current_page-(50+round_offset), current_page+(100-round_offset), 10)[:10])
        shown_numbers.extend(self.included_range(current_page-(500+round_offset), current_page+(1000-round_offset), 100)[:10])

        shown_numbers = list(set(shown_numbers))

        shown_numbers.sort()

        if shown_numbers[0] == 0:
            shown_numbers = shown_numbers[1:]

        return shown_numbers


class CustomPaginator(Paginator):
    def _get_page(self, *args, **kwargs):
        """
        Return an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return CustomPage(*args, **kwargs)


def guilds(request):
    enabled_channels_qs = DiscordChannel.objects \
        .filter(enabled=True) \
        .annotate(player_count=Count("players")) \
        .filter(player_count__gt=0)

    guilds_list = DiscordGuild.objects \
        .filter(Q(channels__in=enabled_channels_qs) & Q(channels__isnull=False)) \
        .prefetch_related(
            Prefetch("channels", queryset=enabled_channels_qs)
        ) \
        .distinct() \
        .order_by('-vip')

    guilds_paginator = CustomPaginator(guilds_list, 50)
    page_number = request.GET.get('page', 1)
    page_obj = guilds_paginator.get_page(page_number)

    return render(request, "botdata/guilds.jinja2", {"guilds": page_obj})


def guild(request, pk: int):
    try:
        current_guild = DiscordGuild.objects.get(pk=pk)
    except DiscordGuild.DoesNotExist:
        return render(request, "botdata/no_guild.jinja2", {"guild": None})

    channels = current_guild.channels.filter(enabled=True)\
        .annotate(player_count=Count("players")) \
        .filter(player_count__gt=0)

    if not channels.count():
        return render(request, "botdata/no_guild.jinja2", {"guild": current_guild})

    return render(request, "botdata/guild.jinja2", {"guild": current_guild, "channels": channels})


def channel(request, pk: int):
    current_channel = get_object_or_404(DiscordChannel, pk=pk)
    current_players = Player.objects.filter(channel=current_channel).select_related("member__user").order_by(
        '-experience')
    return render(request, "botdata/channel.jinja2", {"channel": current_channel, "players": current_players})


def channel_settings(request, pk: int):
    current_channel = get_object_or_404(DiscordChannel, pk=pk)
    return render(request, "botdata/channel_settings.jinja2", {"channel": current_channel})


def player(request, channel_pk: int, user_pk: int):
    from .achievements import achievements, trophys
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

    shots_chart_data = []

    for attr_key, attr_name in [
        ('shots_when_dead', 'When dead'),
        ('shots_when_wet', 'When wet'),
        ('shots_when_confiscated', 'Without a weapon'),
        ('shots_when_sabotaged', 'With a sabotaged weapon'),
        ('shots_when_jammed', 'With a jammed weapon'),
        ('shots_with_empty_magazine', 'Without bullets'),
        ('shots_jamming_weapon', 'Jamming the gun'),
        ('shots_with_duck', 'With ducks'),
        ('shots_without_ducks', 'Without ducks'),
        ('shots_stopped_by_detector', 'Stopped by the detector'),
    ]:
        shots_chart_data.append({
            'name': attr_name,
            'y': current_player.shooting_stats.get(attr_key, 0)
        })
    shots_chart_data.sort(key=lambda d: -d['y'])

    return render(request, "botdata/player.jinja2",
                  {"channel": current_channel, "current_user": current_user, "player": current_player,
                   "achievements": achievements, "trophys": trophys, "barcode": barcode, "shots_chart_data": shots_chart_data})
