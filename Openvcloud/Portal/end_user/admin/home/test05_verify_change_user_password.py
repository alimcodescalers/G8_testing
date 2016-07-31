from end_user.utils import BaseTest
from end_user.page_elements_xpath import users_page
from selenium.common.exceptions import NoSuchElementException
import uuid

class ChangePassword(BaseTest):

    def __init__(self, *args, **kwargs):
        super(ChangePassword, self).__init__(*args, **kwargs)
        self.elements.update(users_page.elements)

    def setUp(self):
        super(ChangePassword, self).setUp()
        self.login()
        if self.check_element_is_exist("left_menu")==False:
            self.click("left_menu_button")

    def test01_verify_change_user_password(self):
        """ PRTL-010
        *Test case for create new user and change his password*

        **Test Scenario:**
        #. Create new user
        #. Login using this user
        #. Change his password
        #. Logout
        #. Login using this user and the new password
        #. Logout
        #. Login as admin
        #. Delete this user
        """
        self.lg('%s STARTED' % self._testID)
        self.username = str(uuid.uuid4()).replace('-', '')[0:10]
        self.password = str(uuid.uuid4()).replace('-', '')[0:10]
        self.email = str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        self.group = 'user'

        self.lg('Create new username, user:%s password:%s' % (self.username,self.password))
        self.create_new_user(self.username,self.password,self.email,self.group)

        self.lg('Do logout')
        self.click("admin_logout_button")

        self.lg("login using the new account")
        self.login(self.username,self.password)

        self.lg("check access denied")
        if self.check_element_is_exist("access_denied") == True:
            self.driver.get(self.environment_url)

        self.lg("Change the password")
        self.click("user_profile")
        self.set_text("current_pw",self.password)
        self.newPassword = str(uuid.uuid4()).replace('-', '')[0:10]
        self.set_text("new_pw_1",self.newPassword)
        self.set_text("new_pw_2",self.newPassword)
        self.click("update_password")

        self.lg("Do logout")
        self.click("end_user_logout")

        self.lg("Login using new password")
        self.login(self.username,self.newPassword)
        self.driver.get(self.environment_url)
        self.click("user_profile")
        self.assertEqual(self.get_text("profile"),"Profile")

        self.lg("Do logout")
        self.click("end_user_logout")

    def tearDown(self):
        self.lg("login as admin")
        self.login()

        self.lg("Delete the user")
        self.assertTrue(self.delete_user(self.username))
        super(ChangePassword, self).tearDown()