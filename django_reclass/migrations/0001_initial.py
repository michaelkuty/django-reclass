# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import yamlfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dbtemplates', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReclassTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=250, null=True, verbose_name='Label', blank=True)),
                ('path', models.CharField(help_text='Somethink like this: srv/salt/leonardo/app/{name}.yml', max_length=250, verbose_name='Path pattern')),
                ('context', yamlfield.fields.YAMLField(null=True, blank=True)),
                ('extra', yamlfield.fields.YAMLField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('rendered', models.TextField(null=True, blank=True)),
                ('sync', models.NullBooleanField(help_text='Keep synced with Salt Master')),
                ('dbtemplate', models.ForeignKey(related_name='reclass_templates', verbose_name='Template', to='dbtemplates.Template')),
                ('user', models.ForeignKey(related_name='reclass_templates', blank=True, to=settings.AUTH_USER_MODEL, help_text='Optionaly assign to user', null=True, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Reclass Template',
                'verbose_name_plural': 'Reclass Templates',
            },
        ),
    ]
