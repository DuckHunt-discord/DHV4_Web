from django.urls import reverse
from django.utils.safestring import mark_safe
from django_jinja import library
from .. import models

product_types_infos = []
for product_type in models.ProductType.objects.all().order_by('name'):
    product_types_infos.append((product_type, reverse('shop_product_type_info', {"pk": product_type.pk})))

designs_infos = []
for design in models.Design.objects.all().order_by('name'):
    designs_infos.append((design, reverse('shop_design_info', {"pk": design.pk})))


@library.global_function()
def get_shop_product_types():
    return product_types_infos


@library.global_function()
def get_shop_designs():
    return designs_infos
