from django.contrib import admin
from .settings import COMPANY_NAME
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from mainsite import models
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.decorators.cache import never_cache

class NewAdminSite(admin.AdminSite):
    site_title = gettext_lazy(COMPANY_NAME)
    site_header = gettext_lazy("MAKE MONEY")
    index_title = gettext_lazy("Administration")


# Make the admin site
admin_site = NewAdminSite(name="myAdmin")

# Register the models with the admin site.
admin_site.register(models.KnowledgeBaseEntry)
admin_site.register(models.FAQEntry)