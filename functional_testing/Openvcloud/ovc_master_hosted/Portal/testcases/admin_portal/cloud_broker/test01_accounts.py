import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class AccountsTests(Framework):
    def setUp(self):
        super(AccountsTests, self).setUp()
        self.Login.Login(username=self.admin_username, password=self.admin_password)
        self.lg('Create new username, user:%s password:%s' % (self.username, self.password))
        self.Users.create_new_user(self.username, self.password, self.email, self.group)
        self.lg('create new account %s' % self.account)
        self.Accounts.create_new_account(self.account, self.username)
        self.Accounts.open_account_page(self.account)

    def test01_edit_account(self):
        """ PRTL-023
        *Test case to make sure that edit actions on accounts are working as expected*

        **Test Scenario:**
        #. create account.
        #. search for it and verify it should succeed
        #. edit account parameters and verify it should succeed
        """
        self.assertTrue(self.Accounts.account_edit_all_items(self.account))

    @unittest.skip("bug# 431")
    def test02_disable_enable_account(self):
        """ PRTL-024
        *Test case to make sure that enable/disable actions on accounts are working as expected*

        **Test Scenario:**
        #. create account.
        #. search for it and verify it should succeed
        #. disable account and verify it should succeed
        #. enable account and verify it should succeed
        """

        self.assertTrue(self.Accounts.account_disable(self.account))
        self.assertTrue(self.Accounts.account_edit_all_items(self.account))
        self.assertTrue(self.Accounts.account_enable(self.account))
        self.assertTrue(self.Accounts.account_edit_all_items(self.account))

    '''
    def test02_account_page_paging_table_sorting(self):
        """ PRTL-000
        *Test case to make sure that paging and sorting of accounts page are working as expected*

        **Test Scenario:**
        #. go to accounts page.
        #. try paging from the available page numbers and verify it should succeed
        #. try paging from start/previous/next/last and verify it should succeed
        #. try sorting for all fields and verify it should succeed
        """
    '''

