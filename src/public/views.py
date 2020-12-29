from typing import Optional

from django.http import Http404
from django.shortcuts import render
from django.conf import settings

# Create your views here.
import requests
from django.views.decorators.cache import cache_page

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
MONTH = 30 * DAY
YEAR = 365 * DAY


def get_from_api(url):
    r = requests.get(url)
    return r.json()


def index(request):
    return render(request, "public/index.jinja2")


def get_command(commands, name):
    direct = commands.get(name)

    if direct:
        return direct
    else:
        for command_name, command in commands.items():
            if name in command.get('aliases', []):
                return command


@cache_page(15*SECOND)
def status(request):
    status_url = settings.DH_API_URL + "/status"
    api_status = get_from_api(status_url)

    return render(request, "public/status.jinja2", {"status": api_status})


@cache_page(15*SECOND)
def shard_status(request, shard_id):
    status_url = settings.DH_API_URL + "/status"
    api_status = get_from_api(status_url)

    for shard in api_status["shards_status"]:
        if shard["shard_id"] == shard_id:
            break
    else:
        shard = None

    return render(request, "public/shard_status.jinja2", {"status": api_status, "shard": shard})


@cache_page(MONTH)
def bot_commands(request):
    command_to_see: Optional[str] = request.GET.get("command", None)
    commands_url = settings.DH_API_URL + "/help/commands"
    commands = get_from_api(commands_url)

    if command_to_see:
        scs = command_to_see.split()
        commands = get_command(commands, scs[0])

        parent = None
        parent_name = None
        if len(scs) != 1:
            parent_name = ' '.join(scs[:-1])
            for sc in scs[1:]:
                parent = commands
                commands = get_command(commands['subcommands'], sc)

        if commands is None:
            raise Http404("No such command")

        ctx = {"command_to_see": command_to_see, "parent_name": parent_name, "command": commands, "prefix": "d!", "parent": parent}
        return render(request, "public/command.jinja2", ctx)
    else:
        commands = dict(sorted(commands.items(), key=lambda d: d[1].get('access_value', 50)))
        ctx = {"commands": commands, "prefix": "d!"}
        return render(request, "public/bot_commands.jinja2", ctx)
