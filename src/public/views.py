from typing import Optional

from django.shortcuts import render
from django.conf import settings

# Create your views here.
import requests


def get_from_api(url):
    r = requests.get(url)
    return r.json()


def index(request):
    return render(request, "public/index.jinja2")


def bot_commands(request):
    command_to_see: Optional[str] = request.GET.get("command", None)
    commands_url = settings.DH_API_URL + "/help/commands"
    commands = get_from_api(commands_url)

    if command_to_see:
        scs = command_to_see.split()
        commands = commands[scs[0]]
        if len(scs) != 1:
            for sc in scs[1:]:
                commands = commands['subcommands'][sc]

    if command_to_see:
        ctx = {"command_to_see": command_to_see, "command": commands, "prefix": "d!"}
        return render(request, "public/command.jinja2", ctx)
    else:
        ctx = {"commands": commands, "prefix": "d!"}
        return render(request, "public/bot_commands.jinja2", ctx)
