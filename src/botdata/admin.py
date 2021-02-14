from django.contrib import admin

from . import models


# Register your models here.


class DiscordChannelAdmin(admin.ModelAdmin):
    raw_id_fields = ["guild"]


admin.site.register(models.DiscordChannel, DiscordChannelAdmin)


class DiscordGuildAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.DiscordGuild, DiscordGuildAdmin)


class DiscordMemberAdmin(admin.ModelAdmin):
    raw_id_fields = ["guild", "user"]


admin.site.register(models.DiscordMember, DiscordMemberAdmin)


class PlayerAdmin(admin.ModelAdmin):
    raw_id_fields = ["channel", "member"]

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


class VoteAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]


admin.site.register(models.Vote, VoteAdmin)
