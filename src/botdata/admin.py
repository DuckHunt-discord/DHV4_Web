from django.contrib import admin

from . import models
# Register your models here.

#admin.site.register(models.Aerich)
admin.site.register(models.DiscordChannel)
admin.site.register(models.DiscordGuild)
admin.site.register(models.DiscordMember)
admin.site.register(models.Player)
admin.site.register(models.DiscordUser)
admin.site.register(models.BotList)
admin.site.register(models.Vote)
