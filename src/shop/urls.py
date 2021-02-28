from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="shop_index"),
    path('product/<int:product_id>', views.view_product, name="shop_product_info"),
    path('product/<int:product_id>/info', views.product_api, name="shop_product_api"),
    path('design/<int:pk>', views.view_design, name="shop_design_info"),
    path('product_type/<int:pk>', views.view_product_type, name="shop_product_type_info"),
]
