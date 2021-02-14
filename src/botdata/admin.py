from django.contrib import admin
from dynamic_raw_id.admin import DynamicRawIDMixin

from . import models


# Register your models here.


class DiscordChannelAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["guild"]


admin.site.register(models.DiscordChannel, DiscordChannelAdmin)


class DiscordGuildAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.DiscordGuild, DiscordGuildAdmin)


class DiscordMemberAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["guild", "user"]


admin.site.register(models.DiscordMember, DiscordMemberAdmin)


class PlayerAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["channel", "member"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('member__user', 'channel')


admin.site.register(models.Player, PlayerAdmin)


class DiscordUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.DiscordUser, DiscordUserAdmin)


class BotListAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.BotList, BotListAdmin)


class VoteAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["user"]


admin.site.register(models.Vote, VoteAdmin)
