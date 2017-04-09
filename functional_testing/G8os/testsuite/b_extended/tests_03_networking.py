from utils.utils import BaseTest
import time
import unittest
from random import randint


class ExtendedNetworking(BaseTest):

    def setUp(self):
        super(ExtendedNetworking, self).setUp()
        self.check_g8os_connection(ExtendedNetworking)

    def rand_mac_address(self):
        mac_addr = ["{:02X}".format(randint(0, 255)) for x in range(6)]
        return ':'.join(mac_addr)


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

    @unittest.skip('bug: https://github.com/g8os/core0/issues/127')
    def test002_create_bridges_with_specs_hwaddr(self):

        """ g8os-023
        *Test case for testing creating, listing, deleting bridges*

        **Test Scenario:**
        #. Create bridge (B1) with specifice hardware address (HA), should succeed
        #. List bridges, (B1) should be listed
        #. Check the created bridge hardware address equal to (HA), should succeed
        #. Delete bridge (B1), should succeed
        #. Create bridge (B2) with invalid hardware address, should fail

        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('Create bridge (B1) with specifice hardware address (HA), should succeed')
        bridge_name = self.rand_str()
        hardwareaddr = self.rand_mac_address()
        self.client.bridge.create(bridge_name, hwaddr=hardwareaddr)

        self.lg('List bridges, (B1) should be listed')
        bridges = self.client.bridge.list()
        self.assertIn(bridge_name, bridges)

        self.lg('Check the created bridge hardware address equal to (HA), should succeed')
        nics = self.client.info.nic()
        nic_names = [x['name'] for x in nics]
        self.assertIn(bridge_name, nic_names)
        for nic in nics:
            if nic['name'] == bridge_name:
                self.assertEqual(nic['hardwareaddr'], hardwareaddr)

        self.lg('Delete bridge (B1), should succeed')
        self.client.bridge.delete(bridge_name)
        bridges = self.client.bridge.list()
        self.assertNotIn(bridge_name, bridges)

        self.lg('Create bridge (B2) with invalid hardware address, should fail')
        bridge_name = self.rand_str()
        hardwareaddr = self.rand_str()
        with self.assertRaises(RuntimeError):
            self.client.bridge.create(bridge_name, hwaddr=hardwareaddr)

        self.lg('{} ENDED'.format(self._testID))


    def test003_create_bridges_with_specs_network(self):
        """ g8os-024
        *Test case for testing creating, listing, deleting bridges*

        **Test Scenario:**
        #. Create bridge (B1) with static network and cidr (C1), should succeed
        #. Check the created bridge addresses contains cidr (C1), should succeed
        #. Delete bridge (B1), should succeed
        #. Create bridge with invalid cidr, should fail
        #. Create bridge (B2) with dnsmasq network and cidr (C2), should succeed
        #. Check the bridge (B2) addresses contains cidr (C2), should succeed
        #. Delete bridge (B2), should succeed

        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('Create bridge (B1) with static network and cidr (C1), should succeed')
        bridge_name = self.rand_str()
        cidr = "10.20.30.1/24"
        settings = {"cidr":cidr}
        self.client.bridge.create(bridge_name, network='static', settings=settings)

        self.lg('Check the created bridge addresses contains cidr (C1), should succeed')
        nics = self.client.info.nic()
        nic_names = [x['name'] for x in nics]
        self.assertIn(bridge_name, nic_names)
        for nic in nics:
            if nic['name'] == bridge_name:
                addrs = [x['addr'] for x in nic['addrs']]
                self.assertIn(cidr, addrs)

        self.lg('Delete bridge (B1), should succeed')
        self.client.bridge.delete(bridge_name)
        bridges = self.client.bridge.list()
        self.assertNotIn(bridge_name, bridges)

        self.lg('Create bridge with invalid cidr, should fail')
        bridge_name = self.rand_str()
        cidr = "10.20.30.1"
        settings = {"cidr":cidr}
        with self.assertRaises(RuntimeError):
            self.client.bridge.create(bridge_name, network='static', settings=settings)

        self.lg('Create bridge (B2) with dnsmasq network and cidr (C2), should succeed')
        bridge_name = self.rand_str()
        cidr = "10.20.30.1/24"
        start = "10.20.30.2"
        end = "10.20.30.3"
        settings = {"cidr":cidr, "start":start, "end":end}
        self.client.bridge.create(bridge_name, network='dnsmasq', settings=settings)

        self.lg('Check the bridge (B2) addresses contains cidr (C2), should succeed')
        nics = self.client.info.nic()
        nic_names = [x['name'] for x in nics]
        self.assertIn(bridge_name, nic_names)
        for nic in nics:
            if nic['name'] == bridge_name:
                addrs = [x['addr'] for x in nic['addrs']]
                self.assertIn(cidr, addrs)

        self.lg('Delete bridge (B2), should succeed')
        self.client.bridge.delete(bridge_name)
        bridges = self.client.bridge.list()
        self.assertNotIn(bridge_name, bridges)

        self.lg('{} ENDED'.format(self._testID))
