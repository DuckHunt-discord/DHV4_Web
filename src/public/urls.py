from django.urls import path, re_path

from public.views.bot_commands import bot_commands
from public.views.botlists import botlists
from public.views.duckroll import duckroll
from public.views.handler404 import handler404
from public.views.index import index
from public.views.invite_bot import invite_bot
from public.views.privacy_policy import privacy_policy
from public.views.robots_txt import robots_txt
from public.views.shard_status import shard_status
from public.views.status import status
from public.views.support_server import support_server
from public.views.tombstone import tombstone


urlpatterns = [
    path('', index, name="index"),
    path('invite', invite_bot, name="invite_bot"),
    path('invite_bot', invite_bot,),
    path('support', support_server, name="support_server"),
    path('support_server', support_server,),
    path('privacy_policy', privacy_policy, name="privacy_policy"),
    path('botlists', botlists, name="botlists"),
    path('robots.txt', robots_txt, name="robotstxt"),
    path('cartographer', duckroll, name="duckroll"),
    path('commands', bot_commands, name="bot_commands"),
    re_path(r'commands/(?P<command>(?:[A-z0-9\-]*/?)*)', bot_commands, name="bot_commands"),
    path('status', status, name="bot_status"),
    path('status/<int:shard_id>', shard_status, name="bot_shard_status"),
    path('web_api/tombstone/', tombstone, name="tombstone"),
    path('404page', handler404),
]
