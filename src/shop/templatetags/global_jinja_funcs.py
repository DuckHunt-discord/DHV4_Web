from django.urls import reverse
from django.utils.safestring import mark_safe
from django_jinja import library
from .. import models
from django.core.cache import cache


@library.global_function()
def get_shop_product_types():
    product_types_infos = cache.get('shop_product_type_infos')

    if not product_types_infos:
        for product_type in models.ProductType.objects.all().order_by('name'):
            product_types_infos.append((product_type, reverse('shop_product_type_info', kwargs={"pk": product_type.pk})))
        cache.set('shop_product_type_infos', product_types_infos, 3600)

    return product_types_infos


@library.global_function()
def get_shop_designs():
    designs_infos = cache.get('shop_design_infos')

    if not designs_infos:
        for design in models.Design.objects.all().order_by('name'):
            designs_infos.append((design, reverse('shop_design_info', kwargs={"pk": design.pk})))

        cache.set('shop_design_infos', designs_infos, 3600)

    return designs_infos
