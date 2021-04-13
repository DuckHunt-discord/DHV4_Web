from django.contrib import sitemaps

class Sitemap(sitemaps.Sitemap):
    """
    Fixes the very annoying Exception while resolving variable 'alternates' in template 'sitemap.xml'
    """
    def _urls(self, *args, **kwargs):
        urls = super()._urls(*args, **kwargs)

        for url_info in urls:
            url_info['alternates'] = []

        return urls


class PaginatedSitemap(sitemaps.Sitemap):
    limit = 1000  # Limit can be set up to 50000
