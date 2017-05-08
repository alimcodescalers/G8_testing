from random import randint
import uuid
from unittest import TestCase
from api_testing.utiles.utiles import Utiles
from api_testing.grid_apis.apis.nodes_apis import NodesAPI
from api_testing.grid_apis.apis.containers_apis import ContainersAPI
import random
import requests
import time


class TestcasesBase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.utiles = Utiles()
        self.config = self.utiles.get_config_values()
        self.nodes = self.update_nodes_info()
        self.containters_api = ContainersAPI()
        self.lg = self.utiles.logging
        self.nodes_api = NodesAPI()
        self.session = requests.Session()
        self.zerotier_token = self.config['zerotier_token']
        self.session.headers['Authorization'] = 'Bearer {}'.format(self.zerotier_token)
        self.createdcontainer=[]

    def setUp(self):
        pass

    def randomMAC(self):
        random_mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
        mac_address = ':'.join(map(lambda x: "%02x" % x, random_mac))
        return mac_address

    def rand_str(self):
        return str(uuid.uuid4()).replace('-', '')[1:10]

    def tearDown(self):
        pass

    def get_random_node(self, except_node=None):
        response = self.nodes_api.get_nodes()
        self.assertEqual(response.status_code, 200)
        nodes_list = [x['id'] for x in response.json()]
        if except_node is not None and except_node in nodes_list:
            nodes_list = nodes_list.remove(except_node)

        tmp = []
        for node in nodes_list:
            if node['status'] == 'running':
                tmp.append(node)
        nodes_list = list(tmp)
        if len(nodes_list) > 0:
            node_id = nodes_list[randint(0, len(nodes_list)-1)]
            return node_id

    def random_string(self, size=10):
        return str(uuid.uuid4()).replace('-', '')[:size]

    def random_item(self, array):
        return array[randint(0, len(array)-1)]

    def getZtNetworkID(self):
        url = 'https://my.zerotier.com/api/network'
        r = self.session.get(url)
        if r.status_code == 200:
            for item in r.json():
                if item['type'] == 'Network':
                    return item['id']
            else:
                self.lg('can\'t find network id')
                return False
        else:
            self.lg('can\'t connect to zerotier, {}:{}'.format(r.status_code, r.content))
            return False

    def wait_for_container_status(self, status, func, timeout=100, **kwargs):
        resource = func(**kwargs)
        if resource.status_code != 200:
            return False
        resource = resource.json()
        for _ in range(timeout):
            if resource['status'] == status:
                return True
            time.sleep(1)
            resource = func(**kwargs)  # get resource
            resource = resource.json()
        return False

    def get_random_container(self, node_id):
        container_name = self.rand_str()
        hostname = self.rand_str()
        container_body = {"name": container_name, "hostname": hostname, "flist": self.root_url,
                          "hostNetworking": False, "initProcesses": [], "filesystems": [],
                          "ports": [], "storage": "ardb://hub.gig.tech:16379"
                          }
        response = self.containers_api.get_containers(node_id)
        self.assertEqual(response.status_code, 200)
        container_list = response.json()
        counter = len(container_list)
        while (counter != 0) and (len(container_list) != 0):
            container_name = container_list[random.randint(0, len(container_list)-1)]['name']
            response = self.containers_api.get_containers_containerid(node_id=node_id,container_id=container_name)
            container=response.json()
            if container['status']=='running':
                return container_name

            else:
                counter = counter-1
        else:
            response = self.containers_api.post_containers(node_id=node_id, body=container_body)
            self.assertEqual(response.status_code, 201)
            if not self.wait_for_container_status('running', self.containers_api.get_containers_containerid,
                                                          node_id=node_id, container_id=container_name):
                return False
            else:
                self.createdcontainer.append({"node": node_id, "container": container_name})
                return container_name
              
              
    def get_node_physical_ip(self, node_id):
            resonse = self.nodes_api.get_nodes_nodeid_nics(node_id)
            self.assertEqual(resonse.status_code, 200)

            nic = {}
            for data in resonse.json():
                if data['name'] == "enp0s20f0":
                    nic['ip'] = data['addrs'][0].split('/')[0]
                    nic['id'] = data['hardwareaddr'].replace(':', '')
                    return nic

    def update_nodes_info(self):
        nodes_info = []
        response = self.nodes_api.get_nodes()
        self.assertEqual(response.status_code, 200)
        for node in response.json():
            if node['status'] == 'running':
                nodes_info.append(self.get_node_physical_ip(node['id']))

        return nodes_info
