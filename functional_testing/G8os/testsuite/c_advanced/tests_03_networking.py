from utils.utils import BaseTest
import time
import re
from random import randint


class AdvancedNetworking(BaseTest):

    def __init__(self, *args, **kwargs):
        super(AdvancedNetworking, self).__init__(*args, **kwargs)
        self.check_g8os_connection(AdvancedNetworking)
        containers = self.client.container.find('ovs')
        ovs_exist = [key for key, value in containers.items()]
        if not ovs_exist:
            ovs = self.client.container.create(self.ovs_flist, host_network=True, storage=self.storage, tags=['ovs'])
            self.ovscl = self.client.container.client(ovs)
            time.sleep(2)
            self.ovscl.json('ovs.bridge-add', {"bridge": "backplane"})
            self.ovscl.json('ovs.vlan-ensure', {'master': 'backplane', 'vlan': 2000, 'name': 'vxbackend'})
        else:
            ovs = int(ovs_exist[0])
            self.ovscl = self.client.container.client(ovs)

    def setUp(self):
        super(AdvancedNetworking, self).setUp()
        self.check_g8os_connection(AdvancedNetworking)

    def create_vm(self, name, nic):
        rs = self.client.bash('ls /var/cache/ | grep Images')
        if not rs.get().stdout:
            self.lg('- Make new directory in cash and download machine Image on it')
            rs = self.client.bash('mkdir /var/cache/Images')
            self.assertEqual(rs.get().state, 'SUCCESS')
            rs = self.client.bash('wget {} -P /var/cache/Images'.format(self.kvm_image))
            self.assertEqual(rs.get().state, 'SUCCESS')
            self.image = '/var/cache/Images/Ubuntu.14.04.x64.qcow2'
        self.client.kvm.create(name=name, media=[{'url': self.image}], nics=nic)

    def test001_vxlans_connections(self):
        """ g8os-000
        *Test case for testing vxlans connections*

        **Test Scenario:**
        #. Create container (c1) on a new vxlan bridge (vx1), should succeed
        #. Create container (c2) connected on (vx1) and connect it to default network
        #. Create virtual machine (vm1) on (vx1), should succeed
        #. Create conatiner (c3) on a new vxlan bridge (vx2)
        #. Check that (c2) can reach the internet while (c1) can't
        #. Check if (c1) can reach (c2), should be reachable
        #. Check if (c1) can reach (vm1), should be reachable
        #. Check if (vm1) can reach (c1), should be reachable
        #. Check if (c3) can reach (c1), shouldn't be reachable
        #. Delete the vxlan bridge (vx1), should succeed
        #. Check if (c1) can reach (c2), shouldn't be reachable
        #. Terminate all machines, should succeed
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Create container (c1) on a new vxlan bridge (vx1), should succeed')
        vx1_id = str(randint(10000, 20000))
        c1_ip = '192.168.2.1'
        nic = [{'type': 'vxlan', 'id': vx1_id, 'config': {'cidr': '{}/24'.format(c1_ip)}}]
        c1 = self.client.container.create(root_url=self.root_url, storage=self.storage, nics=nic)
        c1_client = self.client.container.client(c1)

        self.lg('Create container (c2) connected on (vx1) and connect it to default network.')
        c2_ip = '192.168.2.2'
        nic2 = [{'type': 'default'}, {'type': 'vxlan', 'id': vx1_id, 'config': {'cidr': '{}/24'.format(c2_ip)}}]
        c2 = self.client.container.create(root_url=self.root_url, storage=self.storage, nics=nic2)
        c2_client = self.client.container.client(c2)

        #self.lg('Create virtual machine (vm1) on (vx1), should succeed')
        #vm_nic = [{'type': 'vxlan', 'id': vx1_id}]
        #self.create_vm('vm1', vm_nic)

        self.lg('Create conatiner (c3) on a new vxlan bridge (vx2)')
        vx2_id = str(randint(10000, 20000))
        c3_ip = '192.168.2.3'
        nic3 = [{'type': 'vxlan', 'id': vx2_id, 'config': {'cidr': '{}/24'.format(c3_ip)}}]
        c3 = self.client.container.create(root_url=self.root_url, storage=self.storage, nics=nic3)
        c3_client = self.client.container.client(c3)

        self.lg('Check that (c2) can reach the internet while (c1) can\'t')
        r = c2_client.bash('ping -w5 8.8.8.8').get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)
        r = c1_client.bash('ping -w5 8.8.8.8').get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('Check if (c1) can reach (c2), should be reachable')
        r = c1_client.bash('ping -w5 {}'.format(c2_ip)).get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)

        #self.lg('Check if (c1) can reach (vm1), should be reachable')
        #r = c1_client.bash('ping -w5 {}'.format(vm1_ip)).get()
        #self.assertEqual(r.state, 'SUCCESS', r.stdout)

        #self.lg('Check if (vm1) can reach (c1), should be reachable')
        #r = c1_client.bash('ping -w5 {}'.format(c1_ip)).get()
        #self.assertEqual(r.state, 'SUCCESS', r.stdout)

        self.lg('Check if (c3) can reach (c1), shouldn\'t be reachable')
        r = c3_client.bash('ping -w5 {}'.format(c1_ip)).get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('Delete the vxlan bridge (vx1), should succeed')
        vxbridge = 'vxlbr' + vx1_id
        self.ovscl.json('ovs.bridge-del', {"bridge": vxbridge})

        self.lg('Check if (c1) can reach (c2), shouldn\'t be reachable')
        r = c1_client.bash('ping -w5 {}'.format(c2_ip)).get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('Terminate all machines, should succeed')
        self.client.container.terminate(c1)
        self.client.container.terminate(c2)
        self.client.container.terminate(c3)

        self.lg('{} ENDED'.format(self._testID))

    def test002_vlans_connections(self):
        """ g8os-000
        *Test case for testing vlans connections*

        **Test Scenario:**
        #. Create dhcp server on a container
        #. Create container (c1) on a new vxlan bridge (v1), should succeed.
        #. Create container (c2) connected on (v1) and connect it to default network.
        #. Create conatiner (c3) on a new vlan bridge (v2)
        #. Check that (c2) can reach the internet while (c1) can't.
        #. Check if (c1) can reach (c2), should be reachable
        #. Check if (c1) can reach (vm1), should be reachable
        #. Check if (c3) can reach (c1), shouldn't be reachable
        #. Delete the vlan bridge, should succeed
        #. Check if (c1) can reach (c2), shouldn't be reachable
        #. Terminate all machines, should succeed
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Create dhcp server on a container')
        v1_id = str(randint(1, 4094))
        dhcp_ip = '192.168.1.1'
        nic = [{'type': 'default'}, {'type': 'vlan', 'id': v1_id, 'config': {'cidr': '{}/24'.format(dhcp_ip)}}]

        dhcp_c = self.client.container.create(root_url=self.root_url, storage=self.storage, nics=nic)
        dhcp_c_client = self.client.container.client(dhcp_c)
        r = dhcp_c_client.system('apt-get update').get()
        self.assertEqual(r.state, 'SUCCESS')
        r = dhcp_c_client.system('apt-get install -y dnsmasq-base').get()
        self.assertEqual(r.state, 'SUCCESS')
        dhcp_c_client.system('dnsmasq --no-hosts --keep-in-foreground --listen-address=192.168.1.1 --interface=eth0 --dhcp-range=192.168.1.2,192.168.1.3,255.255.0.0 --dhcp-option=6,192.168.1.1 --bind-interfaces --except-interface=lo')

        self.lg('Create container (c1) on a new vlan bridge (v1), should succeed')
        nic1 = [{'type': 'vlan', 'id': v1_id, 'config': {'dhcp': True}}]
        c1 = self.client.container.create(root_url=self.root_url, storage=self.storage, nics=nic1)
        c1_client = self.client.container.client(c1)
        r = c1_client.system('ip a').get()
        c1_ip = re.search(r'192.168.[\d+].[\d+]', r.stdout).group()

        self.lg('Create container (c2) connected on (v1) and connect it to default network.')
        nic2 = [{'type': 'default'}, {'type': 'vlan', 'id': v1_id, 'config': {'dhcp': True}}]
        c2 = self.client.container.create(root_url=self.root_url, storage=self.storage, nics=nic2)
        c2_client = self.client.container.client(c2)
        r = c2_client.system('ip a').get()
        c2_ip = re.search(r'192.168.[\d+].[\d+]', r.stdout).group()

        self.lg('Create conatiner (c3) on a new vlan bridge (v2)')
        v2_id = str(randint(1, 4094))
        c3_ip = '192.168.1.30'
        nic3 = [{'type': 'vlan', 'id': v2_id, 'config': {'cidr': '{}/24'.format(c3_ip)}}]
        c3 = self.client.container.create(root_url=self.root_url, storage=self.storage, nics=nic3)
        c3_client = self.client.container.client(c3)

        self.lg('Check that (c2) can reach the internet while (c1) can\'t')
        r = c2_client.bash('ping -w5 8.8.8.8').get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)
        r = c1_client.bash('ping -w5 8.8.8.8').get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('Check if (c1) can reach (c2), should be reachable')
        r = c1_client.bash('ping -w5 {}'.format(c2_ip)).get()
        self.assertEqual(r.state, 'SUCCESS', r.stdout)

        self.lg('Check if (c3) can reach (c1), shouldn\'t be reachable')
        r = c3_client.bash('ping -w5 {}'.format(c1_ip)).get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('Delete the vlan bridge (v1), should succeed')
        vbridge = 'vlbr' + v2_id
        self.ovscl.json('ovs.bridge-del', {"bridge": vbridge})

        self.lg('Check if (c1) can reach (c2), shouldn\'t be reachable')
        r = c1_client.bash('ping -w5 {}'.format(c2_ip)).get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('Terminate all machines, should succeed')
        self.client.container.terminate(dhcp_c)
        self.client.container.terminate(c1)
        self.client.container.terminate(c2)
        self.client.container.terminate(c3)

        self.lg('{} ENDED'.format(self._testID))

    def test003_vxlan_vlan_connections(self):
        """ g8os-000
        *Test case for testing vxlans-vlans connections*

        **Test Scenario:**
        #. Create container (c1) on a new vxlan bridge (vx1) on new network (N1)
        #. Create container (c2) on a new vlan bridge (v1) on (N1)
        #. Check if (c1) can reach (c2), shouldn't be reachable
        #. Check if (c2) can reach (c1), shouldn't be reachable
        #. Delete both bridges, should succeed
        #. Terminate all machines, should succeed
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Create container (c1) on a new vxlan bridge (vx1) on new network (N1)')
        vx1_id = str(randint(20000, 30000))
        c1_ip = '192.168.3.1'
        nic = [{'type': 'vxlan', 'id': vx1_id, 'config': {'cidr': '{}/24'.format(c1_ip)}}]
        c1 = self.client.container.create(root_url=self.root_url, storage=self.storage, nics=nic)
        c1_client = self.client.container.client(c1)

        self.lg('Create container (c2) on a new vlan bridge (v1) on (N1)')
        v2_id = str(randint(1, 4094))
        c2_ip = '192.168.3.2'
        nic2 = [{'type': 'vlan', 'id': v2_id, 'config': {'cidr': '{}/24'.format(c2_ip)}}]
        c2 = self.client.container.create(root_url=self.root_url, storage=self.storage, nics=nic2)
        c2_client = self.client.container.client(c2)

        self.lg('Check if (c1) can reach (c2), shouldn\'t be reachable')
        r = c1_client.bash('ping -w5 {}'.format(c2_ip)).get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('Check if (c2) can reach (c1), shouldn\'t be reachable')
        r = c2_client.bash('ping -w5 {}'.format(c1_ip)).get()
        self.assertEqual(r.state, 'ERROR', r.stdout)

        self.lg('Delete both bridges, should succeed')
        vxbridge = 'vxlbr' + vx1_id
        vbridge = 'vlbr' + v2_id
        self.ovscl.json('ovs.bridge-del', {"bridge": vxbridge})
        self.ovscl.json('ovs.bridge-del', {"bridge": vbridge})

        self.lg('Terminate all machines, should succeed')
        self.client.container.terminate(c1)
        self.client.container.terminate(c2)

        self.lg('{} ENDED'.format(self._testID))
