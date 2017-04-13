from random import randint
import uuid
from unittest import TestCase
from api_testing.utiles.utiles import Utiles
from api_testing.grid_apis.apis.nodes_apis import NodesAPI


class TestcasesBase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Utiles().get_config_values()
        self.lg = Utiles().logging
        self.nodes_api = NodesAPI()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_random_node(self, except_node=None):
        response = self.nodes_api.get_nodes()
        self.assertEqual(response.status_code, 200)
        nodes_list = [x['id'] for x in response.json()]
        if except_node != None and except_node in nodes_list:
            nodes_list = nodes_list.remove(except_node)
        node_id = nodes_list[randint(0, len(nodes_list)-1)]
        return node_id

    def random_string(self, size=10):
        return str(uuid.uuid4()).replace('-', '')[:size]

    def random_item(self, array):
        return array[randint(0, len(array)-1)]
