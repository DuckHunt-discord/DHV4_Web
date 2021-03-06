from django.urls import path, re_path

from . import views

app_name = "docs"
urlpatterns = [
    path('README', views.index_redirect,),
    path('', views.display_page, name="index", kwargs={"path": "README"}),
    path('summary', views.summary, name="summary"),
    path('SUMMARY', views.summary, name="summary"),
    path('SUMMARY/', views.summary, name="summary"),
    path('INDEX', views.summary, name="summary"),
    path('.gitbook/assets/<str:file>', views.assets, name="assets"),
    re_path(r'(?P<path>(?:[A-z0-9\-]*/?)*)', views.display_page, name="page"),
]
