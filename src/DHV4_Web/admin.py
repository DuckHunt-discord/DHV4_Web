from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#overriding-the-default-admin-site
class DHAdminSite(admin.AdminSite):
    site_header = _('DuckHunt administration')
    site_title = _('DuckHunt administration')
    index_title = _('DuckHunt Website Administration')
