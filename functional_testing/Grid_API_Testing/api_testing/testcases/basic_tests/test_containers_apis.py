import random
import time
import unittest
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.nodes_apis import NodesAPI
from api_testing.grid_apis.apis.containers_apis import ContainersAPI


class TestcontaineridAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        self.nodes_api = NodesAPI()
        self.base_test = TestcasesBase()
        self.containers_api = ContainersAPI()
        self.root_url = 'https://hub.gig.tech/deboeckj/flist-lede-17.01.0-r3205-59508e3-x86-64-generic-rootfs.flist' # until the timeout issue is fixes 'https://hub.gig.tech/maxux/ubuntu1604.flist'
        self.storage = 'ardb://hub.gig.tech:16379'
        super(TestcontaineridAPI, self).__init__(*args, **kwargs)

    def setUp(self):
        self.container_name = self.base_test.rand_str()
        self.hostname = self.base_test.rand_str()
        self.process_body = {'name': 'yes'}
        self.container_body = {"id": self.container_name, "hostname": self.hostname, "flist": self.root_url,
                               "hostNetworking": False, "initProcesses": [], "filesystems": [],
                               "ports": [], "storage": "ardb://hub.gig.tech:16379",
                               "nics": [{'type': 'default',
                                         'id': '', 'config': {'dhcp': False,
                                                              'gateway': '',
                                                              'cidr': '',
                                                              'dns': None}}]}

    def tearDown(self):
        response = self.nodes_api.get_nodes()
        self.assertEqual(response.status_code, 200)
        for node in response.json():
            response = self.containers_api.get_containers(node['id'])
            self.assertEqual(response.status_code, 200)
            for container in response.json():
                self.containers_api.delete_containers_containerid(node['id'], container['id'])

    def get_random_container(self, node_id):
        response = self.containter_api.get_containers(node_id)
        self.assertEqual(response.status_code, 200)
        container_list = response.json()
        status = 'halted'
        counter = len(container_list)
        container_name = None
        if not len(container_list):
            container_name = self.base_test.rand_str()
            hostname = self.base_test.rand_str()
            container_body = {"id": container_name, "hostname": hostname, "flist": self.root_url,
                              "hostNetworking": False, "initProcesses": [], "filesystems": [],
                              "ports": [], "storage": "ardb://hub.gig.tech:16379",
                              "nics": [{'type': 'default',
                                        'id': '', 'config': {'dhcp': False,
                                                             'gateway': '',
                                                             'cidr': '',
                                                             'dns': None}}]}
            response = self.containter_api.post_containers(node_id=node_id, body=container_body)
            self.assertEqual(response.status_code, 201)
            time.sleep(10)
            counter = 1
        while status != 'running' and counter != 0:
            if not container_name:
                container_name = container_list[random.randint(0, len(container_list)-1)]['id']
            response = self.containers_api.get_containers_containerid(node_id, container_name)
            self.assertEqual(response.status_code, 200)
            container_details = response.json()
            status = container_details['status']
            container_id = container_details['containerid']
            if status != 'running':
                counter -= counter
        return container_id, container_name

    def test001_list_containers(self):
        """ GAT-001
        *GET:/node/{nodeid}/containers Expected: List of all running containers *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send get nodes/{nodeid}/containers api request.
        #. Compare results with golden value.
        """
        containers_id = []
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()

        self.lg.info('Send get nodes/{nodeid}/containers api request.')
        response = self.containers_api.get_containers(node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('Compare results with golden value.')
        containers_list = response.json()
        for container in containers_list:
            response = self.containers_api.get_containers_containerid(node_id, container['id'])
            self.assertEqual(response.status_code, 200)
            data = response.json()
            if data['containerid']:
                containers_id.append(str(data['containerid']))
        containers_id.sort()
        self.assertEqual(sorted(list(self.g8core.client.container.list().keys())), containers_id)



    def test002_create_containers(self):
        """ GAT-002
        *post:/node/{nodeid}/containers Expected: create container then delete it *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send post nodes/{nodeid}/containers api request.
        #. Compare results with golden value.
        #. Delete ctreated container,should succeed
        #. make sure that it deleted .
        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Send post nodes/{nodeid}/containers api request.')
        response = self.containers_api.post_containers(node_id=node_id, body=self.container_body)
        self.assertEqual(response.status_code, 201)

        self.lg.info('Compare results with golden value.')
        self.assertEqual(response.headers['Location'], "/nodes/%s/containers/%s" % (node_id, self.container_name))
        time.sleep(30)

        response = self.containers_api.get_containers_containerid(node_id, self.container_name)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        for key, item in response_data.items():
            if key == 'status':
                self.assertEqual(response_data[key], 'running')
                continue
            elif key == 'containerid':
                continue
            elif key == 'initprocesses':
                self.assertEqual(response_data[key], self.container_body['initProcesses'])
                continue
            self.assertEqual(response_data[key], self.container_body[key])

        # self.lg.info('delete created container')
        # response = self.containers_api.delete_containers_containerid(node_id, self.container_name)
        # self.assertEqual(response.status_code, 204)
        # self.lg.info('Make sure that it deleted ')
        # response = self.containers_api.get_containers(node_id)
        # containers_list = response.json()
        # for container in containers_list:
        #     self.assertNotEqual(container['id'], self.container_name)

    def test003_get_container_details(self):
        """ GAT-003
        *get:/node/{nodeid}/containers/containerid Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Get:/node/{nodeid}/containers/containerid
        #. Compare results with golden value.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose random container of list of running nodes')
        _, container_name = self.get_random_container(node_id)

        self.lg.info('Send get nodes/{nodeid}/containers/containerid api request.')
        response = self.containers_api.get_containers_containerid(node_id, container_name)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        container_id = data['containerid']
        golden_data = self.g8core.client.container.list().get(str(container_id), None)
        if not golden_data:
            return
        golden_value = golden_data['container']
        golden_nics = [{i: nic[i] for i in nic if i != 'hwaddr'} for nic in golden_value['arguments']['nics']]
        golden_ports = ['%s:%s' % (key, value) for key, value in golden_value['arguments']['port'].items()]
        self.assertEqual(data['nics'], golden_nics)
        self.assertEqual(data['ports'], golden_ports)
        self.assertEqual(data['hostNetworking'], golden_value['arguments']['host_network'])
        self.assertEqual(data['hostname'], golden_value['arguments']['hostname'])
        self.assertEqual(data['flist'], golden_value['arguments']['root'])
        self.assertEqual(data['storage'], golden_value['arguments']['storage'])

        self.lg.info('Compare results with golden value.')

    def test004_stop_and_start_container(self):
        """ GAT-004
        *post:/node/{nodeid}/containers/containerid/start Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Create container.
        #. post:/node/{nodeid}/containers/containerid/stop.
        #. Check that container stpoed .
        #. Post:/node/{nodeid}/containers/containerid/start.
        #. Check that container running .

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Create container ')
        response = self.containers_api.post_containers(node_id, self.container_body)
        self.assertEqual(response.status_code, 201)
        data = self.containers_api.get_containers_containerid(node_id, self.container_name).json()
        time.sleep(15)
        container_id = data['containerid']

        self.lg.info('post:/node/{nodeid}/containers/containerid/stop.')
        response = self.containers_api.post_containers_containerid_stop(node_id, self.container_name)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Check that container stoped.')
        response = self.containers_api.get_containers_containerid(node_id, self.container_name)
        self.assertEqual(response.status_code, 200)
        container_details = response.json()

        self.assertEqual(container_details['status'], 'halted')
        self.assertTrue(str(container_id) not in self.g8core.client.container.list().keys())

        self.lg.info('post:/node/{nodeid}/containers/containerid/start.')
        response = self.containers_api.post_containers_containerid_start(node_id, self.container_name)
        self.assertEqual(response.status_code, 201)

        self.lg.info('Check that container running.')
        response = self.containers_api.get_containers_containerid(node_id, self.container_name)
        self.assertEqual(response.status_code, 200)
        container_details = response.json()
        self.assertEqual(container_details['status'], 'running')
        container_id = container_details['containerid']
        self.assertTrue(str(container_id) in self.g8core.client.container.list().keys())


    def test005_get_running_jobs(self):
        """ GAT-005
        *get:/node/{nodeid}/containers/containerid/jobs Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Get:/node/{nodeid}/containers/containerid/jobs
        #. Compare results with golden value.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)
        self.lg.info('Send get nodes/{nodeid}/containers/containerid/jobs api request.')
        response = self.containers_api.get_containers_containerid_jobs(node_id, container_name)
        self.assertEqual(response.status_code, 200)

        self.lg.info('Compare results with golden value.')
        running_jobs_list = response.json()
        container = self.g8core.client.container.client(container_id)
        container_data = container.job.list()
        golden_values = []

        # cannot compare directly as the job.list is considered a job and has a different id everytime is is called
        for i, golden_value in enumerate(container_data[:]):
            if golden_value.get('command', "") == 'job.list':
                container_data.pop(i)
                continue
            golden_values.append((golden_value['cmd']['id'], golden_value['starttime']))
        golden_values = set(golden_values)
        api_jobs = set([(job['id'], job['startTime'])for job in running_jobs_list])
        self.assertEqual(len(golden_values.difference(api_jobs)), 1)

    def test006_kill_all_running_jobs(self):
        """ GAT-006
        *get:/node/{nodeid}/containers/containerid/jobs Expected: get container details*

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. delete :/node/{nodeid}/containers/containerid/jobs.
        #. Check that all jobs in this container killed.
        #. Compare results with golden value.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info('Spawn multiple jobs.')
        for i in range(0, 3):
            response = self.containers_api.post_containers_containerid_processes(node_id, container_name, self.process_body)
            self.assertEqual(response.status_code, 202)

        self.lg.info('Send delete nodes/{nodeid}/containers/containerid/jobs api request.')
        response = self.containers_api.delete_containers_containerid_jobs(node_id, container_name)
        self.assertEqual(response.status_code, 204)
        time.sleep(5)

        self.lg.info('Check that all jobs in this container killed ')
        response = self.containers_api.get_containers_containerid_jobs(node_id, container_name)
        self.assertEqual(response.status_code, 200)
        jobs_list = response.json()
        container = self.g8core.client.container.client(container_id)
        self.assertEqual(len(jobs_list), 1)
        self.assertEqual(len(container.job.list()), 1)

        self.lg.info('Compare results with golden value.')

    def test007_get_job_in_container_details(self):
        """ GAT-007
        *get:/node/{nodeid}/containers/containerid/jobs/jobid Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Choose one random job of list of running jobs in  container.
        #. Send get nodes/{nodeid}/containers/containerid/jobs/jobid api request
        #. Compare results with golden value.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info(' spawn job in container ')
        response = self.containers_api.post_containers_containerid_processes(node_id, container_name, self.process_body)
        self.assertEqual(response.status_code, 202)
        time.sleep(10)
        job_id = response.headers['Location'].split('/')[6]


        self.lg.info('Send get nodes/{nodeid}/containers/containerid/jobs/jobid api request.')
        response = self.containers_api.get_containers_containerid_jobs_jobid(node_id, container_name, job_id)
        self.assertEqual(response.status_code, 200)
        job_details = response.json()

        #get result from python client
        self.lg.info('Compare results with golden value.')
        container = self.g8core.client.container.client(container_id)
        golden_value = container.job.list(job_id)[0]
        self.assertEqual(golden_value['cmd']['command'], job_details['name'])
        self.assertEqual(golden_value['cmd']['id'], job_details['id'])
        self.assertEqual(golden_value['starttime'], job_details['startTime'])

        response = self.containers_api.delete_containers_containerid_jobs_jobid(node_id, container_name, job_id)
        self.assertEqual(response.status_code, 204)

    def test008_post_signal_job_in_container_details(self):
        """ GAT-008
        *get:/node/{nodeid}/containers/containerid/jobs/jobid Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Choose one random job of list of running jobs in  container.
        #. Send post nodes/{nodeid}/containers/containerid/jobs/jobid api request, should succeed

        """
        signal = random.randint(1, 30)
        body = {'signal': signal}
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info(' spawn job in container ')
        response = self.containers_api.post_containers_containerid_processes(node_id, container_name, self.process_body)
        self.assertEqual(response.status_code, 202)
        job_id = response.headers['Location'].split('/')[6]

        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/jobs/jobid api request.')
        response = self.containers_api.post_containers_containerid_jobs_jobid(node_id, container_name, job_id, body)
        self.assertEqual(response.status_code, 204)
        # needs to be compared to golden value
        # TODO:

    def test009_kill_specific_job(self):
        """ GAT-009
        *get:/node/{nodeid}/containers/containerid/jobs/jobid Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Choose one random job of list of running jobs in  container.
        #. Send delete nodes/{nodeid}/containers/containerid/jobs/jobid api request, should succeed
        #. Check that job delted from running jobs list.
        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info(' spawn job in container ')
        response = self.containers_api.post_containers_containerid_processes(node_id, container_name, self.process_body)
        self.assertEqual(response.status_code, 202)
        time.sleep(15)
        job_id = response.headers['Location'].split('/')[6]


        self.lg.info('Send delete  nodes/{nodeid}/containers/containerid/jobs/jobid api request.')
        response = self.containers_api.delete_containers_containerid_jobs_jobid(node_id, container_name, job_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Check that job delted from running jobs list.')
        response = self.containers_api.get_containers_containerid_jobs(node_id, container_name)
        self.assertEqual(response.status_code, 200)
        running_jobs_list = response.json()
        for job in running_jobs_list:
            self.assertNotEqual(job['id'], job_id)

    def test010_post_ping_to_container(self):
        """ GAT-010
        *get:/node/{nodeid}/containers/containerid/ping *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Send post nodes/{nodeid}/containers/containerid/post request.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        _, container_name = self.get_random_container(node_id)
        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/ping api request.')
        response = self.containers_api.post_containers_containerid_ping(node_id, container_name)
        self.assertEqual(response.status_code, 200)

    def test011_get_state_of_container(self):
        """ GAT-011
        *get:/node/{nodeid}/containers/containerid/state *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Send get nodes/{nodeid}/containers/containerid/state request.
        #. Compare results with golden value.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info('Send GET  nodes/{nodeid}/containers/containerid/state api request.')
        response = self.containers_api.get_containers_containerid_state(node_id, container_name)
        self.assertEqual(response.status_code, 200)

        self.lg.info(' Compare results with golden value.')
        container_state = response.json()
        golden_value = self.g8core.client.container.list()[str(container_id)]
        self.assertAlmostEqual(golden_value['rss'], container_state['rss'], delta=1000000)
        self.assertEqual(golden_value['swap'], container_state['swap'])
        self.assertAlmostEqual(golden_value['vms'], container_state['vms'], delta=10000000)

    def test012_get_info_of_container_os(self):
        """ GAT-012
        *get:/node/{nodeid}/containers/containerid/info *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Send get nodes/{nodeid}/containers/containerid/info request.
        #. Compare results with golden value.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/state api request.')
        response = self.containers_api.get_containers_containerid_info(node_id, container_name)
        self.assertEqual(response.status_code, 200)

        self.lg.info(' Compare results with golden value.')
        container_info = response.json()
        container = self.g8core.client.container.client(container_id)
        golden_value = container.info.os()
        self.assertAlmostEqual(golden_value.pop('uptime'), container_info.pop('uptime'), delta=20)
        self.assertEqual(golden_value, container_info)


    def test013_get_running_processes_in_container(self):
        """ GAT-013
        *get:/node/{nodeid}/containers/containerid/processes *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Send get nodes/{nodeid}/containers/containerid/processes request.
        #. Compare results with golden value.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/state api request.')
        response = self.containers_api.get_containers_containerid_processes(node_id, container_name)
        self.assertEqual(response.status_code, 200)
        processes = response.json()
        container = self.g8core.client.container.client(container_id)
        golden_values = container.process.list()

        # compare to golden value
        self.lg.info(' Compare results with golden value.')

        processes.sort(key=lambda d: d['pid'])
        golden_values.sort(key=lambda d: d['pid'])

        for i, p in enumerate(processes):
            self.assertEqual(p['cmdline'], golden_values[i]['cmdline'])
            self.assertEqual(p['pid'], golden_values[i]['pid'])
            self.assertEqual(p['rss'], golden_values[i]['rss'])
            self.assertEqual(p['swap'], golden_values[i]['swap'])
            self.assertEqual(p['vms'], golden_values[i]['vms'])

    def test014_post_create_new_processes_in_container(self):
        """ GAT-014
        *post:/node/{nodeid}/containers/containerid/processes *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Send post nodes/{nodeid}/containers/containerid/processes request.\
        #. Check that created process added to process list.
        #. Compare results with golden value.

        """
        process_name = self.process_body['name']
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/processes api request.')
        response = self.containers_api.post_containers_containerid_processes(node_id, container_name, self.process_body)
        self.assertEqual(response.status_code, 202)
        time.sleep(5)

        self.lg.info('Check that created process added to process list.')
        response = self.containers_api.get_containers_containerid_processes(node_id, container_name)
        self.assertEqual(response.status_code, 200)
        processes = [p['cmdline'] for p in response.json()]
        self.assertIn(process_name, processes)

        self.lg.info(' Compare results with golden value.')
        container = self.g8core.client.container.client(container_id)
        golden_values = [p['cmdline'] for p in container.process.list()]
        self.assertIn(process_name, golden_values)

    def test015_get_process_details_in_container(self):
        """ GAT-015
        *post:/node/{nodeid}/containers/containerid/processes/processid *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Choose one random process of list of process.
        #. Send get nodes/{nodeid}/containers/containerid/processes/processid request.
        #. Compare results with golden value.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()

        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info('Choose one random process of list of processes')
        response = self.containers_api.post_containers_containerid_processes(node_id, container_name, self.process_body)
        self.assertEqual(response.status_code, 202)
        time.sleep(5)
        response = self.containers_api.get_containers_containerid_processes(node_id, container_name)
        self.assertEqual(response.status_code, 200)
        processes_list = response.json()
        process_id = None
        while not process_id or process_id == 1:
            random_number = random.randint(0, len(processes_list)-1)
            process_id = processes_list[random_number]['pid']

        self.lg.info('Send get  nodes/{nodeid}/containers/containerid/processes/processid api request.')
        response = self.containers_api.get_containers_containerid_processes_processid(node_id, container_name,
                                                                                      str(process_id))
        self.assertEqual(response.status_code, 200)
        process = response.json()
        container = self.g8core.client.container.client(container_id)
        golden_value = container.process.list(process_id)[0]
        self.lg.info(' Compare results with golden value.')
        self.assertAlmostEqual(golden_value.pop('rss'), process.pop('rss'), delta=1000000)
        self.assertAlmostEqual(golden_value.pop('vms'), process.pop('vms'), delta=10000000)

        for key in process:
            if key == 'cpu':
                continue
            self.assertEqual(golden_value[key], process[key])

    def test016_delete_process_in_container(self):
        """ GAT-0016
        *post:/node/{nodeid}/containers/containerid/processes/processid *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Choose one random process of list of process.
        #. Send delete nodes/{nodeid}/containers/containerid/processes/processid request.
        #. Check that created process deleted from process list.
        #. Compare results with golden value.

        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()

        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        self.lg.info('Choose one random process of list of processes')
        response = self.containers_api.post_containers_containerid_processes(node_id, container_name, self.process_body)
        self.assertEqual(response.status_code, 202)
        time.sleep(10)
        response = self.containers_api.get_containers_containerid_processes(node_id, container_name)
        self.assertEqual(response.status_code, 200)
        processes_list = response.json()
        process_id = None
        while not process_id or process_id == 1:
            random_number = random.randint(0, len(processes_list)-1)
            process_id = processes_list[random_number]['pid']


        self.lg.info('Send delete  nodes/{nodeid}/containers/containerid/processes/processid api request.')
        response = self.containers_api.delete_containers_containerid_processes_processid(node_id, container_name,
                                                                                         str(process_id))
        self.assertEqual(response.status_code, 204)

        self.lg.info('Check that created process deleted from process list.')
        response = self.containers_api.get_containers_containerid_processes(node_id, container_name)
        self.assertEqual(response.status_code, 200)
        processes_list = response.json()
        for process in processes_list:
            self.assertNotEqual(process['pid'], process_id)

        self.lg.info(' Compare results with golden value.')
        container = self.g8core.client.container.client(container_id)
        golden_value = container.process.list()
        for process in golden_value:
            self.assertNotEqual(process['pid'], process_id)

    def test017_post_signal_to_process_in_container(self):
        """ GAT-0017
        *get:/node/{nodeid}/containers/containerid/processes/processid Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Choose one random process of list of running processes in  container.
        #. Send post nodes/{nodeid}/containers/containerid/processes/process  api request, should succeed

        """
        signal = random.randint(1, 30)
        body = {'signal': signal}
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id, container_name = self.get_random_container(node_id)

        response = self.containers_api.post_containers_containerid_processes(node_id, container_name, self.process_body)
        self.assertEqual(response.status_code, 202)

        self.lg.info('Choose one random process of list of processes')
        response = self.containers_api.get_containers_containerid_processes(node_id, container_name)
        self.assertEqual(response.status_code, 200)
        processes_list = response.json()
        process_id = None
        while not process_id or process_id == 1:
            random_number = random.randint(0, len(processes_list)-1)
            process_id = processes_list[random_number]['pid']

        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/processes/processid api request.')
        response = self.containers_api.post_containers_containerid_processes_processid(node_id, container_name,
                                                                                       str(process_id), body)
        self.assertEqual(response.status_code, 204)
        # TODO: compare to golden value
