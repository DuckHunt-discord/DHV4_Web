from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('robots.txt', views.robots_txt, name="robotstxt"),
    path('commands', views.bot_commands, name="bot_commands"),
    re_path(r'commands/(?P<command>(?:[A-z0-9\-]*/?)*)', views.bot_commands, name="bot_commands"),
    path('status', views.status, name="bot_status"),
    path('status/<int:shard_id>', views.shard_status, name="bot_shard_status"),
]
