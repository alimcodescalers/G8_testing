from random import randint
import uuid
from unittest import TestCase
from api_testing.utiles.utiles import Utiles
from api_testing.grid_apis.apis.nodes_apis import NodesAPI
from api_testing.grid_apis.apis.containers_apis import ContainersAPI
import json
import random



class TestcasesBase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Utiles().get_config_values()
        self.containter_api = ContainersAPI()
        self.lg = Utiles().logging
        self.nodes_api = NodesAPI()

    def setUp(self):
        pass

    def get_random_node(self):
        response = self.nodes_api.get_nodes()
        self.assertEqual(response.status_code, 200)
        nodes_list = response.json()

        node_id = nodes_list[random.randint(0, len(nodes_list)-1)]['id']
        return node_id

    def randomMAC(self):
        random_mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
        mac_address = ':'.join(map(lambda x: "%02x" %x, random_mac))
        return mac_address

    def get_random_container(self, node_id):
        response = self.containter_api.get_containers(node_id)
        self.assertEqual(response.status_code, 200)
        container_list = response.json()
        container_id = container_list[random.randint(0, len(container_list)-1)]['id']
        return container_id

    def rand_str(self):
        return str(uuid.uuid4()).replace('-', '')[1:10]

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
