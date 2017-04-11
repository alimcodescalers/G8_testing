import random
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.nodes_apis import NodesAPI


class TestNodeidAPI(TestcasesBase):
    def __init__(self):
        super(TestNodeidAPI, self).__init__()
        self.nodes_api = NodesAPI()
        self.base_test = TestcasesBase()

    def test001_list_nodes(self):
        """ GAT-001
        *GET:/node/ Expected: List of all nodes*

        **Test Scenario:**

        #. Send get nodes api request.
        #. Compare results with golden value.
        """
        response = self.nodes_api.get_nodes()
        self.assertEqual(response.status_code, 200)

    def test002_get_node_details(self):
        """ GAT-002
        *GET:/nodes/{nodeid} - Expected: id, status, hostname*

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send get nodes/{nodeid} api request.
        #. Compare results with golden value.
        """
        node_id=self.base_test.get_random_node()
        response = self.nodes_api.get_node_nodeid(node_id=node_id)
        self.assertEqual(response.status_code, 200)

    def test003_list_jobs(self):
        """ GAT-003
        *GET:/nodes/{nodeid}/jobs - Expected: job list items*

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send get /nodes/{nodeid}/jobs api request.
        #. Compare results with golden value.
        """
        node_id=self.base_test.get_random_node()
        response = response.self.nodes_api.get_running_jobs(node_id=node_id)
        self.assertEqual(response.status_code, 200)

    def test004_kill_jobs(self):
        """ GAT-004
        *DELETE:/nodes/{nodeid}/jobs *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Send get /nodes/{nodeid}/jobs api request.
        #. Check that all jobs has been killed.
        """
        self.lg('Choose one random node of list of running nodes.')
        node_id=self.base_test.get_random_node()
        self.lg(' Send get /nodes/{nodeid}/jobs api request.')
        status_code = self.nodes_api.kill_job(node_id=node_id)
        self.assertEqual(status_code, 204)
        self.lg('Check that all jobs has been killed.')
        response = response.self.nodes_api.get_running_jobs(node_id=node_id)
        self.assertEqual(response.status_code, 200)
        jobs_list = response.response_content.json()
        for job in jobs_list:
            self.assertTrue(job['state'], 'KILLED')



    def test005_get_job_details(self):
        """ GAT-005
        *GET:/nodes/{nodeid}/jobs/{jobid} *

        **Test Scenario:**

        #. Choose one random node of list of running nodes.
        #. Get list of jobs of this node .
        #. Choose one of these jobs to list its details.
        #. Send get /nodes/{nodeid}/jobs/{jobid} api request.
        #. Compare response with the golden values.
        """

        self.lg('Choose one random node of list of running nodes.')
        node_id = self.base_test.get_random_node()

        self.lg('Get list of jobs of this node .')
        response = self.nodes_api.get_running_jobs(node_id=node_id)
        self.assertEqual(response.status_code, 200)

        self.lg('Choose one of these jobs to list its details.')
        jobs_list = response.response_content.json()
        job_id = nodes_list[random.randint(0, len(jobs_list)]

        self.lg('Send get /nodes/{nodeid}/jobs/{jobid} api request.')
        response = self.nodes_api.get_job_details(node_id=node_id,job_id=job_id)
        self.assertEqual(response.status_code, 200)


    def test006_kill_specific_job(self):
        """ GAT-006
        *DELETE:/nodes/{nodeid}/jobs/{jobid} *

        **Test Scenario:**

        #. get list of jobs.
        #. choose one of these jobs to list its details.
        #. delete /nodes/{nodeid}/jobs/{jobid} api.
        #. verify this job has been killed.
        """

        node_id = self.base_test.get_random_node()
        status_code, response_content = self.nodes_api.get_running_jobs(node_id=node_id)
        job_list = response_content
        job_id = job_list[random.randint(0, len(job_list)-1)
        status_code, response_content = self.nodes_api.kill_job(node_id=node_id, job_id=job_id)
        self.assertEqual(status_code, 204)

    def test007_ping_specific_node(self):
        """ GAT-007
        *POST:/nodes/{nodeid}/ping *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one random node of these nodes.
        #. post /nodes/{nodeid}/ping api.
        #. check response status code.
        """
        node_id = self.base_test.get_random_node()
        status_code, response_content = self.nodes_api.get_running_jobs(node_id=node_id)
        job_list = response_content
        job_id = job_list[random.randint(0, len(job_list)-1)
        status_code, response_content = self.nodes_api.ping_node(node_id=node_id)
        self.assertEqual(status_code, 200)

    def test008_get_node_state(self):
        """ GAT-008
        *GET:/nodes/{nodeid}/state *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get /nodes/{nodeid}/state api.
        #. compare response data with the golden values.
        """
        node_id = self.base_test.get_random_node()
        status_code, response_content = self.nodes_api.get_node_state(node_id=node_id)
        self.assertEqual(status_code, 200)

    def test009_reboot_node(self):
        """ GAT-009
        *POST:/nodes/{nodeid}/reboot *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. post /nodes/{nodeid}/reboot api.
        #. verify that this node has been rebooted.
        """
        node_id = self.base_test.get_random_node()
        status_code, response_content = self.nodes_api.reboot_node(node_id=node_id)
        self.assertEqual(status_code, 204)

    def test010_get_cpus_details(self):
        """ GAT-010
        *GET:/nodes/{nodeid}/cpus *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get /nodes/{nodeid}/cpus api.
        #. compare response data with the golden values.
        """
        node_id = self.base_test.get_random_node()
        status_code, response_content = self.nodes_api.reboot_node(node_id=node_id)
        self.assertEqual(status_code, 200)

    def test011_get_disks_details(self):
        """ GAT-011
        *GET:/nodes/{nodeid}/disks *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get /nodes/{nodeid}/disks api.
        #. compare response data with the golden values.
        """
        node_id = self.base_test.get_random_node()
        status_code, response_content = self.nodes_api.get_disks_detail(node_id=node_id)
        self.assertEqual(status_code, 200)

    def test012_get_memmory_details(self):
        """ GAT-012
        *GET:/nodes/{nodeid}/mem *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get /nodes/{nodeid}/mem api.
        #. compare response data with the golden values.
        """
                node_id = self.base_test.get_random_node()
                status_code, response_content = self.nodes_api.reboot_node(node_id=node_id)
                self.assertEqual(status_code, 200)

    def test013_get_nics_details(self):
        """ GAT-013
        *GET:/nodes/{nodeid}/nics - network interface information*

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get /nodes/{nodeid}/nics api.
        #. compare response data with the golden values.
        """

    def test014_get_info_details(self):
        """ GAT-014
        *GET:/nodes/{nodeid}/info - os information*

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get /nodes/{nodeid}/info api.
        #. compare response data with the golden values.
        """

    def test015_list_processes(self):
        """ GAT-015
        *GET:/nodes/{nodeid}/processes *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get /nodes/{nodeid}/processes api.
        #. compare response data with the golden values.
        """

    def test016_get_process_details(self):
        """ GAT-016
        *GET:/nodes/{nodeid}/processes/{processid} *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get list of running processes
        #. choose one of them.
        #. get /nodes/{nodeid}/processes/{processid} api.
        #. compare response data with the golden values.
        """

    def test017_delete_process(self):
        """ GAT-017
        *DELETE:/nodes/{nodeid}/processes/{processid} *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get list of running processes
        #. choose one of them.
        #. delete /nodes/{nodeid}/processes/{processid} api.
        #. make sure that this process has been killed.
        """

    def test018_list_bridges(self):
        """ GAT-018
        *GET:/nodes/{nodeid}/bridges *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. get /nodes/{nodeid}/bridges api.
        #. compare response data with the golden values.
        """

    def test019_create_bridge(self):
        """ GAT-019
        *POST:/nodes/{nodeid}/bridges *

        **Test Scenario:**

        #. get list of running nodes.
        #. choose one of these nodes.
        #. post /nodes/{nodeid}/bridges api.
        #. compare response data with the golden values.
        """
