"""DHV4_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from django.contrib.sitemaps import views as sitemap_views
from django.views.static import serve

from .sitemaps import sitemaps

urlpatterns = [
    path('', include('public.urls')),
    path('docs/', include('docs.urls'), ),
    path('data/', include('botdata.urls')),
    path('tags/', include('tags.urls')),
    path('shop/', include('shop.urls')),
    path('admin/', admin.site.urls),
    path('admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('sitemap.xml', sitemap_views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^images/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

handler404 = 'public.views.handler404'