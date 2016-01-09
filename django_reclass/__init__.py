
from django.apps import AppConfig
from .reclass import Reclass


default_app_config = 'django_reclass.Config'


LEONARDO_APPS = ['dbtemplates', 'django_reclass']

LEONARDO_PUBLIC = True


class Config(AppConfig):
    name = 'django_reclass'
    verbose_name = "django-reclass"

    def ready(self):
        from .recievers import push_to_master

reclass = Reclass()
