from django.http import HttpResponse
from django.urls import reverse


def robots_txt(request):
    lines = [
        "User-Agent: *",
        f"Disallow: {reverse('guild', kwargs={'pk': 0})}",
        "",
        "Sitemap: https://duckhunt.me/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
