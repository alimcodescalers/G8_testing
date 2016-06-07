# coding=utf-8
from nose_parameterized import parameterized
from Openvcloud.utils.utils import BasicACLTest


class ExtendedTests(BasicACLTest):

    def setUp(self):
        super(ExtendedTests, self).setUp()
        self.default_setup()

    @parameterized.expand(['Ubuntu 14.04 x64'])
    def test001_create_vmachine_with_all_disks(self, image_name):
        """ OVC-013
        *Test case for create machine with Linux image available.*

        **Test Scenario:**

        #. validate the image is exists, should succeed
        #. get all available sizes to use, should succeed
        #. create machine using given image with specific size and all available disk sizes, should succeed
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('1- validate the image is exists, should succeed')
        images = self.api.cloudapi.images.list()
        self.assertIn(image_name,
                      [image['name'] for image in images],
                      'Image [%s] not found in the environment available images' % image_name)
        image = [image for image in images if image['name'] == image_name][0]

        self.lg('2- get all available sizes to use, should succeed')
        sizes = self.api.cloudapi.sizes.list(cloudspaceId=self.cloudspace_id)
        self.lg('- using image [%s]' % image_name)
        for size in sizes:
            self.lg('- using image [%s] with memory size [%s]' % (image_name, size['memory']))
            for disk in size['disks']:
                self.lg('- using image [%s] with memory size [%s] with disk '
                        '[%s]' % (image_name, size['memory'], disk))
                machine_id = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id,
                                                          size_id=size['id'],
                                                          image_id=image['id'],
                                                          disksize=disk)
                self.lg('- done using image [%s] with memory size [%s] with disk '
                        '[%s]' % (image_name, size['memory'], disk))
                self.lg('- delete machine to free environment resources, should succeed')
                self.api.cloudapi.machines.delete(machineId=machine_id)

        self.lg('%s ENDED' % self._testID)


    def test002_node_maintenance_stopVMs(self):
        """ OVC-xxx
        *Test case for putting node in maintenance with action stop all vms.*

        **Test Scenario:**

        #. create 2 VMs, should succeed
        #. put node in maintenance with action stop all vms, should succeed
        #. check that the 2 VMs have been halted
        #. enable the node back, should succeed
        #. check that the 2 VMs have returned to running status
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('- get a running node to create VMs on')
        stackId = self.get_running_stackId()
        self.assertNotEqual(stackId, -1, msg="No active node to create VMs on")

        self.lg('- create 2 VMs, should succeed')
        machine_Id1 = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id,
                                                   onStack=True, stackId=stackId)
        machine_Id2 = self.cloudapi_create_machine(cloudspace_id=self.cloudspace_id,
                                                   onStack=True, stackId=stackId)


        self.lg('- put node in maintenance with action stop all vms, should succeed')
        gid = self.get_node_gid(stackId)
        self.api.cloudbroker.computenode.maintenance(id=stackId, gid=gid, vmaction='stop', message='testing')

        self.lg('- check that the 2 VMs have been halted')
        machine_1 = self.api.cloudapi.machines.get(machineId=machine_Id1)
        self.wait_for_status('HALTED', self.api.cloudapi.machines.get, machineId=machine_1)
        self.assertEqual(machine_1['status'], 'HALTED')
        machine_2 = self.api.cloudapi.machines.get(machineId=machine_Id1)
        self.wait_for_status('HALTED', self.api.cloudapi.machines.get, machineId=machine_2)
        self.assertEqual(machine_2['status'], 'HALTED')

        self.lg('- enable the node back, should succeed')
        self.api.cloudbroker.computenode.enable(id=stackId, gid=gid, message='testing')

        self.lg('check that the 2 VMs have returned to running status')
        machine_1 = self.api.cloudapi.machines.get(machineId=machine_Id1)
        self.assertEqual(machine_1['status'], 'RUNNING')
        machine_2 = self.api.cloudapi.machines.get(machineId=machine_Id1)
        self.assertEqual(machine_2['status'], 'RUNNING')

        self.lg('%s ENDED' % self._testID)


