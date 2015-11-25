from __future__ import unicode_literals

from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_reclass import reclass
from yamlfield.fields import YAMLField
from .signals import push_to_master
from polymorphic import PolymorphicModel


@python_2_unicode_compatible
class ReclassTemplate(PolymorphicModel):

    label = models.CharField(verbose_name=_(
        'Label'), max_length=250, null=True, blank=True)

    path = models.CharField(
        verbose_name=_('Path pattern'), max_length=250,
        help_text=_('Somethink like this: srv/salt/leonardo/app/{name}.yml'))

    dbtemplate = models.ForeignKey(
        'dbtemplates.Template',
        verbose_name=_("Template"),
        related_name="reclass_templates")

    context = YAMLField(blank=True, null=True)
    extra = YAMLField(blank=True, null=True)

    modified = models.DateTimeField(blank=True, null=True)
    rendered = models.TextField(blank=True, null=True)
    sync = models.NullBooleanField(help_text=_('Keep synced with Salt Master'))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        related_name="reclass_templates",
        help_text=_('Optionaly assign to user'),
        null=True, blank=True)

    def __str__(self):
        return self.label

    def push(self, extra_context={}):
        '''Render and Push to Salt Master

        requires context, path and dbtemplate
        optionaly will be use master conf from extra field
        '''
        status = reclass.push(self.get_path(), self.render())
        return status

    def render(self, context={}):
        '''Render Template with context'''

        meta = reclass.render(
            template=self.dbtemplate,
            context=self.get_context(context))

        return meta

    def get_path(self, context={}):
        '''Render Context to path variable and return it'''
        return self.path.format(**self.get_context(context))

    def get_context(self, extra_context={}):
        '''return updated context where extra is primary'''
        ctx = self.context
        ctx.update(extra_context)
        return ctx

    def save(self, *args, **kwargs):

        # render with fail silently
        try:
            self.rendered = self.render()
            self.modified = datetime.now()
        except Exception as e:
            if settings.DEBUG:
                raise e

        super(ReclassTemplate, self).save(*args, **kwargs)

        if self.sync:
            push_to_master.send(sender=ReclassTemplate, template=self)

    class Meta:
        verbose_name = _("Reclass Template")
        verbose_name_plural = _("Reclass Templates")
