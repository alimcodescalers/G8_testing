from end_user.utils import BaseTest
from end_user.page_elements_xpath import home_page
from selenium.common.exceptions import NoSuchElementException
import uuid

class ChangePassword(BaseTest):

    def __init__(self, *args, **kwargs):
        super(ChangePassword, self).__init__(*args, **kwargs)
        self.elements.update(users_page.elements)

    def setUp(self):
        super(ChangePassword, self).setUp()
        self.login()
        if not self.check_element_is_exist("left_menu"):
            self.click("left_menu_button")
        self.click("cloud_broker")
        self.click("users")

    def test01_create_new_user(self):
        """ PRTL-010
        *Test case for create new user.*

        **Test Scenario:**

        #. create new user.
        """
        self.lg('%s STARTED' % self._testID)
        self.click("add_user")
        self.assertTrue(self.check_element_is_exist("Create User"))
        self.username = str(uuid.uuid4()).replace('-', '')[0:10]
        self.password = str(uuid.uuid4()).replace('-', '')[0:10]
        self.email = str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        self.set_text("username",self.username)
        self.set_text("mail",self.email)
        self.set_text("password",self.password)
        while True:
            i = 1
            xpath = "id('createuser')/x:div/x:div[2]/x:div[3]/x:div[4]/x:label[%d]" % i
            if "user" == self.driver.find_element_by_xpath(xpath).text:
                break
            i+=1
            # safe from infinte loop
            if i == 100:
                raise NameError("The group's list isn't contain a user")

        user_group = self.driver.find_element_by_xpath(xpath)
        if not user_group.is_selected():
            user_group.click()

        self.click("confirm_add_user")

    def test02_logout(self):
