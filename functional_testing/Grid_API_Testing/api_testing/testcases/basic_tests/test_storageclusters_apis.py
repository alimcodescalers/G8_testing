from random import randint
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.storageclusters_apis import Storageclusters

class TestStorageclustersAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storageclusters_api = Storageclusters()

    def setUp(self):
        super(TestStorageclustersAPI, self).setUp()
        self.lg.info('Deploy new storage cluster (SC0)')
        self.label = self.rand_str()
        self.servers = randint(1,1000)
        self.types = ['nvme', 'ssd', 'hdd', 'archive']
        self.drivetype = self.random_item(self.types)
        self.slaveNodes = self.random_item([True, False])
        self.nodes = [self.get_random_node()]
        self.body = {"label": self.label,
                     "servers": self.servers,
                     "driveType": self.drivetype,
                     "slaveNodes": self.slaveNodes,
                     "nodes":self.nodes}
        self.storageclusters_api.post_storageclusters(self.body)

    def tearDown(self):
        self.lg.info('Kill storage cluster (SC0)')
        self.storageclusters_api.delete_storageclusters_label(self.label)
        super(TestStorageclustersAPI, self).tearDown()

    def test001_get_storageclusters_label(self):
        """ GAT-001
        **Test Scenario:**
        #. Deploy new storage cluster (SC0)
        #. Get storage cluster (SC0), should succeed with 200
        #. Get nonexisting storage cluster (SC0), should fail with 404
        """
        self.lg.info('Get storage cluster (SC0), should succeed with 200')
        response = self.storageclusters_api.get_storageclusters_label(self.label)
        self.assertEqual(response.status_code, 200)
        for key in ['label', 'driveType', 'nodes']:
            self.assertEqual(response.json()[key], self.body[key])
        self.assertNotEqual(response.json()['status'], 'error')

        self.lg.info('Get nonexisting storage cluster (SC0), should fail with 404')
        response = self.storageclusters_api.get_storageclusters_label('fake_label')
        self.assertEqual(response.status_code, 404)

    def test002_list_storageclusters(self):
        """ GAT-002
        **Test Scenario:**
        #. Deploy new storage cluster (SC0)
        #. List storage clusters, should succeed with 200
        """
        self.lg.info('Get storage cluster (SC0), should succeed with 200')
        response = self.storageclusters_api.get_storageclusters()
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.label, response.json())

    def test003_deploy_new_storagecluster(self):
        """ GAT-003
        **Test Scenario:**
        #. Deploy new storage cluster (SC1), should succeed with 201
        #. List storage clusters, (SC1) should be listed
        #. Kill storage cluster (SC0), should succeed with 204
        """
        self.lg.info('Deploy new storage cluster (SC1), should succeed with 201')
        label = self.rand_str()
        servers = randint(1,1000)
        drivetype = self.random_item(self.types)
        slaveNodes = self.random_item([True, False])
        nodes = [self.get_random_node()]
        body = {"label": label,
                "servers": servers,
                "driveType": drivetype,
                "slaveNodes":slaveNodes,
                "nodes":nodes}
        response = self.storageclusters_api.post_storageclusters(body)
        self.assertEqual(response.status_code, 201)

        self.lg.info('List storage clusters, (SC1) should be listed')
        response = self.storageclusters_api.get_storageclusters()
        self.assertEqual(response.status_code, 200)
        self.assertIn(label, response.json())

        self.lg.info('Kill storage cluster (SC1), should succeed with 204')
        response = self.storageclusters_api.delete_storageclusters_label(label)
        self.assertEqual(response.status_code, 204)

    # @unittest.skip('bug: #96')
    def test004_kill_storagecluster_label(self):
        """ GAT-004
        **Test Scenario:**
        #. #. Deploy new storage cluster (SC0)
        #. Kill storage cluster (SC0), should succeed with 204
        #. List storage clusters, (SC0) should be gone
        #. Kill nonexisting storage cluster, should fail with 404
        """
        self.lg.info('Kill storage cluster (SC0), should succeed with 204')
        response = self.storageclusters_api.delete_storageclusters_label(self.label)
        self.assertEqual(response.status_code, 204)

        self.lg.info('List storage clusters, (SC0) should be gone')
        response = self.storageclusters_api.get_storageclusters()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.label, response.json())

        #bug 135
        # self.lg.info('Kill nonexisting storage cluster, should fail with 404')
        # response = self.storageclusters_api.delete_storageclusters_label('fake_label')
        # self.assertEqual(response.status_code, 404)
