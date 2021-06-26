from django.urls import path

from . import views

app_name = 'stats'

urlpatterns = [
    path('landmines', views.landmines, name="landmines"),
]
