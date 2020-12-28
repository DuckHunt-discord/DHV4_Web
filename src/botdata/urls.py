from django.urls import path

from . import views

urlpatterns = [
    path('guilds', views.guilds, name="guilds"),
    path('guilds/lang/<str:language>', views.guilds, name="guilds"),
    path('guilds/<int:pk>', views.guild, name="guild"),
    path('channels/<int:pk>', views.channel, name="channel"),
    path('channels/<int:pk>/settings', views.channel_settings, name="channel_settings"),
    path('channels/<int:channel_pk>/<int:user_pk>', views.player, name="player"),
]
