from typing import Optional

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .utils import HOUR, get_from_api


def get_command(commands, name):
    direct = commands.get(name)

    if direct:
        return direct
    else:
        for command_name, command in commands.items():
            if name in command.get('aliases', []):
                return command


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
                try:
                    commands = get_command(commands['subcommands'], sc)
                except KeyError:
                    raise Http404("No such subcommand")

        if commands is None:
            raise Http404("No such subcommand")

        ctx = {"command_to_see": command_to_see, "parent_name": parent_name, "command": commands, "prefix": "dh!",
               "parent": parent}
        return render(request, "public/command.jinja2", ctx)
    else:
        commands = dict(sorted(commands.items(), key=lambda d: d[1].get('access_value', 50)))
        ctx = {"commands": commands, "prefix": "dh!"}
        return render(request, "public/bot_commands.jinja2", ctx)
