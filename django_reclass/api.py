import requests
import yaml
from django.conf import settings
from horizon_contrib.api import Manager


class MasterClient(Manager):

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
            data=params,
            headers=headers)

        return response

    def process_headers(self, headers, request):
        '''make raw request'''
        headers["X-Authtoken"] = getattr(
            settings, "SALT_MASTER_KEY", "assadssdASASDsadssd687465")
        return headers

    def set_api(self):
        self.api = '%s://%s:%s/' % (
            getattr(settings, "SALT_MASTER_PROTOCOL", "http"),
            getattr(settings, "SALT_MASTER_HOST", "185.22.98.86"),
            getattr(settings, "SALT_MASTER_PORT", 5000))
