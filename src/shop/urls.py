from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="shop_index"),
    path('product/<int:product_id>', views.view_product, name="shop_product_info"),
]
