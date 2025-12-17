import datetime

from django.conf import settings
from django.shortcuts import render
from django.utils.safestring import mark_safe

from botdata.templatetags.global_jinja_funcs import intcomma, show_timestamp
from .utils import get_from_api


def index(request):
    stats_url = settings.DH_API_URL + "/stats"
    api_stats = get_from_api(stats_url)

    parsed_stats = [
        {
            "name": "Members",
            "numerical_value": api_stats['members_count'],
            "value": intcomma(api_stats['members_count']),
            "color": "success",
            "icon": "fas fa-users",
            "odometer": True,
        },
        {
            "name": "Servers",
            "numerical_value": api_stats['guilds_count'],
            "value": intcomma(api_stats['guilds_count']),
            "color": "success",
            "icon": "fas fa-server",
            "odometer": True,
        },
        {
            "name": "Channels",
            "numerical_value": api_stats['channels_count'],
            "value": intcomma(api_stats['channels_count']),
            "color": "success",
            "icon": "fab fa-slack-hash",
            "odometer": True,
        },
        {
            "name": "Active players",
            "numerical_value": api_stats['players_count'],
            "value": intcomma(api_stats['players_count']),
            "color": "success",
            "icon": "fas fa-hat-cowboy-side",
            "odometer": True,
        },
        {
            "name": "Ducks",
            "numerical_value": api_stats['alive_ducks_count'],
            "value": intcomma(api_stats['alive_ducks_count']),
            "color": "success",
            "icon": "fas fa-feather",
            "odometer": True,
        },
    ]

    td = datetime.datetime.now() - datetime.datetime.fromtimestamp(api_stats['uptime'])
    if not api_stats['global_ready']:
        parsed_stats.append(
            {
                "name": mark_safe("Uptime (<a href=\"https://discordstatus.com/\">discord issues</a>)"),
                "value": show_timestamp(api_stats['uptime']),
                "color": "danger",
                "icon": "fas fa-stopwatch",
                "odometer": False,
            },
        )
    elif td > datetime.timedelta(days=7):
        parsed_stats.append(
            {
                "name": "Uptime",
                "value": show_timestamp(api_stats['uptime']),
                "color": "success",
                "icon": "fas fa-stopwatch",
                "odometer": False,
            },
        )
    else:
        parsed_stats.append(
            {
                "name": "Since last update",
                "value": show_timestamp(api_stats['uptime']),
                "color": "success",
                "icon": "fas fa-stopwatch",
                "odometer": False,
            },
        )

    parsed_stats += [
        {
            "name": api_stats['current_event_value'][1],
            "value": api_stats['current_event_value'][0],
            "color": "blurple" if api_stats['current_event_name'] == "CALM" else "warning",
            "icon": "fas fa-bullhorn",
            "scale": 2,
            "odometer": False,
        },

    ]

    return render(request, "public/index.jinja2", {
        "api_stats": api_stats,
        "parsed_stats": parsed_stats,
    })
