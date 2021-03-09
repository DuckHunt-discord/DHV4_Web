from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="shop_index"),
    path('products/', views.view_product, name="shop_product_info_without_ID"),
    path('products/<int:product_id>', views.view_product, name="shop_product_info"),
    path('products/<int:product_id>/info', views.product_api, name="shop_product_api"),
    path('designs/<int:pk>', views.view_design, name="shop_design_info"),
    path('product_types/<int:pk>', views.view_product_type, name="shop_product_type_info"),
    path('designs', views.view_designs, name="shop_designs"),
    path('product_types', views.view_product_types, name="shop_product_types"),
]
