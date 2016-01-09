# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import yamlfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_reclass', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reclass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('verbose_name', models.CharField(max_length=250, verbose_name='Verbose Name')),
                ('name', models.SlugField(max_length=250, verbose_name='Name')),
                ('context', yamlfield.fields.YAMLField(null=True, blank=True)),
                ('extra', yamlfield.fields.YAMLField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('classes', models.ManyToManyField(related_name='reclass_classes', to='django_reclass.ReclassTemplate', blank=True)),
                ('nodes', models.ManyToManyField(related_name='reclass_nodes', to='django_reclass.ReclassTemplate', blank=True)),
                ('reclass', models.ManyToManyField(help_text='Connect other reclass and all struff would be inherited from them.', related_name='_reclass_reclass_+', to='django_reclass.Reclass', blank=True)),
            ],
        ),
    ]
