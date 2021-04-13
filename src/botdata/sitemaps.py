import collections
import string

from django.contrib import sitemaps

from django.urls import reverse

from botdata.models import Player, DiscordChannel, DiscordGuild
from botdata.views import get_guilds_list


class PaginatedSitemap(sitemaps.Sitemap):
    limit = 1000  # Limit can be set up to 50000


class PlayersPagesSitemap(PaginatedSitemap):
    changefreq = 'always'
    protocol = 'https'

    def items(self):
        return Player.objects.select_related('member').order_by('pk').all()

    def location(self, item):
        return reverse('player', kwargs={'channel_pk': item.channel_id, 'user_pk': item.member.user_id})


class ChannelsPagesSitemap(PaginatedSitemap):
    changefreq = 'hourly'
    protocol = 'https'

    def items(self):
        return DiscordChannel.objects.filter(enabled=True).order_by('pk').all()

    def location(self, item):
        return reverse('channel', kwargs={'pk': item.pk})


class ChannelsSettingsPagesSitemap(PaginatedSitemap):
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return DiscordChannel.objects.filter(enabled=True).order_by('pk').all()

    def location(self, item):
        return reverse('channel', kwargs={'pk': item.pk})


class GuildPagesSitemap(PaginatedSitemap):
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return DiscordGuild.objects.order_by('pk').all()

    def location(self, item):
        return reverse('guild', kwargs={'pk': item.pk})


class GuildListSitemap(PaginatedSitemap):
    changefreq = 'hourly'
    protocol = 'https'

    def items(self):
        guilds = get_guilds_list()

        by_first_letter = collections.Counter()
        guilds_reverse = reverse('guilds')

        for gid, channels in guilds:
            guild_letter = channels[0]["guild_name"][0].lower()
            if guild_letter in string.ascii_lowercase:
                by_first_letter[guild_letter] += 1
            else:
                by_first_letter["others"] += 1

        urls = [guilds_reverse + "?page=" + str(p) for p in range(int(len(guilds)/100) + 1)]

        for first_letter, count in by_first_letter.most_common():
            urls.extend([guilds_reverse + "?page=" + str(p) + "&sw=" + first_letter for p in range(int(count/100) + 1)])

        return urls

    def location(self, item):
        return item

