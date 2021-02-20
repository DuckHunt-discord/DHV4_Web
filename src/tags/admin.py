from django.contrib import admin
from dynamic_raw_id.admin import DynamicRawIDMixin

from . import models


# Register your models here.

class AliasesInline(DynamicRawIDMixin, admin.TabularInline):
    dynamic_raw_id_fields = ["owner"]

    model = models.TagAlias


class TagsAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["owners"]
    inlines = [
        AliasesInline,
    ]


admin.site.register(models.Tag, TagsAdmin)

