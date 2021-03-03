from django.contrib import admin
from imagekit.admin import AdminThumbnail

from . import models
# Register your models here.


class PictureInline(admin.TabularInline):
    model = models.ProductPicture
    admin_thumbnail = AdminThumbnail(image_field='photo')


class ProductAdmin(admin.ModelAdmin):
    inlines = [PictureInline]
    list_select_related = ('design', 'product_type')
    list_display = ['__str__', 'design', 'color', 'product_type', 'get_print_location_display']


admin.site.register(models.Product, ProductAdmin)


class DesignAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Design, DesignAdmin)


class ProductTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.ProductType, ProductTypeAdmin)
