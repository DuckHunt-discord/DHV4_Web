from django.urls import reverse

from DHV4_Web.sitemaps_classes import Sitemap
from . import models


class ProductPagesSitemap(Sitemap):
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return models.Product.objects.all().order_by('pk')

    def location(self, item):
        return reverse('shop_product_info', kwargs={'product_id': item.pk})


class DesignPagesSitemap(Sitemap):
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return models.Design.objects.all().order_by('pk')

    def location(self, item):
        return reverse('shop_design_info', kwargs={'pk': item.pk})


class ProductTypePagesSitemap(Sitemap):
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return models.ProductType.objects.all().order_by('pk')

    def location(self, item):
        return reverse('shop_product_type_info', kwargs={'pk': item.pk})


