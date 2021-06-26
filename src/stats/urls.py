from django.urls import path

from . import views

app_name = 'stats'

urlpatterns = [
    path('support', views.support, name="support"),
    path('landmines', views.landmines, name="landmines"),
]
