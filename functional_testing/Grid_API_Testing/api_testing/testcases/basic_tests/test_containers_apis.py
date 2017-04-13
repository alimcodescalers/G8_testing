import random
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.nodes_apis import NodesAPI
from api_testing.grid_apis.apis.containers_apis import ContainersAPI


class TestcontaineridAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        self.nodes_api = NodesAPI()
        self.base_test = TestcasesBase()
        self.containers_api = ContainersAPI()
        self.root_url = 'https://hub.gig.tech/maxux/ubuntu1604.flist'
        self.storage = 'ardb://hub.gig.tech:16379'
        super(TestcontaineridAPI, self).__init__(*args, **kwargs)

    def setUp(self):
        self.container_name = self.base_test.rand_str()
        self.hostname = self.base_test.rand_str()
        self.body = {"id": self.container_name, "hostname": self.hostname,
                     "flist": self.root_url, "hostNetworking": False}


    def test001_list_containers(self):
        """ GAT-001
        *GET:/node/{nodeid}/containers Expected: List of all running containers *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send get nodes/{nodeid}/containers api request.
        #. Compare results with golden value.
        """
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()

        self.lg.info('Send get nodes/{nodeid}/containers api request.')
        response = self.containers_api.get_containers(node_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('Compare results with golden value.')
        contaiers_list = response.json()
        #result :list from python client with contaires
        # self.assertEqual(len(contaiers_list), len(result),
        #                  'different length from apis than python client')
        # for container, i in enumerate(contaiers_list):
        #     for key in container.keys():
        #         self.assertEqual(container['key'], result[i]['key'])

        ################################
            # container_Id=container['id']
            # for client_container in result:
            #     if client_container[id]==container_Id:
            #         for key in container.keys():
            #             self.assertEqual(container['key'],client_container['key'])
            #
            #         break
        ###################################################

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
        response = self.containers_api.post_containers( node_id=node_id, body=self.body)
        self.assertEqual(response.status_code, 201)

        self.lg.info('Compare results with golden value.')

        self.lg.info('delete created container')
        response = self.containers_api.delete_containers_containerid(node_id, self.container_name)
        self.assertEqual(response.status_code, 204)
        self.lg.info('Make sure that it deleted ')
        response = self.containers_api.get_containers(node_id)
        containers_list = response.json()
        for container in containers_list:
            self.assertNotEqual(container['id'], self.container_name)

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
        container_id = self.base_test.get_random_container(node_id)

        self.lg.info('Send get nodes/{nodeid}/containers/containerid api request.')
        response = self.containers_api.get_containers_containerid(node_id, container_id)
        self.assertEqual(response.status_code, 200)

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
        response = self.containers_api.post_containers(node_id, self.body)
        self.assertEqual(response.status_code,200)
        self.lg.info('post:/node/{nodeid}/containers/containerid/stop.')
        response = self.containers_api.post_containers_containerid_stop(node_id, self.container_name)
        self.assertEqual(response.status_code,201)

        self.lg.info('Check that container stoped.')
        response = self.containers_api.get_containers_containerid(node_id, self.container_name)
        container_details = response.json()
        self.assertEqual(container_details['status'], 'halted')
        ##Check_from_python_client_too

        self.lg.info('post:/node/{nodeid}/containers/containerid/start.')
        response = self.containers_api.post_containers_containerid_start(node_id, self.container_name)
        self.assertEqual(response.status_code, 201)
        self.lg.info('Check that container running.')
        response = self.containers_api.get_containers_containerid(node_id, self.container_name)
        container_details = response.json()
        self.assertEqual(container_details['status'], 'running')
        #Check_from_python_client_too

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
        container_id = self.base_test.get_random_container(node_id)

        self.lg.info('Send get nodes/{nodeid}/containers/containerid/jobs api request.')
        response = self.containers_api.get_containers_containerid_jobs(node_id, container_id)
        self.assertEqual(response.status_code, 200)

        self.lg.info('Compare results with golden value.')
        running_jobs_list = response.json()
        #get result from python client
        # for job ,i in enumerate(running_jobs_list):
        #     for key in list(job.keys()):
        #         job['key'] == result[i][key]

    def test006_kill_all_running_jobs(self):
        """ GAT-006
        *get:/node/{nodeid}/containers/containerid/jobs Expected: get container details *

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
        container_id = self.base_test.get_random_container(node_id)

        self.lg.info('Send delete nodes/{nodeid}/containers/containerid/jobs api request.')
        response = self.containers_api.post_containers_containerid_jobs(node_id, container_id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json(), "Jobs killed successfully")

        self.lg.info('Check that all jobs in this container killed ')
        response = self.containers_api.get_containers_containerid_jobs(node_id, container_id)
        self.assertEqual(response.status_code, 200)
        jobs_list = response.json()
        self.assertEqual(len(jobs_list), 0)

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
        container_id = self.base_test.get_random_container(node_id)

        self.lg.info(' Choose one random job of list of running jobs in  container ')
        response = self.containers_api.get_containers_containerid_jobs(node_id=node_id,container_id=container_id)
        self.assertEqual(response.status_code, 200)
        jobs_list = response.json()
        job_id = jobs_list[random.randint(0, len(jobs_list))]['id']

        self.lg.info('Send get nodes/{nodeid}/containers/containerid/jobs/jobid api request.')
        response = self.containers_api.get_containers_containerid_jobs_jobid(node_id=node_id, container_id=container_id, job_id=job_id)
        self.assertEqual(response.status_code, 200)
        job_details = response.json()

        self.lg.info('Compare results with golden value.')
        #get result from python client
        #check values

    def test008_post_signal_job_in_container_details(self):
        """ GAT-008
        *get:/node/{nodeid}/containers/containerid/jobs/jobid Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Choose one random job of list of running jobs in  container.
        #. Send post nodes/{nodeid}/containers/containerid/jobs/jobid api request, should succeed

        """
        signal = random.randint(1, 30 )
        body = {'signal': signal}
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id = self.base_test.get_random_container(node_id)

        self.lg.info(' Choose one random job of list of running jobs in  container ')
        response = self.containers_api.get_containers_containerid_jobs(node_id=node_id,
                                                                       container_id=container_id)
        self.assertEqual(response.status_code, 200)
        jobs_list = response.json()
        job_id = jobs_list[random.randint(0, len(jobs_list))]['id']

        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/jobs/jobid api request.')
        response = self.containers_api.post_containers_containerid_jobs_jobid(node_id, container_id=container_id, job_id=job_id,body = body)
        self.assertEqual(response.status_code, 201)


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
        container_id = self.base_test.get_random_container(node_id)

        self.lg.info(' Choose one random job of list of running jobs in  container ')
        response = self.containers_api.get_containers_containerid_jobs(node_id=node_id,
                                                                       container_id=container_id)
        self.assertEqual(response.status_code, 200)
        jobs_list = response.json()
        job_id = jobs_list[random.randint(0, len(jobs_list))]['id']

        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/jobs/jobid api request.')
        response = self.containers_api.delete_containers_containerid_jobs_jobid(node_id=node_id,
                                                                                container_id=container_id, job_id=job_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Check that job delted from running jobs list.')
        response = self.containers_api.get_containers_containerid_jobs(node_id, container_id)
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
        container_id = self.base_test.get_random_container(node_id)
        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/ping api request.')
        response = self.containers_api.post_containers_containerid_ping(node_id, container_id )
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
        container_id = self.base_test.get_random_container(node_id)
        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/state api request.')
        response = self.containers_api.get_containers_containerid_state(node_id, container_id )
        self.assertEqual(response.status_code, 200)
        container_state = response.json()
        self.lg.info(' Compare results with golden value.')
        #result output from python client
        #for key in container_state.keys():
        #   self,assertEqual(container_state[key],result[key])

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
        container_id = self.base_test.get_random_container(node_id)
        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/state api request.')
        response = self.containers_api.get_containers_containerid_info(node_id, container_id )
        self.assertEqual(response.status_code, 200)
        container_info = response.json()
        self.lg.info(' Compare results with golden value.')
        #result output from python client
        #for key in container_info.keys():
        #   self,assertEqual(container_info[key],result[key])

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
        container_id = self.base_test.get_random_container(node_id)
        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/state api request.')
        response = self.containers_api.get_containers_containerid_processes(node_id, container_id )
        self.assertEqual(response.status_code, 200)
        processes = response.json()
        self.lg.info(' Compare results with golden value.')
        #result output from python client
        #for process, i in enumerate(processes):
            #for key in process.keys():
                # self,assertEqual(process[key],result[i][key])

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
        process_name = self.base_test.rand_str()
        body = {"name": process_name}
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id = self.base_test.get_random_container(node_id)
        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/processes api request.')
        response = self.containers_api.post_containers_containerid_processes(node_id=node_id, container_id=container_id, body=body)
        self.assertEqual(response.status_code, 200)
        processes = response.json()
        self.lg.info('Check that created process added to process list.')
        response = self.containers_api.get_containers_containerid_processes(node_id, container_id )
        self.assertEqual(response.status_code, 200)
        processes = response.json()
        self.assertIn(process_name, processes)
        self.lg.info(' Compare results with golden value.')


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
        container_id = self.base_test.get_random_container(node_id)

        self.lg.info('Choose one random process of list of processes')
        response = self.containers_api.get_containers_containerid_processes(node_id,
                                                                            container_id)
        self.assertEqual(response.status_code, 200)
        processes_list = response.json()
        process_id = processes_list[random.randint(0, len(processes_list))]['pid']

        self.lg.info('Send get  nodes/{nodeid}/containers/containerid/processes/processid api request.')
        response = self.containers_api.get_containers_containerid_processes_processid(node_id=node_id,
                                                                                       container_id=container_id, process_id=process_id)
        self.assertEqual(response.status_code, 200)
        process = response.json()

        self.lg.info(' Compare results with golden value.')
        #result output from python client
        #for key in process.keys():
            #self,assertEqual(process[key],result[i][key])



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
        container_id = self.base_test.get_random_container(node_id)

        self.lg.info('Choose one random process of list of processes')
        response = self.containers_api.get_containers_containerid_processes(node_id,
                                                                            container_id)
        self.assertEqual(response.status_code, 200)
        processes_list = response.json()
        process_id = processes_list[random.randint(0, len(processes_list))]['pid']

        self.lg.info('Send delete  nodes/{nodeid}/containers/containerid/processes/processid api request.')
        response = self.containers_api.delete_containers_containerid_processes_processid(node_id=node_id,
                                                                                       container_id=container_id, process_id=process_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Check that created process deleted from process list.')
        response = self.containers_api.get_containers_containerid_processes(node_id,
                                                                        container_id)
        self.assertEqual(response.status_code, 200)
        processes_list = response.json()
        for process in processes_list:
            self.assertNotEqual(process['pid'], process_id)

        self.lg.info(' Compare results with golden value.')

    def test017_post_signal_to_process_in_container(self):
        """ GAT-0017
        *get:/node/{nodeid}/containers/containerid/processes/processid Expected: get container details *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Choose one random conatainer of list of running containers.
        #. Choose one random process of list of running processes in  container.
        #. Send post nodes/{nodeid}/containers/containerid/processes/process  api request, should succeed

        """
        signal = random.randint(1, 30 )
        body = {'signal': signal}
        self.lg.info('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()
        self.lg.info('Choose one random container of list of running nodes')
        container_id = self.base_test.get_random_container(node_id)

        self.lg.info('Choose one random process of list of processes')
        response = self.containers_api.get_containers_containerid_processes(node_id,
                                                                            container_id)
        self.assertEqual(response.status_code, 200)
        processes_list = response.json()
        process_id = processes_list[random.randint(0, len(processes_list))]['pid']

        self.lg.info('Send post  nodes/{nodeid}/containers/containerid/processes/processid api request.')
        response = self.containers_api.post_containers_containerid_processes_processid(node_id,
                                  container_id=container_id, process_id=process_id,body = body)

        self.assertEqual(response.status_code, 201)
