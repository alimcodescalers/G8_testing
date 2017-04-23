from random import randint
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.zerotiers_apis import ZerotiersAPI
import unittest
from api_testing.python_client.client import Client

class TestZerotiersAPI(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.zerotier_api = ZerotiersAPI()

    def setUp(self):
        super(TestZerotiersAPI, self).setUp()

        self.lg.info('Get random nodid (N0)')
        self.nodeid = self.get_random_node()
        pyclient_ip = [x['pyclient'] for x in self.nodes_info if x['id'] == self.nodeid][0]
        self.pyclient = Client(pyclient_ip)

        self.lg.info('Join zerotier network (ZT0)')
        self.nwid = self.getZtNetworkID()
        self.body = {"nwid":self.nwid}
        self.zerotier_api.post_nodes_zerotiers(self.nodeid, self.body)

    def tearDown(self):
        self.lg.info('Exit zerotier network (ZT0)')
        self.zerotier_api.delete_nodes_zerotiers_zerotierid(self.nodeid, self.nwid)
        super(TestZerotiersAPI, self).tearDown()

    @unittest.skip('bug: #99')
    def test001_list_node_zerotiers(self):
        """ GAT-001
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Join zerotier network (ZT0).
        #. List node (N0) zerotiers networks, should succeed with 200.
        #. List zerotier networks using python client, (ZT0) should be listed
        """
        self.lg.info('Get node (N0) zerotiers networks, should succeed with 200')
        response = self.zerotier_api.get_nodes_zerotiers(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.nwid, [x['nwid'] for x in response.json()])
        
        self.lg.info('List zerotier networks using python client, (ZT0) should be listed')
        zerotiers = self.pyclient.client.zerotier.list()
        self.assertIn(self.nwid, [x['id'] for x in zerotiers])

    def test002_post_zerotier(self):
        """ GAT-003
        **Test Scenario:**

        #. Get random nodid (N1).
        #. Join zerotier network (ZT1).
        #. List node (N1) zerotier networks, (ZT1) should be listed.
        #. List zerotier networks using python client, (ZT1) should be listed
        #. Leave zerotier network (ZT1), should succeed with 204.
        #. Join invalid zerotier network, should fail with 400.
        """
        self.lg.info('Get random nodid (N1)')
        nodeid = self.get_random_node()

        self.lg.info('Join zerotier network (ZT1)')
        nwid = self.getZtNetworkID()
        body = {"nwid":nwid}
        response = self.zerotier_api.post_nodes_zerotiers(nodeid, body)
        self.assertEqual(response.status_code, 201)

        self.lg.info('List node (N1) zerotier networks, (ZT1) should be listed')
        response = self.zerotier_api.get_nodes_zerotiers(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(nwid, [x['nwid'] for x in response.json()])

        self.lg.info('List zerotier networks using python client, (ZT1) should be listed')
        zerotiers = self.pyclient.client.zerotier.list()
        self.assertIn(nwid, [x['id'] for x in zerotiers])

        self.lg.info('Leave zerotier network (ZT1), should succeed with 204')
        response = self.zerotier_api.delete_nodes_zerotiers_zerotierid(self.nodeid, self.nwid)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Join invalid zerotier network, should fail with 400')
        body = {"nwid":self.rand_str()}
        response = self.zerotier_api.post_nodes_zerotiers(nodeid, body)
        self.assertEqual(response.status_code, 400)

    def test003_leave_zerotier(self):
        """ GAT-004
        **Test Scenario:**

        #. Get random nodid (N0), should succeed.
        #. Join zerotier network (ZT0).
        #. Leave zerotier network (ZT0), should succeed with 204.
        #. List node (N0) zerotier networks, (ZT0) should be gone.
        #. List zerotier networks using python client, (ZT0) should be gone.
        #. Leave nonexisting zerotier network, should fail with 404
        """
        self.lg.info('Leave zerotier network (ZT0), should succeed with 204')
        response = self.zerotier_api.delete_nodes_zerotiers_zerotierid(self.nodeid, self.nwid)
        self.assertEqual(response.status_code, 204)

        self.lg.info('List node (N0) zerotier networks, (ZT0) should be gone')
        response = self.zerotier_api.get_nodes_zerotiers(self.nodeid)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.nwid, [x['nwid'] for x in response.json()])

        self.lg.info('List zerotier networks using python client, (ZT0) should be gone')
        zerotiers = self.pyclient.client.zerotier.list()
        self.assertNotIn(self.nwid, [x['id'] for x in zerotiers])

        self.lg.info('Leave nonexisting zerotier network, should fail with 404')
        response = self.zerotier_api.delete_nodes_zerotiers_zerotierid(self.nodeid, 'fake_zerotier')
        self.assertEqual(response.status_code, 404)
