from django.urls import reverse

from django.conf import settings
from DHV4_Web.sitemaps_classes import Sitemap
from public.views.utils import get_from_api


class BasePagesSitemap(Sitemap):
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['index', 'bot_commands', 'bot_status']

    def location(self, item):
        return reverse(item)


class CommandsSitemap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'

    def recurse_subcommand(self, command, myname=None):
        my_subcommands = command.get('subcommands', {})

        my_subcommands_parsed = []

        for subcommand_name, subcommand in my_subcommands.items():
            my_subcommands_parsed.extend(self.recurse_subcommand(subcommand, myname=subcommand_name))

        if myname:
            my_subcommands_parsed = [s.replace(myname, '', 1) for s in my_subcommands_parsed]
        else:
            myname = command['name']

        aliases = command.get('aliases', []) + [myname]

        all_of_them = []
        for alias in aliases:
            all_of_them.extend([f"{alias}/{subcommand}" for subcommand in my_subcommands_parsed])
            all_of_them.append(alias)

        return all_of_them

    def items(self):
        commands_url = settings.DH_API_URL + "/help/commands"
        commands = get_from_api(commands_url, cache_for=24 * 60 * 60)

        all_paths = []
        for command_name, command in commands.items():
            all_paths.extend(self.recurse_subcommand(command))

        return all_paths

    def location(self, item):
        return reverse('bot_commands', kwargs={'command': item})


class ShardStatusSitemap(Sitemap):
    changefreq = 'always'
    protocol = 'https'

    def items(self):
        status_url = settings.DH_API_URL + "/status"
        api_status = get_from_api(status_url)

        return [shard["shard_id"] for shard in api_status["shards_status"]]

    def location(self, item):
        return reverse('bot_shard_status', kwargs={'shard_id': item})
