from public import sitemaps as public_sitemaps
from botdata import sitemaps as botdata_sitemaps
from docs import sitemaps as docs_sitemaps

sitemaps = {
    'public': public_sitemaps.BasePagesSitemap,
    'players': botdata_sitemaps.PlayersPagesSitemap,
    'channels': botdata_sitemaps.ChannelsPagesSitemap,
    'channels_settings': botdata_sitemaps.ChannelsSettingsPagesSitemap,
    'guild': botdata_sitemaps.GuildPagesSitemap,
    'guilds': botdata_sitemaps.GuildListSitemap,
    'docs': docs_sitemaps.DocsSitemap,
    'commands': public_sitemaps.CommandsSitemap,
    'shards_status': public_sitemaps.ShardStatusSitemap,
}
