
from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from dbtemplates.models import Template
from django_reclass.models import ReclassTemplate
template = ReclassTemplate.objects.first()
template.render()


class CommandTest(TestCase):

    def setUp(self):

        dbtemplate = Template.create(
            name='leonardo-site',
            content='{{ name }}: {{ name }}')

        self.template = ReclassTemplate.objects.create(
            dbtemplate=dbtemplate,
            context='name: hello',
            path='srv/test/{name}/test'
        )

    def test_01_sync_all(self):

        meta = self.template.render()

        self.assertIn('hello', meta)
        self.assertIn('hello', self.template.get_path({'name': 'hello'}))
