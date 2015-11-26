
from django.contrib import admin

from .models import ReclassTemplate
from django_service_templates.admin import ServiceTemplateAdmin


class ReclassTemplateAdmin(ServiceTemplateAdmin):

    pass

admin.site.register(ReclassTemplate, ReclassTemplateAdmin)
