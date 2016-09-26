import time
from random import randint

from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.utils.utils import BaseTest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
import uuid

class accounts(BaseTest):
    def __init__(self, *args, **kwargs):
        super(accounts, self).__init__(*args, **kwargs)

    def create_new_account(self, account='', username=''):
        account = account or str(uuid.uuid4()).replace('-', '')[0:10]
        username = username
        leftNavigationMenu.CloudBroker.Accounts()

        self.click("add_account")
        self.assertTrue(self.check_element_is_exist("create_account"))

        self.set_text("account_name", account)
        self.set_text("account_username", username)

        self.click("account_confirm")

        self.set_text("account_search", account)
        self.wait_until_element_located_and_has_text(self.elements["account_table_first_element"], account)

        self.CLEANUP["accounts"].append(account)
        if account == '':
            return account
        self.lg("%s account is created" % account)

    def open_account_page(self, account=''):
        account = account
        leftNavigationMenu.CloudBroker.Accounts()

        self.set_text("account_search", account)
        self.wait_until_element_located_and_has_text(self.elements["account_table_first_element"], account)

        account_id = self.get_text("account_first_id")
        self.click("account_first_id")
        self.element_in_url(account_id)

    def account_edit(self, account, edit_item, edit_value):
        try:
            self.wait_until_element_located_and_has_text(self.elements["account_name_value"], account)
        except:
            self.open_account_page(account)

        self.click('account_action')
        self.click('account_action_edit')

        self.assertEqual(self.get_text("account_action_edit_page"), 'Confirm Action Edit')

        edit_items = ['name', 'Max Memory Capacity (GB)', 'Max VDisk Capacity (GB)', 'Max Number of CPU Cores',
                      'Max Primary Storage(NAS) Capacity (TB)', 'Max Secondary Storage(Archive) Capacity (TB)',
                      'Max Network Transfer In Operator (GB)', 'Max Network Transfer Peering (GB)',
                      'Max Number of Public IP Addresses']
        for item in edit_items:
            if item == edit_item:
                xpath = self.elements['account_action_edit_page_items'] % (edit_items.index(item) + 1)
                break
        else:
            self.fail("%s isn't an item in the list" % edit_item)

        self.driver.find_element_by_xpath(xpath).clear()
        self.driver.find_element_by_xpath(xpath).send_keys(edit_value)

        self.click('account_action_edit_page_confirm')

    def account_edit_all_items(self, account):
        edit_items = ['name', 'Max Memory Capacity (GB)', 'Max VDisk Capacity (GB)', 'Max Number of CPU Cores',
                      'Max Primary Storage(NAS) Capacity (TB)', 'Max Secondary Storage(Archive) Capacity (TB)',
                      'Max Network Transfer In Operator (GB)', 'Max Network Transfer Peering (GB)',
                      'Max Number of Public IP Addresses']

        for item in edit_items:
            if item == 'name':
                value = str(uuid.uuid4()).replace('-', '')[0:10]
                self.account_edit(account, item, value)
                self.CLEANUP["accounts"].remove(self.account)
                self.account = value
                self.CLEANUP["accounts"].append(self.account)
                time.sleep(0.5)
                if value not in self.get_text('account_name_value'):
                    self.lg("FAIL : %s not in the account name: %s" % (value, self.get_text('account_name_value')))
                    return False
            else:
                value = randint(1, 100)
                self.account_edit(self.account, item, value)
                xpath = self.elements['account_action_page_items'] % edit_items.index(item)
                if str(value) not in self.driver.find_element_by_xpath(xpath).text:
                    self.lg("FAIL : %d no in %s" % (value,self.driver.find_element_by_xpath(xpath).text))
                    return False
        return True

    def account_disable(self, account):
        try:
            self.wait_until_element_located_and_has_text(self.elements["account_name_value"], account)
        except:
            leftNavigationMenu.CloudBroker.Accounts()

        if self.get_text("account_page_status") != "CONFIRMED":
            self.lg("FAIL : %s account status : %s" % (account, self.get_text("account_page_status")))
            return False

        self.click('account_action')
        self.click('account_disable')

        self.assertEqual(self.get_text("account_disable_page"), "Confirm Action Disable")
        self.set_text("account_disable_reason", "disable")
        self.click("account_disable_confirm")

        if self.get_text("account_page_status") == "DISABLED":
            return True
        else:
            self.lg("FAIL : account status : %s" % self.get_text("account_page_status"))
            return False

    def account_enable(self, account):
        try:
            self.wait_until_element_located_and_has_text(self.elements["account_name_value"], account)
        except:
            leftNavigationMenu.CloudBroker.Accounts()

        if self.get_text("account_page_status") != "DISABLED":
            self.lg("FAIL : %s account status : %s" % (account, self.get_text("account_page_status")))
            return False

        self.click('account_action')
        self.click('account_enable')

        self.assertEqual(self.get_text("account_enable_page"), "Confirm Action Enable")
        self.set_text("account_enable_reason", "Enable")
        self.click("account_enable_confirm")

        if self.get_text("account_page_status") == "CONFIRMED":
            return True
        else:

            self.lg("FAIL : account status : %s" % self.get_text("account_page_status"))
            return False

    def delete_account(self, account=''):
        account = account

        self.lg('open %s account' % account)
        self.open_account_page(account)

        if self.driver.find_element_by_xpath(self.elements["account_page_status"]).text in ["CONFIRMED", "DISABLED"]:
            self.lg('delete %s account' % account)
            self.click('account_action')
            self.click('account_delete')
            self.set_text('account_delete_reason', "Test")
            self.click("account_delete_confirm")
            self.wait_until_element_located_and_has_text(self.elements["account_page_status"],
                                                         "DESTROYED")
            self.CLEANUP['accounts'].remove(account)
        elif self.driver.find_element_by_xpath(self.elements["account_page_status"]).text == "DESTROYED":
            self.lg('%s account is already deleted' % account)
        else:
            self.fail('"%s" account status has an error in the page' % account)