from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.utils.utils import BaseTest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import leftNavigationMenu
import time
import uuid

class users(BaseTest):
    def __init__(self, *args, **kwargs):
        super(users, self).__init__(*args, **kwargs)

    def IsAt(self):
        for temp in range(5):
            if self.get_text("users_page") == "Users":
                return True
            else:
                time.sleep(0.5)
        else:
            return False

    def create_new_user(self, username='', password='', email='', group=''):
        username = username or str(uuid.uuid4()).replace('-', '')[0:10]
        password = password or str(uuid.uuid4()).replace('-', '')[0:10]
        email = email or str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        group = group or 'user'

        leftNavigationMenu.CloudBroker.Users()

        self.click("add_user")
        self.assertTrue(self.check_element_is_exist("create_user"))

        self.set_text("username", username)
        self.set_text("mail", email)
        self.set_text("password", password)

        xpath_user_group = ''
        for i in range(1, 100):
            xpath_user_group = self.elements["user_group"] % i
            if group == self.driver.find_element_by_xpath(xpath_user_group).text:
                break
        user_group = self.driver.find_element_by_xpath(xpath_user_group)
        if not user_group.is_selected():
            user_group.click()

        self.click("confirm_add_user")
        time.sleep(1)
        self.set_text("username_search", username)
        self.wait_until_element_located_and_has_text(self.elements["username_table_first"], username)
        self.CLEANUP["users"].append(username)

    def open_user_page(self, username=''):
        username = username
        leftNavigationMenu.CloudBroker.Users()

        self.set_text("username_search", username)
        self.wait_until_element_located_and_has_text(self.elements["username_table_first"], username)
        username_id = self.get_text("username_table_first")

        self.click("username_table_first")
        self.element_in_url(username_id)

    def delete_user(self, username):
        leftNavigationMenu.CloudBroker.Users()

        self.set_text("user_search", username)
        self.lg("check if this user is exist")
        if self.wait_until_element_located_and_has_text(self.elements["username_table_first"],username):
            self.lg("Delete %s user" % username)
            time.sleep(1)
            self.assertEqual(self.get_text("user_table_first_element"),username)
            self.click("user_table_first_element")
            self.assertEqual(self.get_text("user_name")[6:],username)
            self.click("user_action")
            self.click("user_delete")
            self.click("user_delete_confirm")
            self.CLEANUP["users"].remove(username)
            return True
        else:
            self.lg("There is no %s user" % username)
            return False