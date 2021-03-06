import requests
import yaml
from django.conf import settings
from horizon_contrib.api import Manager
import json


class MasterClient(Manager):

    def __init__(self, host=None, port=None, *args, **kwargs):
        super(MasterClient, self).__init__(*args, **kwargs)

        if host or port:
            self.set_api(host, port)

    def do_request(self, path, method="GET", params={}, headers={}):
        '''make raw request'''
        headers["Content-Type"] = "application/json"

        if method == "GET":
            raw_response = requests.get(
                path,
                headers=headers)
            return yaml.load(raw_response)

        response = requests.post(
            path,
            data=json.dumps(params) if 'master' in path else params,
            headers=headers)

        return response

    def process_headers(self, headers, request):
        '''make raw request'''
        headers["X-Authtoken"] = getattr(
            settings, "SALT_MASTER_KEY", "assadssdASASDsadssd687465")
        return headers

    def set_api(self, host=None, port=None):
        self.api = '%s://%s:%s/' % (
            getattr(settings, "SALT_MASTER_PROTOCOL", "http"),
            host or getattr(settings, "SALT_MASTER_HOST", "185.22.98.86"),
            port or getattr(settings, "SALT_MASTER_PORT", 5000))

    def update(self, clients=None, cmd='salt \"{clients}\" state.highstate'):
        '''call salt {clients} state.highstate from salt master'''
        return self.request(
            'master/',
            params={
                'cmd': cmd.format(**{'clients': clients or '*'}),
            }, method='POST')
