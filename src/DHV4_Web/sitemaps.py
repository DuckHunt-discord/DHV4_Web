from public import sitemaps as public_sitemaps
from botdata import sitemaps as botdata_sitemaps
from docs import sitemaps as docs_sitemaps
from shop import sitemaps as shop_sitemaps

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
    'shop_products': shop_sitemaps.ProductPagesSitemap,
    'shop_designs': shop_sitemaps.DesignPagesSitemap,
    'shop_product_types': shop_sitemaps.ProductTypePagesSitemap,
}
