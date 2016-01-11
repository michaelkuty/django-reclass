
from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
                       url(r'', include('django_reclass.api.urls')),
                       url(r'', include('django_reclass.graphql.urls')),
                       )
