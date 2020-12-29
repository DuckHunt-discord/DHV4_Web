from django.urls import path

from . import views

app_name = "docs"
urlpatterns = [
    path('', views.index, name="index"),
    path('<slug:category>', views.category_index, name="category_index"),
    path('<slug:page>', views.display_page, name="page"),
    path('<slug:category>/<slug:page>', views.display_page, name="page"),
    path('<slug:category>/<slug:subcategory>/<slug:page>', views.display_page, name="page"),
]
