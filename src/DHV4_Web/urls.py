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
from django.contrib import admin
from django.urls import path, include

from django.contrib.sitemaps import views as sitemap_views
from .sitemaps import sitemaps

urlpatterns = [
    path('', include('public.urls')),
    path('docs/', include('docs.urls'), ),
    path('data/', include('botdata.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('sitemap.xml', sitemap_views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
