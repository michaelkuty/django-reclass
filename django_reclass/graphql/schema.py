
import graphene
from django.db.models import Q
from graphene.contrib.django import (DjangoConnection, DjangoNode,
                                     DjangoObjectType)

from ..api.views import get_path
from ..models import Reclass as Reclass
from ..models import ReclassTemplate

schema = graphene.Schema(name='Reclass Schema')


class Connection(DjangoConnection):
    total_count = graphene.Int()

    def resolve_total_count(self, args, info):
        return len(self.get_connection_data())


class ReclassTemplateType(DjangoObjectType):

    content = graphene.Field(graphene.String())
    parameters = graphene.Field(graphene.String())
    applications = graphene.String().List
    classes = graphene.String().List

    def resolve_content(self, args, info):
        return self.instance.content

    def resolve_parameters(self, args, info):
        return self.instance.parameters

    def resolve_applications(self, args, info):
        return self.instance.applications

    def resolve_classes(self, args, info):
        return self.instance.classes

    class Meta:
        model = ReclassTemplate


class ReclassType(DjangoObjectType):

    '''Basic Reclass Type'''

    nodes = graphene.Field(graphene.List(ReclassTemplateType))
    classes = graphene.Field(graphene.List(ReclassTemplateType))

    def resolve_nodes(self, args, info):
        return self.instance.nodes.all()

    def resolve_classes(self, args, info):
        return self.instance.classes.all()

    class Meta:
        model = Reclass


class Query(graphene.ObjectType):

    """example queries::

        query {
          getReclass(reclass: "reclass") {
            verboseName, nodes {label, classes, applications}
          }
        }

        query {
          getNode(path: ".ubuntu1404.vanilla.robotice.cz") {
            label, path, rendered
          }
        }
    """

    all_reclass = graphene.List(ReclassType)
    get_reclass = graphene.Field(ReclassType,
                                 id=graphene.String(),
                                 reclass=graphene.String())
    get_node = graphene.Field(ReclassTemplateType,
                              id=graphene.String(),
                              path=graphene.String())

    def resolve_get_node(self, args, info):
        """TODO: get by id"""
        path = args.get('path', None)
        return ReclassTemplate.objects.get(
            Q(path=path) | Q(path=get_path(path)) | Q(label=path) | Q(label=path + '.init'))

    def resolve_get_reclass(self, args, info):
        """TODO: get by id"""
        name = args.get('reclass', None)
        return Reclass.objects.get(name=name)

    def resolve_viewer(self, *args, **kwargs):
        return self


class AddClass(graphene.Mutation):
    '''
    .. code-block:: json

        mutation myFirstMutation {
          addClass(node:"workshop.cfg01.workshop-os-oc.usr02.vpc.cloudlab.cz", name: "test.whatever") {
            node, name
          }
        }

    '''

    class Input:
        name = graphene.String()
        node = graphene.String()

    name = graphene.String()
    node = graphene.String()

    @classmethod
    def mutate(cls, query, args, info):
        path = args.get('node', None)
        name = args.get('name', None)
        template = ReclassTemplate.objects.get(
            Q(path=path) | Q(path=get_path(path)) | Q(label=path) | Q(label=path + '.init'))

        template.add_class(name)

        return AddClass(name=name, node=path)


class ReclassMutations(graphene.ObjectType):
    add_class = graphene.Field(AddClass)

schema.query = Query
schema.mutation = ReclassMutations
