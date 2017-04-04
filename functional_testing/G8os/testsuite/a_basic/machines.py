from utils.utils import BaseTest
import time
import unittest
import uuid

class Machinetests(BaseTest):

    def setUp(self):
        super(Machinetests, self).setUp()
        self.check_g8os_connection(Machinetests)

    def test001_create_destroy_list_kvm(self):
        """ g8os-008

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
        VM_name=str(uuid.uuid4())

        self.lg('- Check that it support hardware virtualization ')
        responce = self.client.info.cpu()
        vmx=['vmx'or'svm' in dec['flags'] for dec in responce]
        self.assertTrue(len(vmx)>0)

        self.lg('- Make new directory in cash and download machine Image on it  ')
        self.client.bash('chmod 777 /var/cache && mkdir /var/cache/Images')
        self.client.bash('wget https://stor.jumpscale.org/public/Images/Ubuntu.14.04.x64.qcow2  -P /var/cache/Images')

        self.lg('- Create virtual machine {} , should succeed'.format(VM_name))
        self.client.experimental.kvm.create(name=VM_name,media=[{'url':'/var/cache/Images/Ubuntu.14.04.x64.qcow2'}])

        self.lg('- List all virtual machines and check that VM {} is there '.format(VM_name))
        Vms_list=self.client.experimental.kvm.list()
        self.assertTrue(any(vm['name'] == VM_name for vm in Vms_list))

        self.lg('- create another virtual machine with the same kvm domain ,should fail')
        with self.assertRaises(RuntimeError):
            self.client.experimental.kvm.create(name=VM_name,media=[{'url':'/var/cache/Images/Ubuntu.14.04.x64.qcow2'}])

        self.lg('- Destroy VM {}'.format(VM_name))
        self.client.experimental.kvm.destroy(VM_name)

        self.lg('- List the virtual machines , VM {} should be gone'.format(VM_name))
        Vms_list=self.client.experimental.kvm.list()
        self.assertFalse(any(vm['name'] == VM_name for vm in Vms_list))

        self.lg('- Destroy VM {} again should fail'.format(VM_name))
        with self.assertRaises(RuntimeError):
            self.client.experimental.kvm.destroy(VM_name)

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
        self.lg('{} STARTED'.format(self._testID))
        self.lg('Create a new container (C1)')
        C1 = self.client.container.create(root_url='https://hub.gig.tech/maxux/ubuntu1604.flist',storagt='ardb://hub.gig.tech:16379')
        containers=self.client.container.list()
        self.assertTrue(str(C1) in containers)
