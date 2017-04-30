import random
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.vms_apis import VmsAPI
import unittest
from api_testing.python_client.client import Client
import time

# @unittest.skip('bug: #101')
class TestVmsAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vms_api = VmsAPI()

    def setUp(self):
        super(TestVmsAPI, self).setUp()

        self.lg.info('Get random nodid (N0)')
        self.nodeid = self.get_random_node()
        pyclient_ip = [x['pyclient'] for x in self.nodes_info if x['id'] == self.nodeid][0]
        self.pyclient = Client(pyclient_ip)

        self.lg.info('Create virtual machine (VM0) on node (N0)')
        self.vm_id = self.random_string()
        self.vm_mem = 1024
        self.vm_cpu = 1
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

        response = self.vms_api.post_nodes_vms(self.nodeid, self.body)

    def tearDown(self):
        self.lg.info('Delete virtual machine (VM0)')
        self.vms_api.delete_nodes_vms_vmid(self.nodeid, self.vm_id)

        super(TestVmsAPI, self).tearDown()

    def test001_get_nodes_vms_vmid(self):
        """ GAT-001
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Get virtual machine (VM0), should succeed with 200.
        #. Get nonexisting virtual machine, should fail with 404.
        """
        self.lg.info('Get virtual machine (VM0), should succeed with 200')
        response = self.vms_api.get_nodes_vms_vmid(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 200)
        keys_to_check = ['id', 'memory', 'cpu', 'nics', 'disks']
        for key in keys_to_check:
            self.assertEqual(self.body[key], response.json()[key])
        self.assertEqual(response.json()['status'], 'running')

        for _ in range(15):
            vms = self.pyclient.client.kvm.list()
            if self.vm_id in [x['name'] for x in vms]:
                break
            else:
                time.sleep(1)
        else:
            raise AssertionError('{} not in clinet kvm.list'.format(self.vm_id))

        self.lg.info('Get nonexisting virtual machine, should fail with 404')
        response = self.vms_api.get_nodes_vms_vmid(self.nodeid, 'fake_vm')
        self.assertEqual(response.status_code, 404)

    def test002_get_node_vms(self):
        """ GAT-002
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. List node (N0) virtual machines, virtual machine (VM0) should be listed, should succeed with 200.
        """
        self.lg.info('List node (N0) virtual machines, virtual machine (VM0) should be listed, should succeed with 200')
        response = self.vms_api.get_nodes_vms(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.vm_id, [x['id'] for x in response.json()])
        

    @unittest.skip('bug: #132')
    def test003_post_node_vms(self):
        """ GAT-003
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM1) on node (N0).
        #. Get virtual machine (VM1), should succeed with 200.
        #. List kvms in python client, (VM1) should be listed.
        #. Delete virtual machine (VM1), should succeed with 204.
        #. Create virtual machine with missing parameters, should fail with 400.
        """
        self.lg.info('Create virtual machine (VM1) on node (N0)')
        vm_id = self.random_string()
        vm_mem = random.randint(1,16)*1024
        vm_cpu = random.randint(1,16)
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

        response = self.vms_api.post_nodes_vms(self.nodeid, body)
        if response.status_code == 400:
            body['memory'] = 1024
            body['cpu'] = 1
            response = self.vms_api.post_nodes_vms(self.nodeid, body)
        
        self.assertEqual(response.status_code, 201)

        self.lg.info('Get virtual machine (VM1), should succeed with 200')
        response = self.vms_api.get_nodes_vms_vmid(self.nodeid, vm_id)
        self.assertEqual(response.status_code, 200)
        keys_to_check = ['id', 'memory', 'cpu', 'nics', 'disks']
        for key in keys_to_check:
            self.assertEqual(body[key], response.json()[key])
        self.assertEqual(response.json()['status'], 'running')

        self.lg.info('List kvms in python client, (VM1) should be listed')
        vms = self.pyclient.client.kvm.list()
        self.assertIn(vm_id, [x['name'] for x in vms])

        self.lg.info('Delete virtual machine (VM1), should succeed with 204')
        response = self.vms_api.delete_nodes_vms_vmid(self.nodeid, vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Create virtual machine with missing parameters, should fail with 400')
        body = {"id":self.random_string()}
        response = self.vms_api.post_nodes_vms(self.nodeid, body)
        self.assertEqual(response.status_code, 400)

    @unittest.skip('bug: #126')
    def test004_put_nodes_vms_vmid(self):
        """ GAT-004
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Update virtual machine (VM1), should succeed with 201.
        #. Get virtual machine (VM1), should succeed with 200.
        #. Update virtual machine with missing parameters, should fail with 400.
        """
        self.lg.info('Create virtual machine (VM0) on node (N0)')
        vm_id = self.vm_id
        vm_mem = 2*1024
        vm_cpu = 2
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

        response = self.vms_api.put_nodes_vms_vmid(self.nodeid, self.vm_id, body)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), should succeed with 200')
        response = self.vms_api.get_nodes_vms_vmid(self.nodeid, vm_id)
        self.assertEqual(response.status_code, 200)

        keys_to_check = ['id', 'memory', 'cpu', 'nics', 'disks']
        for key in keys_to_check:
            self.assertEqual(body[key], response.json()[key])
        self.assertEqual(response.json()['status'], 'running')


        self.lg.info('Update virtual machine with missing parameters, should fail with 400')
        body = {"id":self.random_string()}
        response = self.vms_api.put_nodes_vms_vmid(self.nodeid, body)
        self.assertEqual(response.status_code, 400)

    @unittest.skip('bug: #131')    
    def test005_get_nodes_vms_vmid_info(self):
        """ GAT-005
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Get virtual machine (VM0) info, should succeed with 200.
        #. Get nonexisting virtual machine info, should fail with 404.
        """
        self.lg.info('Get virtual machine (VM0) info, should succeed with 200')
        response = self.vms_api.get_nodes_vms_vmid_info(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nics'], self.vm_nics)
        self.assertEqual(response.json()['disks'], self.vm_disks)

        self.lg.info('Get nonexisting virtual machine info, should fail with 404')
        response = self.vms_api.get_nodes_vms_vmid_info(self.nodeid, 'fake_vm')

    # @unittest.skip('bug: #91')
    def test006_delete_nodes_vms_vmid(self):
        """ GAT-006
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Delete virtual machine (VM0), should succeed with 204.
        #. List kvms in python client, (VM0) should be gone.
        #. Delete nonexisting virtual machine, should fail with 404.
        """
        self.lg.info('Delete virtual machine (VM0), should succeed with 204')
        response = self.vms_api.delete_nodes_vms_vmid(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('List kvms in python client, (VM0) should be gone')
        vms = self.pyclient.client.kvm.list()
        self.assertNotIn(self.vm_id, [x['name'] for x in vms])

        # bug #129
        # self.lg.info('Delete nonexisting virtual machine, should fail with 404')
        # response = self.vms_api.delete_nodes_vms_vmid(self.nodeid, 'fake_vm_id')
        # self.assertEqual(response.status_code, 404)

    def test007_post_nodes_vms_vmid_start(self):
        """ GAT-007
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Stop virtual machine (VM0), should succeed with 204.
        #. Start virtual machine (VM0), should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be running.
        """
        self.lg.info('Stop virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_nodes_vms_vmid_stop(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)
        for _ in range(15):   
            response = self.vms_api.get_nodes_vms_vmid(self.nodeid, self.vm_id)
            self.assertEqual(response.status_code, 200)
            status = response.json()['status']
            if status in ['halting', 'halted']:
                break
            else:
                time.sleep(1)
        else:
            raise AssertionError('{} is not in {}'.format(status, 'halting or halted'))

        vms = self.pyclient.client.kvm.list()
        vm0 = [x for x in vms if x['name'] == self.vm_id]
        self.assertEqual(vm0, [])

        self.lg.info('Start virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_nodes_vms_vmid_start(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)
        for _ in range(15):   
            response = self.vms_api.get_nodes_vms_vmid(self.nodeid, self.vm_id)
            self.assertEqual(response.status_code, 200)
            status = response.json()['status']
            if status == 'running':
                break
            else:
                time.sleep(1)
        else:
            raise AssertionError('{} is not {}'.format(status, 'running'))

        vms = self.pyclient.client.kvm.list()
        vm0 = [x for x in vms if x['name'] == self.vm_id]
        self.assertNotEqual(vm0, [])
        self.assertEquals(vm0[0]['state'], 'running')


    def test008_post_nodes_vms_vmid_stop(self):
        """ GAT-008
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Stop virtual machine (VM0), should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be halting.
        """
        self.lg.info('Stop virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_nodes_vms_vmid_stop(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), virtual machine (VM0) status should be halting')
        for _ in range(15):   
            response = self.vms_api.get_nodes_vms_vmid(self.nodeid, self.vm_id)
            self.assertEqual(response.status_code, 200)
            status = response.json()['status']
            if status in ['halting', 'halted']:
                break
            else:
                time.sleep(1)
        else:
            raise AssertionError('{} not {}'.format(status, 'halting or halted'))

        vms = self.pyclient.client.kvm.list()
        vm0 = [x for x in vms if x['name'] == self.vm_id]
        self.assertEqual(vm0, [])


    @unittest.skip('bug: #127')
    def test009_post_nodes_vms_vmid_pause_resume(self):
        """ GAT-009
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Pause virtual machine (VM0), should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be paused.
        #. Resume virtual machine (VM0), should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be running
        """
        self.lg.info('Pause virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_nodes_vms_vmid_pause(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), virtual machine (VM0) status should be halting')
        for _ in range(15):   
            response = self.vms_api.get_nodes_vms_vmid(self.nodeid, self.vm_id)
            self.assertEqual(response.status_code, 200)
            status = response.json()['status']
            if status == 'paused':
                break
            else:
                time.sleep(1)
        else:
            raise AssertionError('{} != {}'.format(status, 'paused'))

        vms = self.pyclient.client.kvm.list()
        vm0 = [x for x in vms if x['name'] == self.vm_id]
        self.assertNotEqual(vm0, [])
        self.assertEquals(vm0[0]['state'], 'paused')

        self.lg.info('Resume virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_nodes_vms_vmid_resume(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Get virtual machine (VM0), virtual machine (VM0) status should be running')
        for _ in range(15):   
            response = self.vms_api.get_nodes_vms_vmid(self.nodeid, self.vm_id)
            self.assertEqual(response.status_code, 200)
            status = response.json()['status']
            if status == 'running':
                break
            else:
                time.sleep(1)
        else:
            raise AssertionError('{} != {}'.format(status, 'paused'))

        vms = self.pyclient.client.kvm.list()
        vm0 = [x for x in vms if x['name'] == self.vm_id]
        self.assertNotEqual(vm0, [])
        self.assertEquals(vm0[0]['state'], 'running')


    @unittest.skip('bug: #128')
    def test010_post_nodes_vms_vmid_shutdown(self):
        """ GAT-010
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Shutdown virtual machine (VM0), should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be halted.
        """
        self.lg.info('Shutdown virtual machine (VM0), should succeed with 204')
        response = self.vms_api.post_nodes_vms_vmid_shutdown(self.nodeid, self.vm_id)
        self.assertEqual(response.status_code, 204)
        for _ in range(15):   
            response = self.vms_api.get_nodes_vms_vmid(self.nodeid, self.vm_id)
            self.assertEqual(response.status_code, 200)
            status = response.json()['status']
            if status in ['halting', 'halted']:
                break
            else:
                time.sleep(1)
        else:
            raise AssertionError('{} not {}'.format(status, 'halting or halted'))

        vms = self.pyclient.client.kvm.list()
        vm0 = [x for x in vms if x['name'] == self.vm_id]
        self.assertEqual(vm0, [])
    

    @unittest.skip('need at least 2 nodes')
    def test011_post_nodes_vms_vmid_migrate(self):
        """ GAT-011
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create virtual machine (VM0) on node (N0).
        #. Migrate virtual machine (VM0) to another node, should succeed with 204.
        #. Get virtual machine (VM0), virtual machine (VM0) status should be migrating.
        """
        self.lg.info('Migrate virtual machine (VM0) to another node, should succeed with 204')
        node_2 = self.get_random_node(except_node=self.nodeid)
        body = {"nodeid": node_2}
        response = self.vms_api.post_nodes_vms_vmid_migrate(self.nodeid, self.vm_id, body)
        self.assertEqual(response.status_code, 204)

        for _ in range(15):   
            response = self.vms_api.get_nodes_vms_vmid(self.nodeid, self.vm_id)
            self.assertEqual(response.status_code, 200)
            status = response.json()['status']
            if status == 'migrating':
                break
            else:
                time.sleep(1)
        else:
            raise AssertionError('{} is not {}'.format(status, 'migrating'))
