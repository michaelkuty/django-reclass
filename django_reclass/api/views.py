
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from  django.db.models  import  Q

from django_reclass.models import Reclass, ReclassTemplate
from .serializers import ReclassSerializer, ReclassTemplateSerializer


def get_path(path):
    '''just append file extension'''

    if not path.endswith(('.yml', '.yaml')):

        return path + '.yml'

    return path


class ReclassView(APIView):

    """
    View to list all reclass nodes in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAdminUser,)

    def get(self, request, slug=None, path=None):
        """
        Return a reclass or reclass item.
        """
        if path and not slug:
            try:
                template = ReclassTemplate.objects.get(Q(path=path) | Q(label=path))
            except Exception as e:
                response = Response(
                    {'error': 'Path: {} not found.'.format(path)})
            else:
                response = Response(ReclassTemplateSerializer(template).data)

        if slug:

            try:
                reclass = Reclass.objects.get(name=slug)
            except Exception as e:
                response = Response({'error': str(e)})
            else:
                response = Response(ReclassSerializer(reclass).data)

        return response
