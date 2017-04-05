from utils.utils import BaseTest
import time
import unittest
import uuid


class Machinetests(BaseTest):

    def setUp(self):
        super(Machinetests, self).setUp()
        self.check_g8os_connection(Machinetests)

    def test001_create_destroy_list_kvm(self):
        """ g8os-009

        *Test case for testing creating, listing and destroying VMs*

        **Test Scenario:**

        #. Check that system support hardware virtualization
        #. Create virtual machine (VM1), should succeed
        #. List all virtual machines and check that VM1 is there
        #. Create another virtual machine with the same kvm domain, should fail
        #. Destroy VM1, should succeed
        #. List the virtual machines, VM1 should be gone
        #. Destroy VM1 again, should fail

        """
        self.lg('{} STARTED'.format(self._testID))
        VM_name = self.rand_str()

        self.lg('- Check that it support hardware virtualization ')
        responce = self.client.info.cpu()
        vmx = ['vmx'or'svm' in dec['flags'] for dec in responce]
        self.assertGreater(len(vmx), 0)

        self.lg('- Make new directory in cash and download machine Image on it')
        rs = self.client.bash('mkdir /var/cache/Images')
        result = rs.get()
        self.assertEqual(result.state, 'SUCCESS')
        rs = self.client.bash('wget https://stor.jumpscale.org/public/Images/Ubuntu.14.04.x64.qcow2  -P /var/cache/Images')
        result = rs.get()
        self.assertEqual(result.state, 'SUCCESS')

        self.lg('- Create virtual machine {} , should succeed'.format(VM_name))
        self.client.experimental.kvm.create(name=VM_name, media=[{'url': '/var/cache/Images/Ubuntu.14.04.x64.qcow2'}])

        self.lg('- List all virtual machines and check that VM {} is there '.format(VM_name))
        Vms_list = self.client.experimental.kvm.list()
        self.assertTrue(any(vm['name'] == VM_name for vm in Vms_list))

        self.lg('- create another virtual machine with the same kvm domain ,should fail')
        with self.assertRaises(RuntimeError):
            self.client.experimental.kvm.create(name=VM_name, media=[{'url': '/var/cache/Images/Ubuntu.14.04.x64.qcow2'}])

        self.lg('- Destroy VM {}'.format(VM_name))
        self.client.experimental.kvm.destroy(VM_name)

        self.lg('- List the virtual machines , VM {} should be gone'.format(VM_name))
        Vms_list = self.client.experimental.kvm.list()
        self.assertFalse(any(vm['name'] == VM_name for vm in Vms_list))

        self.lg('- Destroy VM {} again should fail'.format(VM_name))
        with self.assertRaises(RuntimeError):
            self.client.experimental.kvm.destroy(VM_name)

        self.lg('- Delete created directory, should succeed')
        rs = self.client.bash('rm -r  /var/cache/Images')
        result = rs.get()
        self.assertEqual(result.state, 'SUCCESS')

        self.lg('{} ENDED'.format(self._testID))

    @unittest.skip('bug# https://github.com/g8os/core0/issues/123')
    def test002_create_list_delete_containers(self):
        """ g8os-010
        *Test case for testing creating, listing and deleting containers*

        **Test Scenario:**
        #. Create a new container (C1), should succeed
        #. List all containers and check that C1 is there
        #. Destroy C1, should succeed
        #. List the containers, C1 should be gone
        #. Destroy C1 again, should fail

        """
        self.lg('{} STARTED'.format(self._testID))
        self.lg('Create a new container (C1)')
        C1 = self.client.container.create(root_url=self.root_url, storage=self.storage)

        self.lg('List all containers and check that C1 {}is there'.format(C1))
        containers = self.client.container.list()
        self.assertTrue(str(C1) in containers)

        self.lg('Destroy C1 {}, should succeed'.format(C1))
        res = self.client.container.terminate(C1)
        self.assertEqual(res, None)

        self.lg('List the containers, C1 {} should be gone'.format(C1))
        time.sleep(0.5)
        containers = self.client.container.list()
        self.assertFalse(str(C1) in containers)

        self.lg('Destroy C1 again, should fail')
        with self.assertRaises(RuntimeError):
            self.client.container.terminate(C1)

        self.lg('{} ENDED'.format(self._testID))

    def test003_deal_with_container_client(self):
        """ g8os-011

        *Test case for testing dealing with container client*

        **Test Scenario:**

        #. Create a new container (C1), should succeed
        #. Get container(C1) client
        #. Use container client  to create  folder using system, should succeed
        #. Use container client to check folder is exist using bash
        #. Use G8os client to check the folder is created only in container
        #. Use container client to delete created folder
        #. Destroy C1, should succeed

        """
        self.lg('{} STARTED'.format(self._testID))
        self.lg('Create a new container (C1), and make sure its exist')
        C1 = self.client.container.create(root_url=self.root_url, storage=self.storage)
        containers = self.client.container.list()
        self.assertTrue(str(C1) in containers)

        self.lg('Get container client(C1)')
        C1_client = self.client.container.client(C1)

        self.lg('Use container client  to create  folder using system, should succeed')
        folder = self.rand_str()
        C1_client.system('mkdir {}'.format(folder))
        time.sleep(0.5)

        self.lg('Use container client to check folder is exist using bash')
        output = C1_client.bash('ls | grep {}'.format(folder))
        result = output.get()
        self.assertEqual(result.stdout, '{}\n'.format(folder))
        self.assertEqual(result.state, 'SUCCESS')

        self.lg('Check that the folder is created only in container')
        output2 = self.client.bash('ls | grep {}'.format(folder))
        self.assertEqual(self.stdout(output2), '')

        self.lg('Remove the created folder using bash,check that it removed ')
        C1_client.bash('rm -rf {}'.format(folder))
        time.sleep(0.5)
        output = self.client.bash('ls | grep {}'.format(folder))
        self.assertEqual(self.stdout(output), '')

        self.lg('{} ENDED'.format(self._testID))
