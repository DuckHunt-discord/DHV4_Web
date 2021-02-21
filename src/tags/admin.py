from django.contrib import admin
from dynamic_raw_id.admin import DynamicRawIDMixin

from . import models


# Register your models here.

class AliasesInline(DynamicRawIDMixin, admin.TabularInline):
    dynamic_raw_id_fields = ["owner"]

    model = models.TagAlias


class TagsAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    list_display = ["name", "official", "uses", "revisions", "created", "last_modified",]

    dynamic_raw_id_fields = ["owner"]
    inlines = [
        AliasesInline,
    ]


admin.site.register(models.Tag, TagsAdmin)

