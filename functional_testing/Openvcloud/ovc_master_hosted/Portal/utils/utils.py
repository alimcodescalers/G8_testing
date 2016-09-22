import logging
import unittest
import time
import os
import uuid
from random import randint

from testconfig import config
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from pytractor import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from . import utils_xpath
from pytractor.exceptions import AngularNotFoundException
from selenium.webdriver.support.ui import Select


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.environment_url = config['main']['env']
        self.environment_storage = config['main']['location']
        self.admin_username = config['main']['admin']
        self.admin_password = config['main']['passwd']
        self.browser = config['main']['browser']
        self.base_page = self.environment_url + '/ays'
        self.elements = utils_xpath.elements.copy()

    @classmethod
    def setUpClass(cls):
        super(BaseTest, cls).setUpClass()

    def setUp(self):
        self.CLEANUP = {"users": [], "accounts": []}
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('portal_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.wait = WebDriverWait(self.driver, 30)
        for temp in range(5):
            try:
                self.driver.get(self.environment_url)
                break
            except AngularNotFoundException:
                time.sleep(1)
        else:
            self.fail('AngularNotFoundException')
        self.driver.set_window_size(1920, 1080)
        for temp in range(5):
            if self.wait_until_element_located(self.elements["username_textbox"]):
                break
            else:
                self.driver.refresh()
        else:
            self.fail("The login page isn't loading well.")

        self.username = str(uuid.uuid4()).replace('-', '')[0:10]
        self.account = str(uuid.uuid4()).replace('-', '')[0:10]
        self.cloudspace = str(uuid.uuid4()).replace('-', '')[0:10]
        self.machine_name = str(uuid.uuid4()).replace('-', '')[0:10]
        self.password = str(uuid.uuid4()).replace('-', '')[0:10]
        self.email = str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        self.group = 'user'


    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        accounts = self.CLEANUP.get("accounts")
        if accounts:
            for account in accounts:
                self.delete_account(account)
                self.lg('Teardown -- delete account: %s' % account)

        users = self.CLEANUP.get("users")
        if users:
            for user in users:
                self.delete_user(user)
                self.lg('Teardown -- delete user: %s' % user)

        self.driver.quit()
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s ExecutionTime is %s sec.' % (self._testID, executionTime))

    def lg(self, msg):
        self._logger.info(msg)

    def login(self, username='', password=''):
        username = username or self.admin_username
        password = password or self.admin_password
        self.lg('Do login using username [%s] and passsword [%s]' % (username, password))
        self.set_text('username_textbox', username)
        self.set_text('password_textbox', password)
        self.click('login_button')
        self.lg('Login successfully using username [%s] and passsword [%s]' % (username, password))

    def logout(self):
        self.lg('Do logout')
        self.click('logout_button')
        self.lg('Logout done successfully')

    def set_browser(self):
        if self.browser == 'chrome':
            self.driver = webdriver.Chrome()
        elif self.browser == 'firefox':
            fp = FirefoxProfile()
            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference("browser.download.manager.showWhenStarting", False)
            fp.set_preference("browser.download.dir", os.path.expanduser("~") + "/Downloads/")
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip, application/octet-stream")
            self.driver = webdriver.Firefox(firefox_profile=fp)
        elif self.browser == 'ie':
            self.driver = webdriver.Ie()
        elif self.browser == 'opera':
            self.driver = webdriver.Opera()
        elif self.browser == 'safari':
            self.driver = webdriver.Safari
        else:
            self.fail("Invalid browser configuration [%s]" % self.browser)

    def get_page(self, page_url):
        try:
            self.driver.get(page_url)
            self.driver.ignore_synchronization = False
        except AngularNotFoundException:
            self.driver.ignore_synchronization = True
            self.driver.get(page_url)

    def element_is_enabled(self, element):
        return self.driver.find_element_by_xpath(self.elements[element]).is_enabled()

    def element_is_displayed(self, element):
        self.wait_until_element_located(self.elements[element])
        return self.driver.find_element_by_xpath(self.elements[element]).is_displayed()

    def element_background_color(self, element):
        return str(self.driver.find_element_by_xpath(self.elements[element]) \
                   .value_of_css_property('background-color'))

    def wait_until_element_located(self, name):
        for temp in range(3):
            try:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, name)))
                return True
            except:
                time.sleep(1)
        else:
            return False

    def wait_element(self, element):
        if self.wait_until_element_located(self.elements[element]):
            return True
        else:
            return False

    def wait_until_element_located_and_has_text(self, xpath, text):
        for temp in range(10):
            try:
                self.wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath), text))
                return True
            except (TimeoutException, StaleElementReferenceException):
                time.sleep(1)
        else:
            self.assertEqual(self.driver.find_element_by_xpath(xpath).text, text)

    def wait_unti_element_clickable(self, name):
        for temp in range(10):
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, name)))
            except (TimeoutException, StaleElementReferenceException):
                time.sleep(1)
            else:
                return True
        else:
            self.fail('StaleElementReferenceException')

    def click(self, element):
        element = self.elements[element]
        for temp in range(10):
            try:
                self.driver.find_element_by_xpath(element).click()
                break
            except:
                time.sleep(1)
        else:
            self.fail("can't find %s element" % element)
        time.sleep(1)

    def click_link(self, link):
        self.get_page(link)

    def get_text(self, element):
        element = self.elements[element]
        for temp in range(10):
            try:
                return self.driver.find_element_by_xpath(element).text
            except:
                time.sleep(0.5)
        else:
            self.fail('NoSuchElementException(%s)' % element)

    def get_size(self, element):
        element = self.elements[element]
        self.wait_until_element_located(element)
        return self.driver.find_element_by_xpath(element).size

    def get_value(self, element):
        return self.get_attribute(element, "value")

    def element_is_readonly(self, element):
        return self.get_attribute(element, "readonly")

    def element_link(self, element):
        return self.get_attribute(element, "href")

    def get_attribute(self, element, attribute):
        element = self.elements[element]
        self.wait_until_element_located(element)
        return self.driver.find_element_by_xpath(element).get_attribute(attribute)

    def get_url(self):
        return self.driver.current_url

    def set_text(self, element, value):
        element = self.elements[element]
        self.wait_until_element_located(element)
        self.driver.find_element_by_xpath(element).clear()
        self.driver.find_element_by_xpath(element).send_keys(value)

    def move_curser_to_element(self, element):
        element = self.elements[element]
        location = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, element)))
        ActionChains(self.driver).move_to_element(location).perform()

    def check_element_is_exist(self, element):
        if self.wait_element(element):
            return True
        else:
            return False

    def select(self, list_element, item_value):
        list_xpath = self.elements[list_element]
        self.select_obeject = Select(self.driver.find_element_by_xpath(list_xpath))
        self.select_list = self.select_obeject.options

        for option in self.select_list:
            self.lg("Debug Test" + str(option.text))
            if item_value in option.text:
                self.select_obeject.select_by_visible_text(option.text)
                item_value = option.text
                break
        else:
            self.fail("This %s item isn't an option in %s list" % (item_value, list_element))

        self.assertEqual(item_value, self.select_obeject.first_selected_option.text)

    def get_list_items(self, list_element):
        element = self.elements[list_element]
        html_list = self.driver.find_element_by_xpath(element)
        return html_list.find_elements_by_tag_name("li")

    def get_list_items_text(self, list_element):
        compo_menu = self.get_list_items(list_element)
        compo_menu_exist = []
        for item in compo_menu:
            if item.text != "":
                if '\n' in item.text:
                    data = item.text.split('\n')
                    compo_menu_exist += data
                else:
                    compo_menu_exist.append(item.text)
        return compo_menu_exist

    def element_in_url(self, text_item):
        if " " in text_item:
            text_item = text_item.replace(" ", "%20")
        for temp in range(10):
            try:
                if text_item in self.get_url():
                    return True
            except:
                time.sleep(1)
        else:
            self.fail("this %s item isn't exist in this url: %s" % (text_item, self.get_url()))

    def check_side_list(self):
        for temp in range(3):
            try:
                if self.driver.find_element_by_xpath(self.elements["left_menu"]).location["x"] < 0:
                    self.click("left_menu_button")
                break
            except:
                self.lg("can't locate the left menu")

    def open_base_page(self, menu_item='', sub_menu_item=''):
        self.get_page(self.base_page)
        self.check_side_list()
        self.click(menu_item)
        self.check_side_list()
        self.click(sub_menu_item)

    def create_new_user(self, username='', password='', email='', group=''):
        username = username or str(uuid.uuid4()).replace('-', '')[0:10]
        password = password or str(uuid.uuid4()).replace('-', '')[0:10]
        email = email or str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        group = group or 'user'

        self.open_base_page("cloud_broker", "users")

        self.click("add_user")
        self.assertTrue(self.check_element_is_exist("create_user"))

        self.set_text("username", username)
        self.set_text("mail", email)
        self.set_text("password", password)

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
        self.open_base_page("cloud_broker", "users")

        self.set_text("username_search", username)
        self.wait_until_element_located_and_has_text(self.elements["username_table_first"], username)
        username_id = self.get_text("username_table_first")

        self.click("username_table_first")
        self.element_in_url(username_id)

    def delete_user(self, username):
        self.open_base_page("cloud_broker", "users")

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

    def create_new_account(self, account='', username=''):
        account = account or str(uuid.uuid4()).replace('-', '')[0:10]
        username = username
        self.open_base_page("cloud_broker", "accounts")

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

        self.open_base_page("cloud_broker", "accounts")

        self.set_text("account_search", account)
        self.wait_until_element_located_and_has_text(self.elements["account_table_first_element"], account)

        account_id = self.get_text("account_first_id")
        self.click("account_first_id")
        self.element_in_url(account_id)

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

    def create_cloud_space(self, account, cloud_space=''):
        account = account
        self.cloud_space_name = cloud_space or str(uuid.uuid4()).replace('-', '')[0:10]

        self.open_account_page(account)
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
        self.open_base_page("cloud_broker", "cloud_spaces")
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

    def create_virtual_machine(self, cloudspace='', machine_name='', image='', memory='', disk=''):
        cloudspace = cloudspace
        machine_name = machine_name or str(uuid.uuid4()).replace('-', '')[0:10]
        self.image = image or 'Ubuntu 14.04'
        self.memory = memory or '1024 MB'
        self.disk = disk or '50 GB'

        self.lg('open the cloudspace page')
        self.open_cloudspace_page(cloudspace)

        self.lg('add virtual machine')
        self.click('add_virtual_machine')
        self.assertEqual(self.get_text('create_virtual_machine_on_cpu_node'), 'Create Machine On CPU Node')

        self.lg('enter the machine name')
        self.set_text('machine_name_admin', machine_name)

        self.lg('enter the machien description')
        self.set_text('machine_description_admin', str(uuid.uuid4()).replace('-', '')[0:10])

        self.lg('select the image')
        self.select('machine_images_list', self.image)

        self.lg('select the memory')
        self.select('machine_memory_list', self.memory)

        self.lg('select the disk')
        self.select('machine_disk_list', self.disk)

        self.lg('create machine confirm button')
        self.click('machine_confirm_button')

        self.set_text('virtual machine search', machine_name)
        self.wait_until_element_located_and_has_text(self.elements["virtual_machine_table_first_element"],
                                                     machine_name)

    def open_virtual_machine_page(self, cloudspace='', machine_name=''):
        cloudspace = cloudspace
        machine_name = machine_name

        self.lg('opne %s cloudspace' % cloudspace)
        self.open_cloudspace_page(cloudspace)

        self.lg('open %s virtual machine' % machine_name)
        self.set_text('virtual machine search', machine_name)
        self.wait_until_element_located_and_has_text(self.elements["virtual_machine_table_first_element"],
                                                     machine_name)
        vm_id = self.get_text("virtual_machine_table_first_element_2")[3:]
        self.click('virtual_machine_table_first_element')
        self.element_in_url(vm_id)

    def delete_virtual_machine(self, cloudspace='', machine_name=''):
        cloudspace = cloudspace
        machine_name = machine_name

        self.lg('open %s virtual machine' % machine_name)
        self.open_virtual_machine_page(cloudspace, machine_name)

        self.lg('delete the machine')
        self.click('virtual_machine_action')
        self.click('virtual_machine_delete')
        self.set_text('virtual_machine_delete_reason', "Test")
        self.click("virtual_machine_delete_confirm")
        self.wait_until_element_located_and_has_text(self.elements["virtual_machine_page_status"],
                                                     "DESTROYED")

    def get_storage_list(self):
        '''
        This method to read the storage list from config file and return list of storage
        :return:
        '''
        item = ''
        storage_menu = []
        for _ in self.environment_storage:
            if _ != "," and self.environment_storage.index(_) != len(self.environment_storage) - 1:
                item += _
            elif self.environment_storage.index(_) == len(self.environment_storage) - 1:
                item += _
                storage_menu.append(item)
            else:
                storage_menu.append(item)
                item = ''
        return storage_menu

    def compare_original_list_with_exist_list(self, menu_click, menu_element, original_list):
        self.check_side_list()
        if menu_click != "":
            self.click(menu_click)
        exist_menu = self.get_list_items_text(menu_element)
        for item in original_list:
            if not item in exist_menu:
                self.fail("This %s list item isn't exist in %s" % (item, exist_menu))

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

    def account_enable(self, account):
        try:
            self.wait_until_element_located_and_has_text(self.elements["account_name_value"], account)
        except:
            self.open_account_page(account)

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

    def account_disable(self, account):
        try:
            self.wait_until_element_located_and_has_text(self.elements["account_name_value"], account)
        except:
            self.open_account_page(account)

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

    def end_user_create_virtual_machine(self, image_name="ubuntu_14_04", machine_name=''):
        self.lg('Open end user home page')
        self.get_page(self.environment_url)

        if self.check_element_is_exist("machines_button"):
            self.lg(' Start creation of machine')
            self.click("machines_button")
            self.click("create_machine_button")

            machine_name = machine_name or str(uuid.uuid4()).replace('-', '')[0:10]
            machine_description = str(uuid.uuid4()).replace('-', '')[0:10]
            randome_package = randint(1, 6)
            if image_name != "windows_2012":
                random_disk_size = randint(1, 8)
            else:
                random_disk_size = randint(1, 6)
                self.click("windows")

            self.lg("Create a machine name: %s image:%s" % (machine_name, image_name))
            self.set_text("machine_name", machine_name)
            self.set_text("machine_description_", machine_description)
            self.click(image_name)
            self.click("package_%i" % randome_package)
            self.click("disk_size_%i" % random_disk_size)

            self.click("create_machine")
            for temp in range(30):
                if "console" in self.get_url():
                    break
                else:
                    time.sleep(1)

            if self.get_text("machine_status") == "RUNNING":
                self.lg(' machine is created')
                return True
            else:
                self.lg("FAIL : %s Machine isn't RUNNING" % machine_name)
                return False
        else:
            self.lg("FAIL : Machine button isn't exist for this user")
            return False

    def end_user_delete_virtual_machine(self, virtual_machine):
        self.lg('Open end user home page')
        self.get_page(self.environment_url)

        if self.check_element_is_exist("machines_button"):
            self.lg(' Start creation of machine')
            self.click("machines_button")

            if self.check_element_is_exist("end_user_machine_table"):
                self.lg('Open the machine page to destroy it')
                machine_table = self.driver.find_element_by_xpath(self.elements["end_user_machine_table"])
                machine_table_rows = machine_table.find_elements_by_class_name("ng-scope")

                for counter in range(len(machine_table_rows)):
                    machine_name_xpath = self.elements["end_user_machine_name_table"] % (counter+1)
                    machine_name = self.driver.find_element_by_xpath(machine_name_xpath)
                    if virtual_machine == machine_name.text:
                        machine_name.click()
                        break
                else:
                    self.lg("can't find %s machine in the table" % virtual_machine)
                    return False

                self.lg("Destroy the machine")
                self.click("destroy_machine")
                self.click("destroy_machine_confirm")
                time.sleep(10)
                if self.get_text("machine_list") == "Machines":
                    return True
                else:
                    self.lg("FAIL : Can't delete %s machine" % virtual_machine)
                    return False
            else:
                self.lg("There is no machines")
                return False
        else:
            self.lg("FAIL : Machine button isn't exist for this user")
            return False

    def end_user_choose_account(self, account=''):
        account = account or self.account
        self.lg('Open end user home page')
        self.get_page(self.environment_url)
        if self.check_element_is_exist("end_user_selected_account"):
            print(account,self.get_text("end_user_selected_account"))
            if account not in self.get_text("end_user_selected_account"):
                accounts_xpath = self.elements["end_user_accounts_list"]
                for temp in range(100):
                    try:
                        account_item = self.driver.find_element_by_xpath(accounts_xpath % temp)
                    except:
                        self.lg("Can't choose %s account from the end user" % account)
                        return False
                    else:
                        if account in account_item.text:
                            account_item.click()
                            cloud_space_xpath = self.elements["end_user_cloud_space"] % account
                            self.driver.find_element_by_xpath(cloud_space_xpath).click()
                            return True
            else:
                return True
        else:
            self.lg("This user doesn't has any account")
            return False