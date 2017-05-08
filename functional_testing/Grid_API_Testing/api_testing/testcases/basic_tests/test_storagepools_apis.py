import  random
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.storagepools_apis import StoragepoolsAPI
from api_testing.python_client.client import Client
import unittest, time

class TestStoragepoolsAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storagepool_api = StoragepoolsAPI()

    def setUp(self):
        super(TestStoragepoolsAPI, self).setUp()

        self.lg.info('Get random nodid (N0)')
        self.nodeid = self.get_random_node()
        pyclient_ip = [x['ip'] for x in self.nodes if x['id'] == self.nodeid][0]
        self.pyclient = Client(pyclient_ip)

        self.lg.info('Create storagepool (SP0) on node (N0)')
        self.storagepool_name = self.random_string()
        self.levels = ['raid0', 'raid1', 'raid5', 'raid6', 'raid10', 'dup', 'single']

        free_devices = self.pyclient.getFreeDisks()
        if free_devices == []:
            self.skipTest('no free disks on node {}'.format(self.nodeid))

        if len(free_devices) < 5:
            self.metadata = 'single'
            self.data = 'single'
            self.devices = [random.choice(free_devices)]
        else:
            self.metadata = self.random_item(self.levels)
            self.data = self.random_item(self.levels)
            self.devices = free_devices[:4]
        
        self.body = {"name":self.storagepool_name, 
                     "metadataProfile":self.metadata, 
                     "dataProfile":self.data, 
                     "devices":self.devices}
        self.storagepool_api.post_storagepools(self.nodeid, self.body)

        time.sleep(30)

        self.lg.info('Create filesystem (FS0) on storagepool (SP0)')
        self.fs_name = self.random_string()
        self.fs_quota = random.randint(0, 10)
        self.fs_body = {"name":self.fs_name, "quota":self.fs_quota}
        self.storagepool_api.post_storagepools_storagepoolname_filesystems(self.nodeid, self.storagepool_name, self.fs_body)
        time.sleep(10)

        # self.lg.info('Create snapshot (SS0) on filesystem (FS0)')
        # self.storagepool_api.post_filesystems_snapshots(self.nodeid, self.storagepool_name, self.fs_name)


    def tearDown(self):
        self.lg.info('Delete Storagepool (SP0)')
        self.storagepool_api.delete_storagepools_storagepoolname(self.nodeid, self.storagepool_name)
        time.sleep(30)
        super(TestStoragepoolsAPI, self).tearDown()

    def test001_get_storagepool(self):
        """ GAT-001
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Create storagepool (SP0) on node (N0), should succeed.
        #. Get storagepool (SP0), should succeed with 200.
        #. Get storagepool (SP0) using python client, should be listed
        #. Get nonexisting storagepool, should fail with 404.
        """
        self.lg.info('Get storagepool (SP0), should succeed with 200')
        response = self.storagepool_api.get_storagepools_storagepoolname(self.nodeid, self.storagepool_name)
        self.assertEqual(response.status_code, 200)
        for key in self.body.keys():
            if key == 'devices':
                continue
            self.assertEqual(response.json()[key], self.body[key])

        self.lg.info('Get storagepool (SP0) using python client, should be listed')
        storagepools = self.pyclient.client.btrfs.list()
        storagepool_SP0 = [x for x in storagepools if x['label'] == 'sp_{}'.format(self.storagepool_name)]
        self.assertNotEqual(storagepool_SP0, [])
        self.assertIn(self.devices[0], [x['path'][:-1] for x in storagepool_SP0[0]['devices']])

        self.lg.info('Get nonexisting storagepool, should fail with 404')
        response = self.storagepool_api.get_storagepools_storagepoolname(self.nodeid, 'fake_storagepool')
        self.assertEqual(response.status_code, 404)

    def test002_list_storagepool(self):
        """ GAT-002
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create Storagepool (SP0) on node (N0).
        #. list node (N0) storagepools, storagepool (SP0) should be listed.
        """
        self.lg.info('list node (N0) storagepools, storagepool (SP0) should be listed')
        response = self.storagepool_api.get_storagepools(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.storagepool_name, [x['name'] for x in response.json()])

    def test003_post_storagepool(self):
        """ GAT-003
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create storagepool (SP0) on node (N0).
        #. Get storagepool (SP0), should succeed with 200.
        #. Get storagepool (SP1) using python client, should be listed
        #. Delete Storagepool (SP0), should succeed with 204.
        #. Create invalid storagepool (missing required params), should fail with 400.
        """
        self.lg.info('Get random nodid, should succeed')
        nodeid = self.get_random_node()

        self.lg.info('Create Storagepool (SP1), should succeed with 201')
        name = self.random_string()
        free_devices = self.pyclient.getFreeDisks()
        if free_devices == []:
            self.skipTest('no free disks on node {}'.format(nodeid))

        if len(free_devices) < 5:
            metadata = 'single'
            data = 'single'
            devices = [random.choice(free_devices)]
        else:
            metadata = self.random_item( self.levels)
            data = self.random_item( self.levels)
            devices = free_devices[:4]
        
        body = {"name":name, 
                "metadataProfile":metadata, 
                "dataProfile":data, 
                "devices":devices}

        response = self.storagepool_api.post_storagepools(nodeid, body)
        self.assertEqual(response.status_code, 201)
        time.sleep(30)
        
        self.lg.info('Get Storagepool (SP1), should succeed with 200')
        response = self.storagepool_api.get_storagepools_storagepoolname(nodeid, name)
        self.assertEqual(response.status_code, 200)
        for key in body.keys():
            if key == 'devices':
                continue
            self.assertEqual(response.json()[key], body[key])

        self.lg.info('Get storagepool (SP1) using python client, should be listed')
        storagepools = self.pyclient.client.btrfs.list()
        storagepool_SP1 = [x for x in storagepools if x['label'] == 'sp_{}'.format(name)]
        self.assertNotEqual(storagepool_SP1, [])
        self.assertEqual(devices, [x['path'][:-1] for x in storagepool_SP1[0]['devices']])

        self.lg.info('Delete Storagepool (SP0), should succeed with 204')
        response = self.storagepool_api.delete_storagepools_storagepoolname(nodeid, name)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Create invalid storagepool, should fail with 400')
        body = {"name":name, "metadataProfile":metadata}
        response = self.storagepool_api.post_storagepools(nodeid, body)
        self.assertEqual(response.status_code, 400)

    def test004_delete_storagepool(self):
        """ GAT-004
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create Storagepool (SP0) on node (N0).
        #. Delete Storagepool (SP0), should succeed with 204.
        #. list node (N0) storagepools, storagepool (SP0) should be gone.
        #. Delete nonexisting storagepool, should fail with 404.
        """
        self.lg.info('Delete storagepool (SP0), should succeed with 204')
        response = self.storagepool_api.delete_storagepools_storagepoolname(self.nodeid, self.storagepool_name)
        self.assertEqual(response.status_code, 204)

        self.lg.info('list node (N0) storagepools, storagepool (SP0) should be gone')
        response = self.storagepool_api.get_storagepools(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.test001_get_storagepool, [x['name'] for x in response.json()])

        self.lg.info('Delete nonexisting storagepool, should fail with 404')
        response = self.storagepool_api.delete_storagepools_storagepoolname(self.nodeid, 'fake_storagepool')
        self.assertEqual(response.status_code, 404)

    @unittest.skip('bug: #93')
    def test005_get_storagepool_device(self):
        """ GAT-005
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create storagepool (SP0) with device (DV0) on node (N0).
        #. Get device (DV0), should succeed with 200.
        #. Get nonexisting device, should fail with 404.
        """
        self.lg.info('Get device (DV0), should succeed with 200')
        response = self.storagepool_api.get_storagepools_storagepoolname_devices(self.nodeid, self.storagepool_name)
        self.assertEqual(response.status_code, 200)
        device_uuid = response.json()[0]['uuid']

        response = self.storagepool_api.get_storagepools_storagepoolname_devices_deviceid(self.nodeid, self.storagepool_name, device_uuid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['uuid'], device_uuid)
        self.assertEqual(response.json()['status'], 'healthy')

        self.lg.info('Get nonexisting device, should fail with 404')
        response = self.storagepool_api.get_storagepools_storagepoolname_devices_deviceid(self.nodeid, self.storagepool_name, 'fake_device')
        self.assertEqual(response.status_code, 404)

    @unittest.skip('bug: #93')
    def test006_list_storagepool_devices(self):
        """ GAT-006
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create storagepool (SP0) with device (DV0) on node (N0).
        #. list storagepool (SP0) devices, should succeed with 200.
        """
        self.lg.info('list storagepool (SP0) devices, should succeed with 200')
        response = self.storagepool_api.get_storagepools_storagepoolname_devices(self.nodeid, self.storagepool_name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['status'], 'healthy')

    def test007_post_storagepool_device(self):
        """ GAT-007
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create storagepool (SP0) with device (DV0) on node (N0).
        #. Create device (DV1) on storagepool (SP0), should succeed with 201.
        #. list storagepool (SP0) devices, device (DV1) should be listed.
        #. Create device with invalid body, should fail with 400.
        """
        self.lg.info('Create device (DV1) on storagepool (SP0), should succeed with 201')

        free_devices = self.pyclient.getFreeDisks() 
        if free_devices == []:
            self.skipTest('no free disks on node {}'.format(self.nodeid))

        device = random.choice(free_devices)
        body = [device]
        response = self.storagepool_api.post_storagepools_storagepoolname_devices(self.nodeid, self.storagepool_name, body)
        self.assertEqual(response.status_code, 204)
        time.sleep(10)

        self.lg.info('list storagepool (SP0) devices, should succeed with 200')
        response = self.storagepool_api.get_storagepools_storagepoolname_devices(self.nodeid, self.storagepool_name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(device, [x['deviceName'][:-1] for x in response.json()])

        # self.lg.info('Create device with invalid body, should fail with 400')
        # body = self.random_string()
        # response = self.storagepool_api.post_storagepools_storagepoolname_devices(self.nodeid, self.storagepool_name, body)
        # self.assertEqual(response.status_code, 404)

    def test008_delete_storagepool_device(self):
        """ GAT-008
        **Test Scenario:**

        #. Get random nodid, should succeed.
        #. Create storagepool (SP0) with device (DV0) on node (N1), should succeed with 201.
        #. Delete device (DV0), should succeed with 204.
        #. list storagepool (SP0) devices, device (DV0) should be gone.
        #. Delete nonexisting device, should fail with 404.
        """
        self.lg.info('Create device (DV1) on storagepool (SP0), should succeed with 201')
        device = random.choice(self.pyclient.getFreeDisks())
        body = [device]
        response = self.storagepool_api.post_storagepools_storagepoolname_devices(self.nodeid, self.storagepool_name, body)
        self.assertEqual(response.status_code, 204)
        time.sleep(10)

        self.lg.info('list storagepool (SP0) devices, device (DV0) should be gone')
        response = self.storagepool_api.get_storagepools_storagepoolname_devices(self.nodeid, self.storagepool_name)
        self.assertEqual(response.status_code, 200)
        deviceuuid = [x['uuid'] for x in response.json() if x['deviceName'][:-1] == device]
        self.assertNotEqual(deviceuuid, [], 'device was not added to storagepool')

        self.lg.info('Delete device (DV1), should succeed with 204')
        response = self.storagepool_api.delete_storagepools_storagepoolname_devices_deviceid(self.nodeid, self.storagepool_name, deviceuuid[0])
        self.assertEqual(response.status_code, 204)
        time.sleep(10)

        self.lg.info('list storagepool (SP0) devices, device (DV0) should be gone')
        response = self.storagepool_api.get_storagepools_storagepoolname_devices(self.nodeid, self.storagepool_name)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(device, [x['deviceName'][:-1] for x in response.json()])

        # self.lg.info('Delete nonexisting device, should fail with 404')
        # response = self.storagepool_api.delete_storagepools_storagepoolname_devices_deviceid(self.nodeid, self.storagepool_name, 'fake_device')
        # self.assertEqual(response.status_code, 404)

    def test009_get_storagepool_filessystem(self):
        """ GAT-009
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Create storagepool (SP0) on node (N0), should succeed.
        #. Create filesystem (FS0) on storagepool (SP0).
        #. Get filesystem (FS0), should succeed with 200.
        #. Get nonexisting filesystem, should fail with 404.
        """
        self.lg.info('Get filesystem (FS0), should succeed with 200')
        response = self.storagepool_api.get_storagepools_storagepoolname_filesystems_filesystemname(self.nodeid, self.storagepool_name, self.fs_name)
        self.assertEqual(response.status_code, 200)
        for key in self.fs_body.keys():
            self.assertEqual(response.json()[key], self.fs_body[key])

        self.lg.info('Get nonexisting filesystem, should fail with 404')
        response = self.storagepool_api.get_storagepools_storagepoolname_filesystems_filesystemname(self.nodeid, self.storagepool_name, 'fake_filesystem')
        self.assertEqual(response.status_code, 404)

    def test010_list_storagepool_filesystems(self):
        """ GAT-010
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create Storagepool (SP0) on node (N0).
        #. Create filesystem (FS0) on storagepool (SP0).
        #. list storagepools (SP0) filesystems, filesystem (FS0) should be listed.
        """
        self.lg.info('list storagepools (SP0) filesystems, filesystem (FS0) should be listed')
        response = self.storagepool_api.get_storagepools_storagepoolname_filesystems(self.nodeid, self.storagepool_name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.fs_name, response.json())

    def test011_post_storagepool_filesystem(self):
        """ GAT-011
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create storagepool (SP0) on node (N0).
        #. Create filesystem (FS1) on storagepool (SP0), should succeed with 201.
        #. Get filesystem (FS1), should succeed with 200.
        #. Delete filesystem (FS1), should succeed with 204.
        #. Create invalid filesystem (missing required params), should fail with 400.
        """
        self.lg.info('Create filesystem (FS1) on storagepool (SP0), should succeed with 201')
        name = self.random_string()
        quota = random.randint(0, 10)
        body = {"name":name, "quota":quota}
        response = self.storagepool_api.post_storagepools_storagepoolname_filesystems(self.nodeid, self.storagepool_name, body)
        self.assertEqual(response.status_code, 201)
        time.sleep(5)

        self.lg.info('Get filesystem (FS1), should succeed with 200')
        response = self.storagepool_api.get_storagepools_storagepoolname_filesystems_filesystemname(self.nodeid, self.storagepool_name, name)
        self.assertEqual(response.status_code, 200)
        for key in body.keys():
            self.assertEqual(response.json()[key], body[key])

        self.lg.info('Delete filesystem (FS1), should succeed with 204')
        response = self.storagepool_api.delete_storagepools_storagepoolname_filesystems_filesystemname(self.nodeid, self.storagepool_name, name)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Create filesystem with invalid body, should fail with 400')
        body = {self.random_string():self.random_string()}
        response = self.storagepool_api.post_storagepools_storagepoolname_filesystems(self.nodeid, self.storagepool_name, body)
        self.assertEqual(response.status_code, 400)

    def test012_delete_storagepool_filesystem(self):
        """ GAT-012
        **Test Scenario:**

        #. Get random nodid (N0).
        #. Create Storagepool (SP0) on node (N0).
        #. Create filesystem (FS0) on storagepool (SP0).
        #. Delete filesystem (FS0), should succeed with 204.
        #. list storagepool (SP0) filesystems, filesystem (FS0) should be gone.
        #. Delete nonexisting filesystems, should fail with 404.
        """
        self.lg.info('Delete filesystem (FS0), should succeed with 204')
        response = self.storagepool_api.delete_storagepools_storagepoolname_filesystems_filesystemname(self.nodeid, self.storagepool_name, self.fs_name)
        self.assertEqual(response.status_code, 204)

        self.lg.info('list storagepool (SP0) filesystems, filesystem (FS0) should be gone')
        response = self.storagepool_api.get_storagepools_storagepoolname_filesystems(self.nodeid, self.storagepool_name)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.fs_name, response.json())

        self.lg.info('Delete nonexisting filesystems, should fail with 404')
        response = self.storagepool_api.delete_storagepools_storagepoolname_filesystems_filesystemname(self.nodeid, self.storagepool_name, 'fake_filesystem')
        self.assertEqual(response.status_code, 404)

    @unittest.skip('issue: #141')
    def test013_get_storagepool_filessystem_snapshot(self):
        """ GAT-013
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Create storagepool (SP0) on node (N0), should succeed.
        #. Create filesystem (FS0) on storagepool (SP0).
        #. Create snapshot (SS0) on filesystem (FS0).
        #. Get snapshot (SS0), should succeed with 200.
        #. Get nonexisting snapshot, should fail with 404.
        """
        self.lg.info('Get snapshot (SS0), should succeed with 200')
        response = self.storagepool_api.get_filesystem_snapshots_snapshotname(self.nodeid, self.storagepool_name,
                                                                                           self.fs_name,
                                                                                           self.ss_name)
        self.assertEqual(response.status_code, 200)
        for key in self.ss_body.keys():
            self.assertEqual(response.json()[key], self.ss_body[key])

        self.lg.info('Get nonexisting snapshot, should fail with 404')
        response = self.storagepool_api.get_filesystem_snapshots_snapshotname(self.nodeid, self.storagepool_name,
                                                                                           self.fs_name,
                                                                                           'fake_snapshot')
        self.assertEqual(response.status_code, 404)

    @unittest.skip('issue: #141')
    def test014_list_storagepool_filesystems_snapshots(self):
        """ GAT-014
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Create storagepool (SP0) on node (N0), should succeed.
        #. Create filesystem (FS0) on storagepool (SP0).
        #. Create snapshot (SS0) on filesystem (FS0).
        #. list snapshots of filesystems (FS0), snapshot (SS0) should be listed.
        """
        self.lg.info('list snapshots of filesystems (FS0), snapshot (SS0) should be listed')
        response = self.storagepool_api.get_filesystem_snapshots(self.nodeid, self.storagepool_name, self.fs_name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.ss_name, response.json())

    @unittest.skip('issue: #141')
    def test015_post_storagepool_filesystem_snapshot(self):
        """ GAT-015
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Create storagepool (SP0) on node (N0), should succeed.
        #. Create filesystem (FS0) on storagepool (SP0).
        #. Create snapshot (SS1) on filesystem (FS0).
        #. Get snapshot (SS1), should succeed with 200.
        #. Delete snapshot (SS1), should succeed with 204.
        #. Create snapshot with missing required params, should fail with 400.
        """
        self.lg.info('Create snapshot (SS1) on filesystem (FS0)')
        name = self.random_string()
        body = {"name":name}
        response = self.storagepool_api.post_filesystems_snapshots(self.nodeid, self.storagepool_name, self.fs_name, body)
        self.assertEqual(response.status_code, 201)

        self.lg.info(' Get snapshot (SS1), should succeed with 200')
        response = self.storagepool_api.get_filesystem_snapshots_snapshotname(self.nodeid, self.storagepool_name,
                                                                                           self.fs_name,
                                                                                           name)
        self.assertEqual(response.status_code, 200)
        for key in body.keys():
            self.assertEqual(response.json()[key], body[key])

        self.lg.info('Delete snapshot (SS1), should succeed with 204')
        response = self.storagepool_api.delete_filesystem_snapshots_snapshotname(self.nodeid, self.storagepool_name,
                                                                                              self.fs_name,
                                                                                              name)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Create snapshot with missing required params, should fail with 400')
        body = {}
        response = self.storagepool_api.post_filesystems_snapshots(self.nodeid, self.storagepool_name, self.fs_name, body)
        self.assertEqual(response.status_code, 400)

    @unittest.skip('issue: #141')
    def test016_delete_storagepool_filesystem_snapshot(self):
        """ GAT-016
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Create storagepool (SP0) on node (N0), should succeed.
        #. Create filesystem (FS0) on storagepool (SP0).
        #. Create snapshot (SS0) on filesystem (FS0).
        #. Delete  snapshot (SS0), should succeed with 204.
        #. list filesystem (FS0) snapshots, snapshot (SS0) should be gone.
        #. Delete nonexisting snapshot, should fail with 404.
        """
        self.lg.info('Delete  snapshot (SS0), should succeed with 204')
        response = self.storagepool_api.delete_filesystem_snapshots_snapshotname(self.nodeid, self.storagepool_name,
                                                                                              self.fs_name,
                                                                                              self.ss_name)
        self.assertEqual(response.status_code, 204)

        self.lg.info('list filesystem (FS0) snapshots, snapshot (SS0) should be gone')
        response = self.storagepool_api.delete_filesystem_snapshots_snapshotname(self.nodeid, self.storagepool_name, self.fs_name)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.ss_name, response.json())

        self.lg.info('Delete nonexisting snapshot, should fail with 404')
        response = self.storagepool_api.delete_filesystem_snapshots_snapshotname(self.nodeid, self.storagepool_name, self.fs_name, 'fake_filesystem')
        self.assertEqual(response.status_code, 404)
