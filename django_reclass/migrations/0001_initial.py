# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_service_templates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReclassTemplate',
            fields=[
                ('servicetemplate_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_service_templates.ServiceTemplate')),
            ],
            options={
                'verbose_name': 'Reclass Template',
                'verbose_name_plural': 'Reclass Templates',
            },
            bases=('django_service_templates.servicetemplate',),
        ),
    ]
