from __future__ import unicode_literals

from datetime import datetime

import yaml
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_reclass import reclass
from django_service_templates.models import ServiceTemplate
from yamlfield.fields import YAMLField

from .signals import push_to_master


class ReclassTemplate(ServiceTemplate):

    reclass = reclass

    def push(self, extra_context={}):
        '''Render and Push to Salt Master

        requires context, path and dbtemplate
        optionaly will be use master conf from extra field
        '''
        status = reclass.push(self.get_path(), self.get_content())
        return status

    def save(self, *args, **kwargs):

        if self.sync:
            # render with fail silently
            try:
                self.rendered = self.render()
                self.modified = datetime.now()
            except Exception as e:
                if settings.DEBUG:
                    raise Exception('Exception was raised {} during rendering {}'.format(e, self.label))

        super(ReclassTemplate, self).save(*args, **kwargs)

        if self.sync:
            push_to_master.send(sender=ReclassTemplate, template=self)

    def get_reclass_path(self, root_path='srv/salt/reclass/classes'):
        '''return doted path for reclass classes.system.app'''
        return self.get_path().replace(root_path, '').replace('/', '.').replace('.yml', '')[1:]

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
        data = self.get_yaml_content()

        if 'classes' in data:
            if cls not in data['classes']:
                data['classes'].append(cls)
                self.rendered = yaml.safe_dump(data)
                self.save()

    def add_service(self, cls):
        '''manipulate with reclass means add and push to master'''

        data = self.get_yaml_content()

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


@python_2_unicode_compatible
class Reclass(models.Model):

    verbose_name = models.CharField(
        verbose_name=_('Verbose Name'), max_length=250)

    name = models.SlugField(verbose_name=_('Name'), max_length=250)

    nodes = models.ManyToManyField(
        ReclassTemplate, related_name="reclass_nodes",
        blank=True)
    classes = models.ManyToManyField(
        ReclassTemplate, related_name="reclass_classes",
        blank=True)

    context = YAMLField(blank=True, null=True)
    extra = YAMLField(blank=True, null=True)

    reclass = models.ManyToManyField(
        'self', related_name="reclasses", blank=True,
        help_text=_('Connect other reclass and all struff would be inherited from them.'))

    modified = models.DateTimeField(
        blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.verbose_name

    def export(self):
        '''Export reclass as standard directory'''
        raise NotImplementedError
