from django.contrib.admin.apps import AdminConfig


class DHAdminConfig(AdminConfig):
    default_site = 'DHV4_Web.admin.DHAdminSite'

