import requests, time
from api_testing.utiles.utiles import Utiles


class GridAPIBase(object):
    def __init__(self):
        self.config = Utiles().get_config_values()
        self.api_base_url = self.config['api_base_url']
        self.headers = {'content-type': 'application/json'}
        self.requests = requests

    def request_api(self, method, api, body=''):
        if method not in ['post', 'get', 'put', 'delete']:
            raise NameError(" [*] %s method isn't handled" % method)

        api = self.build_api(api)

        if method == 'get':
            response = self.requests.get(url=api, headers=self.headers, data=body)
        elif method == 'post':
            response = self.requests.post(url=api, headers=self.headers, data=body)
        elif method == 'put':
            response = self.requests.put(url=api, headers=self.headers, data=body)
        elif method == 'delete':
            response = self.requests.delete(url=api, headers=self.headers, data=body)

        return response

    def build_api(self, api):
        api_path = self.api_base_url
        if api_path[-1] != '/':
            api_path += '/'

        for item in api:
            api_path += item + '/'

        return api_path[:-1]
