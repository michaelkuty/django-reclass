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
import yaml


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
        status = reclass.push(self.get_path(), self.get_data())
        return status

    def get_data(self):
        '''returns rendered data if is present or render new'''

        if self.rendered:
            return self.rendered

        self.rendered = self.render()
        self.save()

        return self.rendered

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
        ctx = self.context or {}
        ctx.update(extra_context)
        return ctx

    def save(self, *args, **kwargs):

        if not self.rendered and self.sync:
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

    def get_reclass_path(self):
        '''return doted path for reclass classes.system.app'''
        return self.get_path().replace('srv/salt/reclass/classes', '').replace('/', '.').replace('.yml', '')[1:]

    def get_yaml_template(self):
        '''specific reclass/heat method'''
        return yaml.load(self.get_data())

    def add_class_to_node(self, name, push=False):
        '''add class to node template'''
        path = self.get_reclass_path()
        node = reclass.get_node(name)
        node.add_class(path)
        node.push()

    def add_class_to_salt_master(self, push=False):
        '''add class to salt master template'''
        path = self.get_reclass_path()
        reclass.salt_master.add_class(path)
        reclass.salt_master.push()

    def add_service_to_salt_master(self, push=False):
        '''add class to salt master template'''
        path = self.get_reclass_path()
        reclass.salt_master.add_service(path)
        reclass.salt_master.push()

    def add_class(self, cls):
        '''manipulate with reclass means add and push to master'''
        data = self.get_yaml_template()

        if 'classes' in data:
            if cls not in data['classes']:
                data['classes'].append(cls)
                self.rendered = yaml.safe_dump(data)
                self.save()

    def add_service(self, cls):
        '''manipulate with reclass means add and push to master'''

        data = self.get_yaml_template()

        if 'services' in data:
            data['services'].append(cls)
            self.rendered = yaml.safe_dump(data)
            self.save()

    def paramaters(self, paramaters):
        '''manipulate with reclass means add and push to master'''
        raise NotImplementedError

    class Meta:
        verbose_name = _("Reclass Template")
        verbose_name_plural = _("Reclass Templates")
