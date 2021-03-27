from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('invite', views.invite_bot, name="invite_bot"),
    path('invite_bot', views.invite_bot,),
    path('support', views.support_server, name="support_server"),
    path('support_server', views.invite_bot,),
    path('privacy_policy', views.privacy_policy, name="privacy_policy"),
    path('botlists', views.botlists, name="botlists"),
    path('robots.txt', views.robots_txt, name="robotstxt"),
    path('commands', views.bot_commands, name="bot_commands"),
    re_path(r'commands/(?P<command>(?:[A-z0-9\-]*/?)*)', views.bot_commands, name="bot_commands"),
    path('status', views.status, name="bot_status"),
    path('status/<int:shard_id>', views.shard_status, name="bot_shard_status"),
    path('404page', views.handler404),
    re_path(r'fr/.*', views.old_pages_and_weird_urls),
]
