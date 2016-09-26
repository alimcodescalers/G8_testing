import time
from random import randint
from selenium.common.exceptions import TimeoutException
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.utils.utils import BaseTest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.accounts import accounts
import uuid

class cloudspaces(BaseTest):
    def __init__(self, *args, **kwargs):
        super(cloudspaces, self).__init__(*args, **kwargs)

    def create_cloud_space(self, account, cloud_space=''):
        account = account
        self.cloud_space_name = cloud_space or str(uuid.uuid4()).replace('-', '')[0:10]

        accounts().open_account_page(account)
        account_username = self.get_text("account_first_user_name")

        self.click("add_cloudspace")

        self.assertEqual(self.get_text("create_cloud_space"), "Create Cloud Space")

        self.set_text("cloud_space_name", self.cloud_space_name)
        self.set_text("cloud_space_user_name", account_username)

        self.click("cloud_space_confirm")

        self.set_text("cloud_space_search", self.cloud_space_name)
        self.wait_until_element_located_and_has_text(self.elements["cloud_space_table_first_element_2"],
                                                     self.cloud_space_name)
        self.lg(" %s cloudspace is created" % self.cloud_space_name)
        return self.cloud_space_name

    def open_cloudspace_page(self, cloudspace=''):
        cloudspace = cloudspace
        leftNavigationMenu.CloudBroker.CloudSpaces()
        self.set_text("cloud_space_search", cloudspace)
        self.wait_until_element_located_and_has_text(self.elements["cloud_space_table_first_element_2"],
                                                     cloudspace)
        cloudspace_id = self.get_text("cloud_space_table_first_element_1")
        self.click("cloud_space_table_first_element_1")
        self.element_in_url(cloudspace_id)

    def delete_cloudspace(self, cloudspace=''):
        cloudspace = cloudspace

        self.lg('open %s cloudspace' % cloudspace)
        self.open_cloudspace_page(cloudspace)
        if self.driver.find_element_by_xpath(self.elements["cloudspace_page_status"]).text != "DESTROYED":
            self.lg('delete "%s" cloudspace' % cloudspace)
            self.click('cloudspace_action')
            if self.driver.find_element_by_xpath(self.elements["cloudspace_page_status"]).text == "DEPLOYED":
                self.click('cloudspace_delete_deployed')
            elif self.driver.find_element_by_xpath(self.elements["cloudspace_page_status"]).text == "VIRTUAL":
                self.click('cloudspace_delete_virtual')

            self.set_text('cloudspace_delete_reason', "Test")
            self.click("cloudspace_delete_confirm")
            time.sleep(0.5)
            self.get_page(self.driver.current_url)
            for temp in range(10):
                try:
                    self.wait_until_element_located_and_has_text(self.elements["cloudspace_page_status"], "DESTROYED")
                    return True
                except TimeoutException:
                    time.sleep(1)
                    self.get_page(self.driver.current_url)
            else:
                self.fail("Can't delete this '%s' cloudspcae")
        else:
            self.lg('"%s" cloudspace is already deleted' % cloudspace)
            return True