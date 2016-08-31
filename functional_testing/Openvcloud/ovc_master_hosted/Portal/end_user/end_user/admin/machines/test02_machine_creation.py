from .....utils.utils import BaseTest
from ...page_elements_xpath import machines_page
import time
import uuid
from nose_parameterized import parameterized
from random import randint
import unittest

class Read(BaseTest):
    def __init__(self, *args, **kwargs):
        super(Read, self).__init__(*args, **kwargs)
        self.elements.update(machines_page.elements)

    def setUp(self):
        super(Read, self).setUp()
        self.login()

    def test01_machine_get(self):
        """
        *Test case for get machine.*

        **Test Scenario:**

        #. create new machine, should succeed
        #. get machine, should succeed
        """

    def test02_machine_list(self):
        """
        *Test case for list machine.*

        **Test Scenario:**

        #. create new machine, should succeed
        #. list machines should see 1 machine, should succeed
        """
        pass

    def test03_machine_getConsoleUrl(self):
        """
        *Test case for getConsoleUrl machine.*

        **Test Scenario:**

        #. create new machine, should succeed
        #. getConsoleUrl machine, should succeed
        """
        pass

    def test04_machine_listSnapshots(self):
        """
        *Test case for listSnapshots machine.*

        **Test Scenario:**

        #. create snapshot for a machine with the account user, should succeed
        #. try to listSnapshots of created machine with new user [user], should return 403
        #. add user to the machine with read access
        #. listSnapshots of created machine with new user [user], should succeed
        """
        pass

    def test05_machine_getHistory(self):
        """
        *Test case for getHistory machine.*

        **Test Scenario:**

        #. create new machine, should succeed
        #. getHistory of created machine, should succeed
        """
        pass


    '''
    @parameterized.expand(["ubuntu_14_04",
                           "ubuntu_15_10",
                           "ubuntu_16_04",
                           "windows_2012"
                           ])
    '''
    @unittest.skip("bug #346")
    def test06_machine_create(self, image_name="ubuntu_14_04"):
        """ PRTL-011
        *Test case for creating/deleting machine with all avaliable image name, random package and random disk size*

        **Test Scenario:**

        #. create new machine, should succeed
        #. delete the new machine
        
        """
        self.lg('%s STARTED' % self._testID)
        #self.driver.find_element_by_xpath(self.elements["machines_button"]).click
        #self.driver.find_element_by_xpath(self.elements["machines_button"]).click
        self.click("machines_button")
        self.click("create_machine_button")

        self.machine_name = str(uuid.uuid4()).replace('-', '')[0:10]
        self.machine_description = str(uuid.uuid4()).replace('-', '')[0:10]
        randome_package = randint(1, 6)
        if image_name != "windows_2012":
            random_disk_size = randint(1, 8)
        else:
            random_disk_size = randint(1, 6)
            self.click("windows")

        self.lg("Create a machine name: %s image:%s" % (self.machine_name, image_name))
        self.set_text("machine_name", self.machine_name)
        self.set_text("machine_description_", self.machine_description)
        self.click(image_name)
        self.click("package_%i" % randome_package)
        self.click("disk_size_%i" % random_disk_size)

        self.click("create_machine")
        #time.sleep(20)
        self.assertEqual(self.get_text("machine_status"), "RUNNING")

        self.lg("Destroy the machine")
        self.click("destroy_machine")
        self.click("destroy_machine_confirm")
        time.sleep(10)
        self.assertEqual(self.get_text("machine_list"),"Machines")
        self.lg('%s ENDED' % self._testID)
