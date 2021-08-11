from django.contrib import admin
from dynamic_raw_id.admin import DynamicRawIDMixin

from . import models


# Register your models here.

class DiscordMemberInline(DynamicRawIDMixin, admin.TabularInline):
    dynamic_raw_id_fields = ["guild"]
    model = models.DiscordMember
    extra = 0


class DiscordChannelInline(admin.StackedInline):
    model = models.DiscordChannel
    extra = 0


class DiscordChannelAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["guild"]


admin.site.register(models.DiscordChannel, DiscordChannelAdmin)


class DiscordGuildAdmin(admin.ModelAdmin):
    inlines = [
        DiscordChannelInline,
    ]


admin.site.register(models.DiscordGuild, DiscordGuildAdmin)


class DiscordMemberAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["guild", "user"]


admin.site.register(models.DiscordMember, DiscordMemberAdmin)


class PlayerAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["channel", "member", "weapon_sabotaged_by"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('member__user', 'channel')


admin.site.register(models.Player, PlayerAdmin)


class DiscordUserAdmin(admin.ModelAdmin):
    inlines = [
        DiscordMemberInline,
    ]


admin.site.register(models.DiscordUser, DiscordUserAdmin)


class UserInventoryAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["user"]


admin.site.register(models.UserInventory, UserInventoryAdmin)


class Event2021UserDataAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["user"]


admin.site.register(models.LandminesUserData, Event2021UserDataAdmin)


class Event2021LandminesAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["placed_by", "stopped_by"]

    list_display = ["word", "placed_by", "stopped_by", "stopped_at"]
    list_select_related = ["placed_by", "stopped_by"]


admin.site.register(models.LandminesPlaced, Event2021LandminesAdmin)


class Event2021LandminesAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["protected_by", ]

    list_display = ["word", "protected_by", "placed"]
    list_select_related = ["protected_by"]


admin.site.register(models.LandminesProtects, Event2021LandminesAdmin)


class BotListAdmin(admin.ModelAdmin):

    list_display = ["name", "can_vote", "webhook_handler", "post_stats_method", "bot_verified", "bot_certified"]
    ordering = ["key"]

    fieldsets = (
        (None, {
            'fields': (('key', 'name'), 'bot_url', 'notes', 'auth', 'can_vote')
        }),
        ('Votes', {
            'description': "Everything about the users votes",
            'classes': ('collapse',),
            'fields': ('vote_url', 'vote_every',),
        }),
        (None, {
            'fields': ('webhook_handler', )
        }),
        ('Webhooks', {
            'description': "Webhooks are used to give vote rewards",
            'classes': ('collapse',),
            'fields': ('webhook_authorization_header', 'webhook_user_id_json_field', 'webhook_auth',),
        }),
        ('Check URL', {
            'description': "Two methods exist to check if one can vote: webhook+timedelta, "
                           "where the bot checks when the users voted last based on the database informations, or "
                           "by using an URL that returns a value if a user voted recently.",
            'classes': ('collapse',),
            'fields': ('check_vote_url', ('check_vote_key', 'check_vote_negate',),),
        }),

        (None, {
            'fields': ('post_stats_method',)
        }),
        ('Statistics', {
            'description': "Pushing statistics make lists owners happy and make the bot pages more interesting to "
                           "users if the bot has enough servers.",
            'classes': ('collapse',),
            'fields': ('post_stats_url', ('post_stats_server_count_key', 'post_stats_shard_count_key',),),
        }),
        ('Verification', {
            'description': "This is a place to see how recognized the bot is by the botlist. Note that some bot lists "
                           "don't certify bots (anymore).",
            'fields': (('bot_verified', 'bot_certified'), 'embed_code',),
        }),
    )


admin.site.register(models.BotList, BotListAdmin)


class VoteAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    dynamic_raw_id_fields = ["user"]

    list_display = ["user", "bot_list", "at"]
    ordering = ["-at"]


admin.site.register(models.Vote, VoteAdmin)


class SupportTicketAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    list_display = ["user", "opened_at", "opened_for", "closed"]
    readonly_fields = ('opened_at',)
    ordering = ["-opened_at"]

    dynamic_raw_id_fields = ["user", "closed_by"]


admin.site.register(models.SupportTicket, SupportTicketAdmin)

