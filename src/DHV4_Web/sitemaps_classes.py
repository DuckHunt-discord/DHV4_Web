from django.contrib import sitemaps


class Sitemap(sitemaps.Sitemap):
    """
    Fixes the very annoying Exception while resolving variable 'alternates' in template 'sitemap.xml'

    This is not needed anymore since my fix was added into Django.
    """
    pass


class PaginatedSitemap(Sitemap):
    limit = 1000  # Limit can be set up to 50000
