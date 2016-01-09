
from django.contrib import admin

from .models import ReclassTemplate, Reclass
from django_service_templates.admin import ServiceTemplateAdmin


class ReclassTemplateAdmin(ServiceTemplateAdmin):

    pass

admin.site.register(ReclassTemplate, ReclassTemplateAdmin)


class ReclassAdmin(admin.ModelAdmin):

    prepopulated_fields = {"name": ("verbose_name",)}


admin.site.register(Reclass, ReclassAdmin)
