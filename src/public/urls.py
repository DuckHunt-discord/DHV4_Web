from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('commands', views.bot_commands, name="bot_commands"),
    path('', views.index, name="bot_settings"),
    path('status', views.status, name="bot_status"),
    path('status/<int:shard_id>', views.shard_status, name="bot_shard_status"),
]