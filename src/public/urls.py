from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('commands', views.bot_commands, name="bot_commands"),
    path('', views.index, name="bot_settings"),
]