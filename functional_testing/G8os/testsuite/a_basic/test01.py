from utils.utils import BaseTest
import time
import unittest
#import nose.tools; nose.tools.set_trace()


class BasicTests(BaseTest):
    
    def setUp(self):
        super(BasicTests, self).setUp()

    
    def test001_execute_commands(self):

        """ g8os-001
        *Test case for testing basic commands using  bash and system*

        **Test Scenario:**
        #. Check if you can ping the remote host, should succeed
        #. Create folder using system 
        #. Check that the folder is created
        #. Remove the created folder
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Check if you can ping the remote host, should succeed')
        rs = self.client.ping()
        self.assertEqual(rs[:4], 'PONG')
 
        self.lg('Create folder using system')
        folder = self.rand_str()
        self.client.system('mkdir {}'.format(folder))
  
        self.lg('Check that the folder is created')
        rs1 = self.client.bash('ls | grep {}'.format(folder))
        rs_ob = rs1.get()
        self.assertEqual(rs_ob.stdout, '{}\n'.format(folder))
        self.assertEqual(rs_ob.state, 'SUCCESS')

        self.lg('Remove the created folder')
        self.client.bash('rm -rf {}'.format(folder))
        rs2 = self.client.bash('ls | grep {}'.format(folder))
        self.assertEqual(rs2.get().stdout, '')

        self.lg('{} ENDED'.format(self._testID))

    @unittest.skip('bug')
    def test002_kill_list_processes(self):

        """ g8os-002
        *Test case for testing killing and listing processes*

        **Test Scenario:**
        #. Create process that runs for long time using both system and bash
        #. List the process, should be found
        #. Kill the process
        #. List the process, shouldn't be found 
        """

        self.lg('{} STARTED'.format(self._testID))
        
        for i in range(2):
            if i == 0:
               cmd = 'core.system'
               match = 'sleep'
               self.client.system('sleep 40')
            else:
               cmd = 'bash'
               match = 'sleep 40'
               self.client.bash('sleep 40')
            self.lg('Created process that runs for long time using {}'.format(cmd))

            self.lg('List the process, should be found')
            id = self.get_process_id(cmd, match)
            self.assertIsNotNone(id)

            self.lg('Kill the process')
            self.client.process.kill(id)

            self.lg('List the process, shouldn\'t be found')
            id = self.get_process_id(cmd, match)
            self.assertIsNone(id)

            self.lg('{} ENDED'.format(self._testID))

    def test003_os_info(self):

        """ g8os-003
        *Test case for checking on the system os information*

        **Test Scenario:**
        #. Get the os information using g8os client
        #. Get the hostname and compare it with the g8os os insformation
        #. Get the kernal's name and compare it with the g8os os insformation
        #. compare the rest of the info ...
        """

        self.lg('{} STARTED'.format(self._testID))
        
        self.lg('Get the os information using g8os client')
        os_info = self.client.info.os()

        self.lg('Get the hostname and compare it with the g8os os insformation') 
        hostname = self.client.system('uname -n').get().stdout.strip()
        self.assertEqual(os_info['hostname'], hostname)

        self.lg('Get the kernal\'s name and compare it with the g8os os insformation') 
        krn_name = self.client.system('uname -s').get().stdout.strip()
        self.assertEqual(os_info['os'], krn_name.lower())

        
        self.lg('{} ENDED'.format(self._testID))

    def test004_mem_info(self):

        """ g8os-004
        *Test case for checking on the system memory information*

        **Test Scenario:**
        #. Get the memory information using g8os client
        #. Get the info using bash and compare it to that of g8os client(write detailed scenario here)
        """

    def test005_cpu_info(self):

        """ g8os-005
        *Test case for checking on the system CPU information*

        **Test Scenario:**
        #. Get the CPU information using g8os client
        #. Get the info using bash and compare it to that of g8os client
        """
        self.lg('get cpu info using bash')
        expected_cpu_info = self.getCpuInfo()
        self.lg('get cpu info using g8os')
        g8os_cpu_info = self.client.info.cpu()
        for key in expected_cpu_info.keys():
                items_list = [x[key] for x in g8os_cpu_info]
                self.assertEqual(expected_cpu_info[key], items_list, "error in parameter %s : %s != %s" % (key,str(items_list),str(expected_cpu_info[key])))

    def test006_disk_info(self):

        """ g8os-006
        *Test case for checking on the disks information*

        **Test Scenario:**
        #. Get the disks information using g8os client
        #. Get the info using bash and compare it to that of g8os client
        """
        self.lg('get disks info using linux bash command (mount)')
        expected_disk_info = self.getDiskInfo()
        self.lg('get cpu info using g8os')
        g8os_disk_info = self.client.info.disk()
        for key in expected_disk_info.keys():
                items_list = [x[key] for x in g8os_disk_info]
                self.assertEqual(expected_disk_info[key], items_list, "error in parameter %s : %s != %s" % (key,str(items_list),str(expected_disk_info[key])))



    def test007_nic_info(self):

        """ g8os-007
        *Test case for checking on the system nic information*

        **Test Scenario:**
        #. Get the nic information using g8os client
        #. Get the info using bash and compare it to that of g8os client(write detailed scenario here)
        """

    def test008_create_destroy_list_kvm(self):
        """ g8os-008
        *Test case for testing creating, listing and destroying VMs*

        **Test Scenario:**
        #. Create virtual machine (VM1), should succeed
        #. List all virtual machines and check that VM1 is there
        #. Create another virtual machine with the same kvm domain, should fail
        #. Destroy VM1, should succeed
        #. List the virtual machines, VM1 should be gone
        #. Destroy VM1 again, should fail
        """

    def test009_create_list_delete_containers(self):
        """ g8os-009
        *Test case for testing creating, listing and deleting containers*

        **Test Scenario:**
        #. Create a new container (C1), should succeed
        #. List all containers and check that C1 is there
        #. Get client, execute command and check on the result (write more details)
        #. Destroy C1, should succeed
        #. List the containers, C1 should be gone
        #. Destroy C1 again, should fail
        """ 

    def test010_join_leave_list_zerotier(self):
        """ g8os-010
        *Test case for testing joining, listing, leaving zerotier networks*

        **Test Scenario:**
        #. Join zerotier network (N1), should succeed
        #. List zerotier network
        #. Leave zerotier network (N1),should succeed
        #. List zerotier networks, N1 should be gone 
        #. Leave zerotier network (N1), should fail
        #. ref: https://www.zerotier.com/manual.shtml .. please all possible missing steps .. also add extended scenario to test zerotier functionality
        """

    def test011_create_delete_list_bridges(self):
        """ g8os-011
        *Test case for testing creating, listing, deleting bridges*

        **Test Scenario:**
        #. Create bridge (B1), should succeed 
        #. List  bridges, B1 should be listed 
        #. Delete bridge B1, should succeed
        #. List bridges, B1 should be gone
        #. Delete bridge B1, should fail
        .... please add extended scenario to test bridges functionality 
        """


 

