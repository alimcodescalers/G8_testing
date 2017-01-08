import time
from random import randint
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
import uuid


class accounts():
    def __init__(self, framework):
        self.framework = framework
        self.LeftNavigationMenu = leftNavigationMenu(framework)

    def get_it(self):
        self.LeftNavigationMenu.CloudBroker.Accounts()

    def is_at(self):
        for _ in range(10):
            if 'Accounts' == self.framework.get_text('account_name_value'):
                return True
            else:
                time.sleep(1)
        else:
            return False

    def create_new_account(self, account='', username='', max_memory=None):
        account = account or str(uuid.uuid4()).replace('-', '')[0:10]
        username = username
        self.LeftNavigationMenu.CloudBroker.Accounts()

        self.framework.click("add_account")
        self.framework.assertTrue(self.framework.check_element_is_exist("create_account"))

        self.framework.set_text("account_name", account)
        self.framework.set_text("account_username", username)

        if max_memory:
            self.framework.set_text("account_maxmemory", max_memory)

        self.framework.click("account_confirm")
        time.sleep(3)
        self.framework.set_text("account_search", account)
        self.framework.wait_until_element_located_and_has_text("account_table_first_element", account)

        self.framework.CLEANUP["accounts"].append(account)
        if account == '':
            return account
        self.framework.lg("%s account is created" % account)

    def open_account_page(self, account=''):
        account = account
        self.LeftNavigationMenu.CloudBroker.Accounts()

        self.framework.set_text("account_search", account)
        self.framework.wait_until_element_located_and_has_text("account_table_first_element", account)

        account_id = self.framework.get_text("account_first_id")
        self.framework.click("account_first_id")
        self.framework.element_in_url(account_id)

    def account_edit(self, account, edit_item, edit_value):
        try:
            self.framework.wait_until_element_located_and_has_text("account_name_value", account)
        except:
            self.open_account_page(account)

        self.framework.click('account_action')
        self.framework.click('account_action_edit')

        self.framework.assertEqual(self.framework.get_text("account_action_edit_page"), 'Confirm Action Edit')

        edit_items = ['name', 'Max Memory Capacity (GB)', 'Max VDisk Capacity (GB)', 'Max Number of CPU Cores',
                      'Max Primary Storage(NAS) Capacity (TB)', 'Max Secondary Storage(Archive) Capacity (TB)',
                      'Max Network Transfer In Operator (GB)', 'Max Network Transfer Peering (GB)',
                      'Max Number of Public IP Addresses']
        for item in edit_items:
            if item == edit_item:
                xpath = self.framework.elements['account_action_edit_page_items'][1] % (edit_items.index(item) + 1)
                break
        else:
            self.framework.fail("%s isn't an item in the list" % edit_item)

        self.framework.driver.find_element_by_xpath(xpath).clear()
        self.framework.driver.find_element_by_xpath(xpath).send_keys(edit_value)

        self.framework.click('account_action_edit_page_confirm')

    def account_edit_all_items(self, account):
        edit_items = ['name', 'Max Memory Capacity (GB)', 'Max VDisk Capacity (GB)', 'Max Number of CPU Cores',
                      'Max Primary Storage(NAS) Capacity (TB)', 'Max Secondary Storage(Archive) Capacity (TB)',
                      'Max Network Transfer In Operator (GB)', 'Max Network Transfer Peering (GB)',
                      'Max Number of Public IP Addresses']

        for item in edit_items:
            if item == 'name':
                value = str(uuid.uuid4()).replace('-', '')[0:10]
                self.account_edit(account, item, value)
                self.framework.CLEANUP["accounts"].remove(self.framework.account)
                self.framework.account = value
                self.framework.CLEANUP["accounts"].append(self.framework.account)
                time.sleep(0.5)
                if value not in self.framework.get_text('account_name_value'):
                    self.framework.lg("FAIL : %s not in the account name: %s" % (
                        value, self.framework.get_text('account_name_value')))
                    return False
            else:
                value = randint(1, 100)
                self.account_edit(self.framework.account, item, value)
                xpath = self.framework.elements['account_action_page_items'][1] % edit_items.index(item)
                try:
                    for _ in range(10):
                        if str(value) not in self.framework.driver.find_element_by_xpath(xpath).text:
                            time.sleep(0.5)
                        else:
                            break
                    else:
                        self.framework.lg(
                            "FAIL : %d no in %s" % (value, self.framework.driver.find_element_by_xpath(xpath).text))
                        return False
                except:
                    pass  # ignor silence
        return True

    def account_disable(self, account):
        try:
            self.framework.wait_until_element_located_and_has_text("account_name_value", account)
        except:
            self.LeftNavigationMenu.CloudBroker.Accounts()

        if self.framework.get_text("account_page_status") != "CONFIRMED":
            self.framework.lg(
                "FAIL : %s account status : %s" % (account, self.framework.get_text("account_page_status")))
            return False

        self.framework.click('account_action')
        self.framework.click('account_disable')

        self.framework.assertEqual(self.framework.get_text("account_disable_page"), "Confirm Action Disable")
        self.framework.set_text("account_disable_reason", "disable")
        self.framework.click("account_disable_confirm")

        if self.framework.get_text("account_page_status") == "DISABLED":
            return True
        else:
            self.framework.lg("FAIL : account status : %s" % self.framework.get_text("account_page_status"))
            return False

    def account_enable(self, account):
        try:
            self.framework.wait_until_element_located_and_has_text("account_name_value", account)
        except:
            self.LeftNavigationMenu.CloudBroker.Accounts()

        if self.framework.get_text("account_page_status") != "DISABLED":
            self.framework.lg(
                "FAIL : %s account status : %s" % (account, self.framework.get_text("account_page_status")))
            return False

        self.framework.click('account_action')
        self.framework.click('account_enable')

        self.framework.assertEqual(self.framework.get_text("account_enable_page"), "Confirm Action Enable")
        self.framework.set_text("account_enable_reason", "Enable")
        self.framework.click("account_enable_confirm")

        if self.framework.get_text("account_page_status") == "CONFIRMED":
            return True
        else:

            self.framework.lg("FAIL : account status : %s" % self.framework.get_text("account_page_status"))
            return False

    def delete_account(self, account=''):
        account = account

        self.framework.lg('open %s account' % account)
        self.open_account_page(account)

        if self.framework.driver.find_element_by_xpath(self.framework.elements["account_page_status"][1]).text in [
            "CONFIRMED", "DISABLED"]:
            self.framework.lg('delete %s account' % account)
            self.framework.click('account_action')
            self.framework.click('account_delete')
            self.framework.set_text('account_delete_reason', "Test")
            self.framework.click("account_delete_confirm")
            self.framework.wait_until_element_located_and_has_text("account_page_status",
                                                                   "DESTROYED")
            self.framework.CLEANUP['accounts'].remove(account)
        elif self.framework.driver.find_element_by_xpath(
                self.framework.elements["account_page_status"]).text == "DESTROYED":
            self.framework.lg('%s account is already deleted' % account)
        else:
            self.framework.fail('"%s" account status has an error in the page' % account)
