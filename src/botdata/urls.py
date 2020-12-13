from django.urls import path

from . import views

urlpatterns = [
    path('guilds', views.guilds, name="guilds"),
    path('guilds/<int:pk>', views.guild, name="guild"),
    path('channels/<int:pk>', views.channel, name="channel"),
    path('channels/<int:channel_pk>/<int:user_pk>', views.player, name="player"),
]
