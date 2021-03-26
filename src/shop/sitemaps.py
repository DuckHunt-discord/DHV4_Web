from typing import List, Optional

from django.contrib.flatpages import sitemaps
from django.urls import reverse

from DHV4_Web import settings
from public.views import get_from_api

from . import models


class ProductPagesSitemap(sitemaps.Sitemap):
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return models.Product.objects.all().order_by('pk')

    def location(self, item):
        return reverse('shop_product_info', kwargs={'product_id': item.pk})


class DesignPagesSitemap(sitemaps.Sitemap):
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return models.Design.objects.all().order_by('pk')

    def location(self, item):
        return reverse('shop_design_info', kwargs={'pk': item.pk})


class ProductTypePagesSitemap(sitemaps.Sitemap):
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return models.ProductType.objects.all().order_by('pk')

    def location(self, item):
        return reverse('shop_product_type_info', kwargs={'pk': item.pk})
