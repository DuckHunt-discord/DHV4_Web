from typing import Optional

from django.core.cache import cache
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.template import loader

# Create your views here.
import requests
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page

from botdata.templatetags.global_jinja_funcs import show_timestamp, intcomma

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
MONTH = 30 * DAY
YEAR = 365 * DAY


def get_from_api(url, cache_for=60):
    r = cache.get('duckhunt_api_' + url)
    if not r:
        try:
            r = requests.get(url).json()
            cache.set('duckhunt_api_' + url, r, cache_for)
            return r
        except:
            if "api/status" in url:
                return {
                    "bot_latency": 0,
                    "shards_status": [],
                    "unsharded_guilds": []
                }
            elif "api/stats" in url:
                return {
                    "members_count": 0,
                    "guilds_count": 0,
                    "channels_count": 0,
                    "players_count": 0,
                    "alive_ducks_count": 0,
                    "uptime": 0,
                    "current_event_name": "DOWN",
                    "current_event_value": ["Bot is down", "Bot under maintenance"],
                    "global_ready": False,
                }
            elif "api/commands" in url:
                return None
    return r


def index(request):
    stats_url = settings.DH_API_URL + "/stats"
    api_stats = get_from_api(stats_url)

    parsed_stats = [
        {
            "name": "Guilds",
            "value": intcomma(api_stats['guilds_count']),
            "color": "success",
            "icon": "fas fa-server",
            "odometer": True,
        },
        {
            "name": "Channels",
            "value": intcomma(api_stats['channels_count']),
            "color": "success",
            "icon": "fab fa-slack-hash",
            "odometer": True,
        },
        {
            "name": "Players",
            "value": intcomma(api_stats['players_count']),
            "color": "success",
            "icon": "fas fa-hat-cowboy-side",
            "odometer": True,
        },
        {
            "name": "Members",
            "value": intcomma(api_stats['members_count']),
            "color": "success",
            "icon": "fas fa-users",
            "odometer": True,
        },
        {
            "name": "Ducks",
            "value": intcomma(api_stats['alive_ducks_count']),
            "color": "success",
            "icon": "fas fa-feather",
            "odometer": True,
        },
        {
            "name": "Uptime" if api_stats['global_ready'] else mark_safe(
                "Uptime (<a href=\"https://discordstatus.com/\">discord issues</a>)"),
            "value": show_timestamp(api_stats['uptime']),
            "color": "success" if api_stats['global_ready'] else "danger",
            "icon": "fas fa-stopwatch",
            "odometer": False,
        },
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


def get_command(commands, name):
    direct = commands.get(name)

    if direct:
        return direct
    else:
        for command_name, command in commands.items():
            if name in command.get('aliases', []):
                return command


@cache_page(2 * MINUTE)
def status(request):
    status_url = settings.DH_API_URL + "/status"
    api_status = get_from_api(status_url)

    return render(request, "public/status.jinja2", {"status": api_status})


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


@cache_page(1 * HOUR)
def bot_commands(request, command: str = None):
    if not command:
        command_to_see: Optional[str] = request.GET.get("command", None)
    else:
        command_to_see = ' '.join(command.strip('/').split('/'))

    commands_url = settings.DH_API_URL + "/help/commands"
    commands = get_from_api(commands_url, cache_for=24 * 60 * 60)

    if not commands:
        return render(request, "public/commands_api_error.jinja2")

    if command_to_see:
        scs = command_to_see.split()
        commands = get_command(commands, scs[0])

        parent = None
        parent_name = None
        if len(scs) != 1:
            parent_name = ' '.join(scs[:-1])
            for sc in scs[1:]:
                if commands is None:
                    raise Http404("No such command")

                parent = commands
                commands = get_command(commands['subcommands'], sc)

        if commands is None:
            raise Http404("No such subcommand")

        ctx = {"command_to_see": command_to_see, "parent_name": parent_name, "command": commands, "prefix": "dh!",
               "parent": parent}
        return render(request, "public/command.jinja2", ctx)
    else:
        commands = dict(sorted(commands.items(), key=lambda d: d[1].get('access_value', 50)))
        ctx = {"commands": commands, "prefix": "dh!"}
        return render(request, "public/bot_commands.jinja2", ctx)


def robots_txt(request):
    lines = [
        "User-Agent: *",
        f"Disallow: {reverse('guild', kwargs={'pk': 0})}",
        "",
        "Sitemap: https://duckhunt.me/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def handler404(request, exception=None):
    content = loader.render_to_string('public/404.jinja2', None, request)
    return HttpResponse(content, None, 404)
