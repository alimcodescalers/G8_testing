from random import randint
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.vms_apis import VmsAPI


class TestVmsAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vms_api = VmsAPI()

    def setUp(self):
        super(TestVmsAPI, self).setUp()

        self.lg.info('Get random nodid (N0)')
        self.nodeid = self.get_random_node()

        self.lg.info('Create virtual machine (VM0) on node (N0)')
        self.vm_id = self.random_string()
        self.vm_mem = randint(1, 4)*1024
        self.vm_cpu = randint(1, 4)
        self.vm_nics = []
        self.vm_disks = []
        self.vm_userCloudInit = {}
        self.vm_systemCloudInit = {}

        self.body = {"id":self.vm_id,
                    "memory":self.vm_mem,
                    "cpu":self.vm_cpu,
                    "nics":self.vm_nics,
                    "disks":self.vm_disks,
                    "userCloudInit":self.vm_userCloudInit,
                    "systemCloudInit":self.vm_systemCloudInit}

        response = self.vms_api.post_node_vms(self.nodeid, self.body)

    def tearDown(self):
        self.lg.info('Delete virtual machine (VM0)')
        self.vms_api.delete_node_vms_vmid(self.nodeid, self.vm_id)

        super(TestVmsAPI, self).tearDown()

    def test001_get_node_vms_vmid(self):
        """ GAT-001
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Get virtual machine (VM0), should succeed with 200.
        #. Get nonexisting virtual machine, should fail with 404.
        """
        self.lg.info('Get virtual machine (VM0), should succeed with 200')
        response = self.vms_api.get_node_vms_vmid(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 200)
        for key in self.body.keys():
            self.assertEqual(self.body[key], response.json()[key])
        self.assertEqual(response.json()['status'], 'running')

        self.lg.info('Get nonexisting virtual machine, should fail with 404')
        response = self.vms_api.get_node_vms_vmid(self.nodeid, 'fake_vm')
        self.assertEqual(response.status_code, 404)

    def test002_get_node_vms(self):
        """ GAT-002
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. List node (N0) virtual machines, virtual machine (VM0) should be listed, should succeed with 200.
        """
        self.lg.info('List node (N0) virtual machines, virtual machine (VM0) should be listed, should succeed with 200')
        response = self.vms_api.get_node_vms(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.vm_id, [x['id'] for x in response.json()])

    def test003_post_node_vms(self):
        """ GAT-003
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM1) on node (N0).
        #. Get virtual machine (VM1), should succeed with 200.
        #. Delete virtual machine (VM1), should succeed with 204.
        #. Create virtual machine with missing parameters, should fail with 400.
        """
        self.lg.info('Create virtual machine (VM1) on node (N0)')
        vm_id = self.random_string()
        vm_mem = randint(1, 4)*1024
        vm_cpu = randint(1, 4)
        vm_nics = []
        vm_disks = []
        vm_userCloudInit = {}
        vm_systemCloudInit = {}

        body = {"id":vm_id,
                "memory":vm_mem,
                "cpu":vm_cpu,
                "nics":vm_nics,
                "disks":vm_disks,
                "userCloudInit":vm_userCloudInit,
                "systemCloudInit":vm_systemCloudInit}

        response = self.vms_api.post_node_vms(self.nodeid, body)
        self.assertEqual(response.status_code, 201)
        vm_location = response.headers['Location']

        self.lg.info('Get virtual machine (VM1), should succeed with 200')
        response = self.vms_api.get_node_vms_vmid(self.nodeid, vm_id)
        self.assertEqual(response.status_code, 200)
        for key in body.keys():
            self.assertEqual(body[key], response.json()[key])
        self.assertEqual(response.json()['status'], 'running')

        self.lg.info('Delete virtual machine (VM1), should succeed with 204')
        response = self.vms_api.delete_node_vms_vmid(self.nodeid, vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Create virtual machine with missing parameters, should fail with 400')
        body = {"id":self.random_string()}
        response = self.vms_api.post_node_vms_vmid(self.nodeid, body)
        self.assertEqual(response.status_code, 400)

    def test004_put_node_vms_vmid(self):
        """ GAT-004
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Update virtual machine (VM1), should succeed with 201.
        #. Get virtual machine (VM1), should succeed with 200.
        #. Update virtual machine with missing parameters, should fail with 400.
        """
        self.lg.info('Create virtual machine (VM0) on node (N0)')
        vm_id = self.random_string()
        vm_mem = randint(1, 4)*1024
        vm_cpu = randint(1, 4)
        vm_nics = []
        vm_disks = []
        vm_userCloudInit = {}
        vm_systemCloudInit = {}

        body = {"id":self.vm_id,
                "memory":vm_mem,
                "cpu":vm_cpu,
                "nics":vm_nics,
                "disks":vm_disks,
                "userCloudInit":vm_userCloudInit,
                "systemCloudInit":vm_systemCloudInit}

        response = self.vms_api.put_node_vms_vmid(self.nodeid, self.vm_id, body)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), should succeed with 200')
        response = self.vms_api.get_node_vms_vmid(self.nodeid, vm_id)
        self.assertEqual(response.status_code, 200)
        for key in body.keys():
            self.assertEqual(body[key], response.json()[key])
        self.assertEqual(response.json()['status'], 'running')


        self.lg.info('Update virtual machine with missing parameters, should fail with 400')
        body = {"id":self.random_string()}
        response = self.vms_api.post_node_vms_vmid(self.nodeid, body)
        self.assertEqual(response.status_code, 400)

    def test005_get_node_vms_vmid_info(self):
        """ GAT-005
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Get virtual machine (VM0) info, should succeed with 200.
        #. Get nonexisting virtual machine info, should fail with 404.
        """
        self.lg.info('Get virtual machine (VM0) info, should succeed with 200')
        response = self.vms_api.get_node_vms_vmid_info(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nics'], self.vm_nics)
        self.assertEqual(response.json()['disks'], self.vm_disks)

        self.lg.info('Get nonexisting virtual machine info, should fail with 404')
        response = self.vms_api.get_node_vms_vmid_info(self.nodeid, 'fake_vm')
        self.assertEqual(response.status_code, 404)

    def test006_post_node_vms_vmid_start(self):
        """ GAT-006
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Stop virtual machine (VM0), should succeed with 204.
        #. Start virtual machine (VM0), should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be running.
        """
        self.lg.info('Stop virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_node_vms_vmid_stop(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Start virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_node_vms_vmid_start(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), virtual machine (VM0) status should be running')
        response = self.vms_api.get_node_vms_vmid(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'running')

    def test007_post_node_vms_vmid_stop(self):
        """ GAT-007
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Stop virtual machine (VM0), should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be halted.
        """
        self.lg.info('Stop virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_node_vms_vmid_stop(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), virtual machine (VM0) status should be running')
        response = self.vms_api.get_node_vms_vmid(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'halting')

    def test008_post_node_vms_vmid_pause(self):
        """ GAT-008
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Pause virtual machine (VM0), should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be paused.
        """
        self.lg.info('Pause virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_node_vms_vmid_pause(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), virtual machine (VM0) status should be paused')
        response = self.vms_api.get_node_vms_vmid(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'paused')

    def test009_post_node_vms_vmid_shutdown(self):
        """ GAT-009
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Shutdown virtual machine (VM0), should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be halted.
        """
        self.lg.info('Shutdown virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_node_vms_vmid_shutdown(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), virtual machine (VM0) status should be halted')
        response = self.vms_api.get_node_vms_vmid(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'halted')

    def test010_post_node_vms_vmid_migrate(self):
        """ GAT-010
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Migrate virtual machine (VM0) to another node, should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be migrating.
        """
        self.lg.info('Migrate virtual machine (VM0) to another node, should succeed with 204')
        node_2 = self.get_random_node(except_node=self.nodeid)
        response = self.vms_api.post_node_vms_vmid_migrate(node_2, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), virtual machine (VM0) status should be running')
        response = self.vms_api.get_node_vms_vmid(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'migrating')
