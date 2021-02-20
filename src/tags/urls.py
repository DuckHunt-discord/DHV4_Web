from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('<str:tag_name>', views.tag, name="tag"),
]
