import requests
from django.conf import settings
from horizon_contrib.api import Manager


class MasterClient(Manager):

    def do_request(self, path, method="GET", params={}, headers={}):
        '''make raw request'''
        headers["Content-Type"] = "application/json"
        response = requests.post(
            path,
            data=params,
            headers=headers)
        return response

    def set_api(self):
        self.api = '%s://%s:%s/' % (
            getattr(settings, "MASTER_PROTOCOL", "http"),
            getattr(settings, "MASTER_HOST", "185.22.98.86"),
            getattr(settings, "MASTER_PORT", 5000))
