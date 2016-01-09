
from django.conf.urls import include, patterns, url

from .views import ReclassView

urlpatterns = patterns('',
                       (r'^reclass/(?P<slug>.*)/(?P<path>.*)$',
                        ReclassView.as_view(), {}, 'get_reclass_with_path'),
                       (r'^reclass/(?P<path>.*)$',
                        ReclassView.as_view(), {}, 'get_reclass_path'),
                       (r'^reclass/(?P<slug>.*)/$',
                        ReclassView.as_view(), {}, 'get_reclass'),
                       )
