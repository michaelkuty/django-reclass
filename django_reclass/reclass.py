from jinja2 import Environment
from dbtemplates.models import Template
from .api import MasterClient


class Reclass(MasterClient):

    '''Object for generating and delivering metadata to reclass'''

    env = Environment()

    def pull(self, path):
        '''Get data from remote Salt Master'''
        return self.request(path, method='GET')

    def push(self, path, data):
        '''Send data to remote Salt Master'''
        return self.request(path, params=data, method='POST')

    def render_and_push(self, path, data=None, name=None, context={}):
        '''Render and Push data to remote Salt Master'''
        self.request(path, params=(data or self.render(
            name, context, send=False)), method='POST')

    def render(self, name=None, template=None, context={},
               send=False, path=None):
        ''''Render reclass meta from jinja2 templates.

        if send flag is True will be pushed to master
        '''

        reclass_template = template or Template.objects.get(name=name)

        # Maybe cache or save local ?
        meta = self.env.from_string(
            reclass_template.content).render(context)

        if send and path:
            self.push(path=path, data=meta)

        return meta
