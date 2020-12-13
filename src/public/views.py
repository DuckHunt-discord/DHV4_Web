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


def get_command(commands, name):
    direct = commands.get(name)

    if direct:
        return direct
    else:
        for command_name, command in commands.items():
            if name in command.get('aliases', []):
                return command


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

        ctx = {"command_to_see": command_to_see, "parent_name": parent_name, "command": commands, "prefix": "d!", "parent": parent}
        return render(request, "public/command.jinja2", ctx)
    else:
        ctx = {"commands": commands, "prefix": "d!"}
        return render(request, "public/bot_commands.jinja2", ctx)
