import os, re, requests, uuid, logging, time, configparser
from subprocess import Popen, PIPE
from xml.etree.ElementTree import Element, SubElement, tostring
from bs4 import BeautifulSoup
from random import randint
from unittest import TestCase
from api_testing.utiles.utiles import Utiles
from api_testing.grid_apis.apis.nodes_apis import NodesAPI


class TestcasesBase(TestCase):
    def __init__(self):
        super(TestcasesBase, self).__init__()
        self.config = Utiles().get_config_values()
        self.nodes_api = NodesAPI()

    def setUp(self):
        pass

    def get_random_node(self):
        status_code, response_content = self.nodes_api.get_node()
        self.assertEqual(status_code, 200)
        nodes_list = response_content
        node_id = nodes_list[random.randint(0, len(nodes_list)-1)]
        return node_id

    def tearDown(self):
        pass
