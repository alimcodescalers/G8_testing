from utils.utils import BaseTest
import time
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

    def test003_os_mem_info(self):

        """ g8os-003
        *Test case for checking on the memory and os information*

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
        hostname = self.client.system('uname -n')
        self.assertEqual(os_info['hostname'], stdout(hostname))

        self.lg('Get the kernal\'s name and compare it with the g8os os insformation') 
        krn_name = self.client.system('uname -s')
        self.assertEqual(os_info['os'], stdout(krn_name))

        
        self.lg('{} ENDED'.format(self._testID))

        
