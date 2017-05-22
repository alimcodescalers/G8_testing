from g8os import resourcepool
from api_testing.utiles.utiles import Utiles


class GridPyclientBase(object):
    def __init__(self):
        self.utiles = Utiles()
        self.config = self.utiles.get_config_values()
        self.api_base_url = self.config['api_base_url']
        client = resourcepool.Client(self.api_base_url)
        self.api_client = client.api
        