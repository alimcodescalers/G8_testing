from admin_portal.utils import BaseTest
from admin_portal.page_elements_xpath import account_page
import time
import uuid
from nose_parameterized import parameterized
from random import randint


class Account(BaseTest):
    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)
        self.elements.update(account_page.elements)

    def setUp(self):
        super(Account, self).setUp()
        self.login()
        if self.check_element_is_exist("left_menu") == False:
            self.click("left_menu_button")
        self.driver.implicitly_wait(20)

    def test01_create_account(self):
        """ PRTL-010
        *Test case for create new user and change his password*

        **Test Scenario:**
        #. Create new user
        #. create new account
        #. open the account page
        #. create new cloudspace
        #. open cloudspace page
        """
        self.username = str(uuid.uuid4()).replace('-', '')[0:10]
        self.account = str(uuid.uuid4()).replace('-', '')[0:10]
        self.cloudspace = str(uuid.uuid4()).replace('-', '')[0:10]
        self.password = str(uuid.uuid4()).replace('-', '')[0:10]
        self.email = str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        self.group = 'user'

        self.lg('Create new username, user:%s password:%s' % (self.username,self.password))
        self.create_new_user(self.username,self.password,self.email,self.group)

        self.lg('create new account %s' % self.account)
        self.create_new_account(self.account,self.username)

        self.lg('open the account page')
        self.open_account_page(self.account)

        self.lg('create new cloudspace')
        self.create_cloud_space(self.account,self.cloudspace)

        self.lg('open cloud space page')
        self.open_cloudspace_page(self.account,self.cloudspace)


        self.lg('%s ENDED' % self._testID)