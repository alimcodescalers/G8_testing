from ....utils.utils import BaseTest
from ..page_elements_xpath import account_page
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

    def test01_create_account_user_cs_vm(self):
        """ PRTL-010
        *Test case for create new user and change his password*

        **Test Scenario:**
        #. Create new user
        #. create new account
        #. open the account page
        #. create new cloudspace
        #. open cloudspace page
        #. create virtual machine
        #. open the virtual machine page
        """
        self.username = str(uuid.uuid4()).replace('-', '')[0:10]
        self.account = str(uuid.uuid4()).replace('-', '')[0:10]
        self.cloudspace = str(uuid.uuid4()).replace('-', '')[0:10]
        self.machine_name = str(uuid.uuid4()).replace('-', '')[0:10]
        self.password = str(uuid.uuid4()).replace('-', '')[0:10]
        self.email = str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        self.group = 'user'

        self.lg('Create new username, user:%s password:%s' % (self.username,self.password))
        self.create_new_user(self.username,self.password,self.email,self.group)

        self.lg('open user page')
        self.open_user_page(self.username)

        self.lg('create new account %s' % self.account)
        self.create_new_account(self.account,self.username)

        self.lg('open the account page')
        self.open_account_page(self.account)

        self.lg('create new cloudspace')
        self.create_cloud_space(self.account,self.cloudspace)

        self.lg('open cloud space page')
        self.open_cloudspace_page(self.account,self.cloudspace)

        self.lg('create virtual machine')
        self.create_virtual_machine(self.account, self.cloudspace, self.machine_name)

        self.lg('open virtual machine page')
        self.open_virtual_machine_page(self.account,self.cloudspace,self.machine_name)

        self.lg('delete virtual machine')
        self.delete_virtual_machine(self.account,self.cloudspace,self.machine_name)

        self.lg('delete cloudspace')
        self.delete_cloudspace(self.account,self.cloudspace)

        self.lg('delete account')
        self.delete_account(self.account)

        self.lg('%s ENDED' % self._testID)