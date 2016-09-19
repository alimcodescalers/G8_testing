import uuid
from random import randint

from functional_testing.Openvcloud.ovc_master_hosted.Portal.utils.utils import BaseTest


class AccountsTests(BaseTest):
    def setUp(self):
        super(AccountsTests, self).setUp()
        self.login()
        self.lg('Create new username, user:%s password:%s' % (self.username, self.password))
        self.create_new_user(self.username, self.password, self.email, self.group)
        self.lg('create new account %s' % self.account)
        self.create_new_account(self.account, self.username)
        self.open_account_page(self.account)

    def test01_edit_account(self):
        """ PRTL-000
        *Test case to make sure that edit actions on accounts are working as expected*

        **Test Scenario:**
        #. create account.
        #. search for it and verify it should succeed
        #. edit account parameters and verify it should succeed
        """
        edit_items = ['name', 'Max Memory Capacity (GB)', 'Max VDisk Capacity (GB)', 'Max Number of CPU Cores',
                      'Max Primary Storage(NAS) Capacity (TB)', 'Max Secondary Storage(Archive) Capacity (TB)',
                      'Max Network Transfer In Operator (GB)', 'Max Network Transfer Peering (GB)',
                      'Max Number of Public IP Addresses']

        for item in edit_items:
            if item == 'name':
                value = str(uuid.uuid4()).replace('-', '')[0:10]
                self.edit_account(self.account, item, value)
                self.CLEANUP["accounts"].remove(self.account)
                self.account = value
                self.CLEANUP["accounts"].append(self.account)
                self.assertIn(value,self.get_text('account_name_value'))
            else:
                value = randint(1, 100)
                self.edit_account(self.account, item, value)
                xpath = self.elements['account_action_page_items'] % edit_items.index(item)
                self.assertIn(str(value),self.driver.find_element_by_xpath(xpath).text)


    def test02_disable_enable_account(self):
        pass
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

