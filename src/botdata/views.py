import random
import string
import time

from django.core.cache import cache
from collections import namedtuple, defaultdict
from math import inf
from typing import List
from django.db import connection

from django.core.paginator import Paginator, Page
from django.db.models import Prefetch, Q, Count, Exists, OuterRef, Max
from django.http import Http404, HttpResponseGone
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from .models import DiscordGuild, DiscordChannel, DiscordUser, Player, DUCKS_COLORS, DUCKS_DAY_CATEGORIES, \
    DUCKS_NIGHT_CATEGORIES


SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR

# Create your views here.


class CustomPage(Page):
    def included_range(self, start, stop, step=1):
        return range(max(0, start), min(self.paginator.num_pages, stop), step)

    def get_pages_to_show(self):
        shown_numbers = []

        current_page = self.number

        round_offset = current_page % 10

        shown_numbers.extend(
            self.included_range(current_page - (10 + round_offset), current_page + (10 - round_offset))[:20])
        shown_numbers.extend(
            self.included_range(current_page - (100 + round_offset), current_page + (100 - round_offset), 10)[:20])
        shown_numbers.extend(
            self.included_range(current_page - (1000 + round_offset), current_page + (1000 - round_offset), 100)[:20])

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


def get_guilds_list(language=None):
    sql = """
    SELECT
        guilds.language AS guild_language,
        guilds.vip AS guild_vip_status,
        guilds.name AS guild_name,
        guilds.discord_id AS guild_id,
        chasqy.name AS channel_name,
        channel_id AS channel_id,
        players_count
    FROM
        guilds
        INNER JOIN (
            SELECT
                channels.guild_id,
                channels.name,
                channel_id,
                players_count
            FROM
                channels
                INNER JOIN (
                    SELECT
                        channel_id,
                        players_count
                    FROM (
                        SELECT
                            COUNT(id) AS players_count,
                            channel_id
                        FROM
                            players
                        GROUP BY
                            channel_id) AS pla
                    WHERE
                        pla.players_count > 0) AS sqy ON channels.discord_id = sqy.channel_id AND channels.enabled = True)
                         AS chasqy ON chasqy.guild_id = guilds.discord_id
    ORDER BY
        guild_vip_status DESC,
        guild_id ASC;
    """
    res = cache.get('guilds_list_custom_sql')
    if res:
        return res

    with connection.cursor() as cursor:
        cursor.execute(sql)
        desc = [d[0] for d in cursor.description]
        all_data = cursor.fetchall()

    result = defaultdict(list)
    for channel_data in all_data:
        channel_result = {k: v for k, v in zip(desc, channel_data)}

        result[channel_result["guild_id"]].append(channel_result)

    res = list(result.items())
    cache.set('guilds_list_custom_sql', res, 12 * HOUR)
    return res


guilds_list = get_guilds_list()
guilds_paginator = CustomPaginator(guilds_list, 100)
ascii_lowercase = list(string.ascii_lowercase)


def startswith(string_, prefix):
    if prefix == "others":
        return string_[0] not in ascii_lowercase
    else:
        return string_.startswith(prefix)


def guilds(request, language=None):
    # I couldn't find a good way to do this using django ORM without it taking a ton of time.
    page_number = request.GET.get('page', 1)
    name_start_with = request.GET.get('sw', '').lower()

    if language:
        current_guilds_list = [
            (k, v) for k, v in guilds_list
            if v[0]["guild_language"].startswith(language)
               and startswith(v[0]["guild_name"].lower(), name_start_with)
        ]
        filters = []
        current_guilds_paginator = CustomPaginator(current_guilds_list, 100)
    else:
        filters = ascii_lowercase
        if name_start_with:
            current_guilds_list = [
                (k, v) for k, v in guilds_list
                if startswith(v[0]["guild_name"].lower(), name_start_with)
            ]
            current_guilds_paginator = CustomPaginator(current_guilds_list, 100)
        else:
            current_guilds_list = guilds_list
            current_guilds_paginator = guilds_paginator

    if len(current_guilds_list) == 0:
        raise Http404("Nothing matching provided filters")

    page_obj = current_guilds_paginator.get_page(page_number)

    return render(request, "botdata/guilds.jinja2",
                  {"guilds": page_obj, "language": language, "sw": name_start_with, "filters": filters})


def guild(request, pk: int):
    try:
        current_guild = DiscordGuild.objects.get(pk=pk)
    except DiscordGuild.DoesNotExist:
        return render(request, "botdata/no_guild.jinja2", {"guild": None})

    channels = current_guild.channels.filter(enabled=True) \
        .annotate(player_count=Count("players")) \
        .filter(player_count__gt=0)

    if not channels.count():
        return render(request, "botdata/no_guild.jinja2", {"guild": current_guild})

    return render(request, "botdata/guild.jinja2", {"guild": current_guild, "channels": channels})


def sum_dict(d1, d2):
    final = {}
    keys = set(d1.keys())
    keys.update(set(d2.keys()))
    for key in keys:
        final[key] = d1.get(key, 0) + d2.get(key, 0)

    return final


def sum_dicts(dicts):
    final = {}
    for current_dict in dicts:
        final = sum_dict(final, current_dict)

    return final


def generate_shots_chart_data(shooting_stats):
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
            'y': shooting_stats.get(attr_key, 0)
        })

    shots_chart_data.sort(key=lambda d: -d['y'])
    return shots_chart_data


def channel(request, pk: int):
    current_channel = get_object_or_404(DiscordChannel.objects.all().select_related("guild"), pk=pk,)
    # We cast to a list because we slice first then later use the whole thing.
    # If we didn't, we would have 2 queries : one with a limit and one without
    page_number = request.GET.get("page", 1)

    paginator = Paginator(
        Player.objects.filter(channel=current_channel)
            .select_related("member__user")
            .order_by('-experience')
            .only("experience", "member__user__name", "member__user__discord_id", "member__user__discriminator",
                  "member__user__name", "shooting_stats", "best_times", "killed"), 100)

    current_players = paginator.get_page(page_number)

    chart_best_players_data_experience = []
    for chart_player in current_players[:100]:
        if chart_player.experience > 1:
            chart_best_players_data_experience.append({
                'name': str(chart_player.member.user),
                'y': chart_player.experience
            })

    chart_best_players_data_ducks = []
    #
    # for chart_player in sorted(current_players[:100], key=lambda p: -p.total_ducks_killed):
    #    if chart_player.experience > 1:
    #        chart_best_players_data_ducks.append({
    #            'name': str(chart_player.member.user),
    #            'y': chart_player.total_ducks_killed
    #        })

    global_shooting_stats = sum_dicts((p.shooting_stats for p in current_players))

    shots_chart_data = generate_shots_chart_data(global_shooting_stats)

    global_best_times = {}
    for chart_player in current_players:
        for duck_type, time_ in chart_player.best_times.items():
            if global_best_times.get(duck_type, (inf, chart_player))[0] > time_:
                global_best_times[duck_type] = (time_, chart_player)

    chart_best_time = []
    chart_best_colors = []

    for duck_type, best_info in global_best_times.items():
        duck_time, chart_player = best_info
        chart_best_time.append({
            'name': f'{duck_type.title()}<br/>{str(chart_player.member.user)}',
            'y': round(duck_time, 2)
        })
        chart_best_colors.append(DUCKS_COLORS[duck_type])

    return render(request, "botdata/channel.jinja2", {"paginator": paginator, "channel": current_channel, "players": current_players,
                                                      "chart_best_players_data_experience": chart_best_players_data_experience,
                                                      "chart_best_players_data_ducks": chart_best_players_data_ducks,
                                                      "shots_chart_data": shots_chart_data,
                                                      "global_best_times": global_best_times,
                                                      "chart_best_time": chart_best_time,
                                                      "chart_best_colors": chart_best_colors})


def channel_settings(request, pk: int):
    current_channel = get_object_or_404(DiscordChannel.objects.all().select_related("guild"), pk=pk)

    parliament_day_data = []
    parliament_night_data = []

    for duck in sorted(DUCKS_DAY_CATEGORIES):
        parliament_day_data.append(
            [duck.title(),
             getattr(current_channel, f"spawn_weight_{duck}_ducks"),
             DUCKS_COLORS[duck]]
        )

    for duck in sorted(DUCKS_NIGHT_CATEGORIES):
        parliament_night_data.append(
            [duck.title(),
             getattr(current_channel, f"spawn_weight_{duck}_ducks"),
             DUCKS_COLORS[duck]]
        )

    return render(request, "botdata/channel_settings.jinja2", {"channel": current_channel,
                                                               "parliament_day_data": parliament_day_data,
                                                               "parliament_night_data": parliament_night_data})


def player(request, channel_pk: int, user_pk: int):
    from .achievements import achievements, trophys
    # TODO: Replace that by an API call
    current_channel = get_object_or_404(DiscordChannel.objects.all().select_related('guild'), pk=channel_pk)
    current_user = get_object_or_404(DiscordUser, pk=user_pk)
    try:
        current_player = Player.objects.get(member__user=current_user, channel=current_channel)
    except Player.DoesNotExist:
        return HttpResponseGone("410 Gone: The data was deleted, or you can't spell an URL")

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
    shots_chart_data = generate_shots_chart_data(current_player.shooting_stats)

    return render(request, "botdata/player.jinja2",
                  {"channel": current_channel, "current_user": current_user, "player": current_player,
                   "achievements": achievements, "trophys": trophys, "barcode": barcode,
                   "shots_chart_data": shots_chart_data})
