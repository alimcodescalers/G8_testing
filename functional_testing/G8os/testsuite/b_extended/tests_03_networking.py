from utils.utils import BaseTest
import time
import unittest


class ExtendedNetworking(BaseTest):

    def setUp(self):
        super(ExtendedNetworking, self).setUp()
        self.check_g8os_connection(ExtendedNetworking)

    @unittest.skip('bug# https://github.com/g8os/core0/issues/126')
    def test001_zerotier(self):
        """ g8os-014
        *Test case for testing zerotier functionally*

        **Test Scenario:**
        #. Get NetworkId (N1) using zerotier API
        #. G8os client join zerotier network (N1)
        #. Create 2 containers c1, c2 and make them join (N1)
        #. Get g8os and containers zerotier ip addresses
        #. Container c1 ping g8os client, should succeed
        #. Container c1 ping Container c2, should succeed
        #. Container c2 ping g8os client, should succeed
        #. Container c2 ping Container c1, should succeed
        #. G8os client ping Container c1, should succeed
        #. G8os client ping Container c2, should succeed
        #. G8os client leave zerotier network (N1), should succeed
        #. G8os client ping Container c1, should fail
        #. G8os client ping Container c2, should fail
        #. Terminate containers c1, c2
        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('Get NetworkId using zerotier API')
        networkId = self.getZtNetworkID()

        self.lg('Join zerotier network (N1)')
        self.client.zerotier.join(networkId)

        self.lg('Create 2 containers c1, c2 and make them join (N1) && create there clients')
        cid_1 = self.client.container.create(root_url=self.root_url, storage=self.storage, zerotier=networkId)
        cid_2 = self.client.container.create(root_url=self.root_url, storage=self.storage, zerotier=networkId)
        c1_client = self.client.container.client(cid_1)
        c2_client = self.client.container.client(cid_2)

        time.sleep(40)

        self.lg('Get g8os and containers zerotier ip addresses')
        g8_ip = self.get_g8os_zt_ip(networkId)
        c1_ip = self.get_contanier_zt_ip(c1_client)
        c2_ip = self.get_contanier_zt_ip(c2_client)

        self.lg('set client time to 100 sec')
        self.client.timeout = 100

        self.lg('Container c1 ping g8os client (ip : {}), should succeed'.format(g8_ip))
        r = c1_client.bash('ping -w10 {}'.format(g8_ip)).get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)

        self.lg('Container c1 ping Container c2 (ip : {}), should succeed'.format(c2_ip))
        r = c1_client.bash('ping -w10 {}'.format(c2_ip)).get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)

        self.lg('Container c2 ping g8os client (ip : {}), should succeed'.format(g8_ip))
        r = c2_client.bash('ping -w10 {}'.format(g8_ip)).get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)

        self.lg('Container c2 ping Container c1 (ip : {}), should succeed'.format(c1_ip))
        r = c2_client.bash('ping -w10 {}'.format(c1_ip)).get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)

        self.lg('G8os client ping Container c1 (ip : {}), should succeed'.format(c1_ip))
        r = self.client.bash('ping -w10 {}'.format(c1_ip)).get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)

        self.lg('G8os client ping Container c2 (ip : {}), should succeed'.format(c2_ip))
        r = self.client.bash('ping -w10 {}'.format(c2_ip)).get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)

        self.lg('G8os client leave zerotier network (N1), should succeed')
        self.client.zerotier.leave(networkId)
        time.sleep(5)

        self.lg('G8os client ping Container c1 (ip : {}), should fail'.format(c1_ip))
        r = self.client.bash('ping -w10 {}'.format(c1_ip)).get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('G8os client ping Container c2 (ip : {}), should fail'.format(c2_ip))
        r = self.client.bash('ping -w10 {}'.format(c2_ip)).get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('Terminate c1, c2')
        self.client.container.terminate(cid_1)
        self.client.container.terminate(cid_2)

        self.lg('{} ENDED'.format(self._testID))


    # def test002_bridges(self):
    #     pass
