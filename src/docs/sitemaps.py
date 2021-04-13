from django.urls import reverse

from DHV4_Web.sitemaps_classes import Sitemap
from docs.views import MARKDOWN_FILES


class DocsSitemap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return list(MARKDOWN_FILES.rglob("*.md"))

    def location(self, item):
        return reverse('docs:page', kwargs={"path": str(item).replace('.md', '')[len(str(MARKDOWN_FILES)) + 1:]})

