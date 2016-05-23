from utils.utils import BasicACLTest

from nose_parameterized import parameterized


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
