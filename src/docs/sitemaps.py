from django.contrib.flatpages import sitemaps
from django.urls import reverse

from docs.views import MARKDOWN_FILES


class DocsSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return list(MARKDOWN_FILES.rglob("*.md"))

    def location(self, item):
        return reverse('docs:page', kwargs={"path": str(item).replace('.md', '')[len(str(MARKDOWN_FILES)) + 1:]})

