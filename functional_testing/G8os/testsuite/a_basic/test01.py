from utils.utils import BaseTest
#import nose.tools; nose.tools.set_trace()


class BasicTests(BaseTest):
    
    def setUp(self):
        super(BasicTests, self).setUp()

    
    def test001_execute_commands(self):

        """ g8os-001
        *Test case for testing basic commands using  bash and system*

        **Test Scenario:**
        #. Create folder using system 
        #. Check that the folder is created 
        #. Remove the created folder
        """

        self.lg('{} STARTED'.format(self._testID))

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


