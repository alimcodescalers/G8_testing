import logging
import unittest
import time
import os
import uuid

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

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('portal_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.set_browser()
        self.wait = WebDriverWait(self.driver, 30)
        for temp in range(5):
            try:
                self.driver.get(self.environment_url)
                break
            except AngularNotFoundException:
                time.sleep(1)
        else:
            raise AngularNotFoundException
        self.driver.set_window_size(1920,1080)
        for temp in range(5):
            if self.wait_until_element_located(self.elements["username_textbox"]):
                break
            else:
                self.driver.refresh()
        else:
            raise NameError("The login page isn't loading well.")

    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
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
            raise AssertionError("Invalid broswer configuration [%s]" % self.browser)

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
            except (TimeoutException, StaleElementReferenceException):
                time.sleep(1)
        else:
            return False

    def wait_element(self, element):
        if self.wait_until_element_located(self.elements[element]):
            return True

    def wait_until_element_located_and_has_text(self, xpath, text):
        for temp in range(3):
            try:
                self.wait.until(EC.text_to_be_present_in_element((By.XPATH, xpath), text))
                break
            except (TimeoutException, StaleElementReferenceException):
                time.sleep(1)
        else:
            raise TimeoutException

    def wait_unti_element_clickable(self, name):
        for temp in range(3):
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, name)))
            except (TimeoutException, StaleElementReferenceException):
                time.sleep(1)
            else:
                return True
        else:
            raise StaleElementReferenceException

    def click(self, element):
        element = self.elements[element]
        # self.wait_until_element_located(element)
        # self.wait_unti_element_clickable(element)
        for temp in range(10):
            try:
                self.driver.find_element_by_xpath(element).click()
                break
            except:
                time.sleep(1)
        else:
            raise NoSuchElementException("can't find %s element" % element)
        time.sleep(1)

    def click_link(self, link):
        self.get_page(link)

    def get_text(self, element):
        element = self.elements[element]
        for temp in range(3):
            try:
                return self.driver.find_element_by_xpath(element).text
            except:
                time.sleep(0.5)
        else:
            raise NoSuchElementException(element)

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
        location = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, element)))
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
            raise Exception("This %s item isn't an option in %s list" % (item_value, list_element))
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
            raise NoSuchElementException("this %s item isn't exist in this url: %s" % (text_item, self.get_url()))

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
        self.username = username or str(uuid.uuid4()).replace('-', '')[0:10]
        self.password = password or str(uuid.uuid4()).replace('-', '')[0:10]
        self.email = email or str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        self.group = group or 'user'

        self.open_base_page("cloud_broker", "users")

        self.click("add_user")
        self.assertTrue(self.check_element_is_exist("create_user"))

        self.set_text("username", self.username)
        self.set_text("mail", self.email)
        self.set_text("password", self.password)

        for i in range(1, 100):
            xpath_user_group = self.elements["user_group"] % i
            if self.group == self.driver.find_element_by_xpath(xpath_user_group).text:
                break
        user_group = self.driver.find_element_by_xpath(xpath_user_group)
        if not user_group.is_selected():
            user_group.click()

        self.click("confirm_add_user")
        time.sleep(1)
        self.set_text("username_search", self.username)
        self.wait_until_element_located_and_has_text(self.elements["username_table_first"], self.username)

    def open_user_page(self, username=''):
        self.username = username
        self.open_base_page("cloud_broker", "users")

        self.set_text("username_search", self.username)
        self.wait_until_element_located_and_has_text(self.elements["username_table_first"], self.username)
        username_id = self.get_text("username_table_first")

        self.click("username_table_first")
        self.element_in_url(username_id)

    def delete_user(self, username):
        self.open_base_page("cloud_broker", "users")

        self.set_text("user_search", username)
        self.lg("check if this user is exist")
        if self.check_element_is_exist("user_table_first_element"):
            time.sleep(1)
            self.click("user_table_first_element")
            self.click("user_action")
            self.click("user_delete")
            self.click("user_delete_confirm")
            self.set_text("user_search", username)
            return True
        else:
            return False

    def create_new_account(self, account='', username=''):
        self.account = account or str(uuid.uuid4()).replace('-', '')[0:10]
        self.username = username
        self.open_base_page("cloud_broker", "accounts")

        self.click("add_account")
        self.assertTrue(self.check_element_is_exist("create_account"))

        self.set_text("account_name", self.account)
        self.set_text("account_username", self.username)

        self.click("account_confirm")

        self.set_text("account_search", self.account)
        self.wait_until_element_located_and_has_text(self.elements["account_table_first_element"], self.account)

        if account == '':
            return self.account

    def open_account_page(self, account=''):
        self.account = account

        self.open_base_page("cloud_broker", "accounts")

        self.set_text("account_search", self.account)
        self.wait_until_element_located_and_has_text(self.elements["account_table_first_element"], self.account)

        account_id = self.get_text("account_first_id")
        self.click("account_first_id")
        self.element_in_url(account_id)

    def delete_account(self, account=''):
        self.account = account

        self.lg('open %s account' % account)
        self.open_account_page(self.account)

        self.lg('delete the account')
        self.click('account_action')
        self.click('account_delete')
        self.set_text('account_delete_reason', "Test")
        self.click("account_delete_confirm")
        self.wait_until_element_located_and_has_text(self.elements["account_page_status"],
                                                     "DESTROYED")

    def create_cloud_space(self, account='', cloud_space=''):
        self.account = account
        self.cloud_space_name = cloud_space or str(uuid.uuid4()).replace('-', '')[0:10]

        self.open_account_page(self.account)
        self.account_username = self.get_text("account_first_user_name")

        self.click("add_cloudspace")

        self.assertEqual(self.get_text("create_cloud_space"), "Create Cloud Space")

        self.set_text("cloud_space_name", self.cloud_space_name)
        self.set_text("cloud_space_user_name", self.account_username)

        self.click("cloud_space_confirm")

        self.set_text("cloud_space_search", self.cloud_space_name)
        self.wait_until_element_located_and_has_text(self.elements["cloud_space_table_first_element_2"],
                                                     self.cloud_space_name)
        return self.cloud_space_name

    def open_cloudspace_page(self, account='', cloudspace=''):
        self.account = account
        self.cloudspace = cloudspace

        self.open_account_page(self.account)

        self.set_text("cloud_space_search", self.cloudspace)
        self.wait_until_element_located_and_has_text(self.elements["cloud_space_table_first_element_2"],
                                                     self.cloudspace)
        cloudspace_id = self.get_text("cloud_space_table_first_element_1")
        self.click("cloud_space_table_first_element_1")
        self.element_in_url(cloudspace_id)

    def delete_cloudspace(self, account='', cloudspace=''):
        self.account = account
        self.cloudspace = cloudspace

        self.lg('open %s cloudspace' % cloudspace)
        self.open_cloudspace_page(self.account, self.cloudspace)

        self.lg('delete the cloudspace')
        self.click('cloudspace_action')
        self.click('cloudspace_delete')
        self.set_text('cloudspace_delete_reason', "Test")
        self.click("cloudspace_delete_confirm")
        time.sleep(0.5)
        self.get_page(self.driver.current_url)
        for temp in range(5):
            try:
                self.wait_until_element_located_and_has_text(self.elements["cloudspace_page_status"], "DESTROYED")
            except TimeoutException:
                time.sleep(1)
                self.driver.refresh()

    def create_virtual_machine(self, account='', cloudspace='', machine_name='', image='', memory='', disk=''):
        self.account = account
        self.cloudspace = cloudspace
        self.machine_name = machine_name or str(uuid.uuid4()).replace('-', '')[0:10]
        self.image = image or 'Ubuntu 14.04'
        self.memory = memory or '1024 MB'
        self.disk = disk or '50 GB'

        self.lg('open the cloudspace page')
        self.open_cloudspace_page(self.account, self.cloudspace)

        self.lg('add virtual machine')
        self.click('add_virtual_machine')
        self.assertEqual(self.get_text('create_virtual_machine_on_cpu_node'), 'Create Machine On CPU Node')

        self.lg('enter the machine name')
        self.set_text('machine_name', self.machine_name)

        self.lg('enter the machien description')
        self.set_text('machine_description', str(uuid.uuid4()).replace('-', '')[0:10])

        self.lg('select the image')
        self.select('machine_images_list', self.image)

        self.lg('select the memory')
        self.select('machine_memory_list', self.memory)

        self.lg('select the disk')
        self.select('machine_disk_list', self.disk)

        self.lg('create machine confirm button')
        self.click('machine_confirm_button')

        self.set_text('virtual machine search', self.machine_name)
        self.wait_until_element_located_and_has_text(self.elements["virtual_machine_table_first_element"],
                                                     self.machine_name)

    def open_virtual_machine_page(self, account='', cloudspace='', machine_name=''):
        self.account = account
        self.cloudspace = cloudspace
        self.machine_name = machine_name

        self.lg('opne %s cloudspace' % cloudspace)
        self.open_cloudspace_page(self.account, self.cloudspace)

        self.lg('open %s virtual machine' % machine_name)
        self.set_text('virtual machine search', self.machine_name)
        self.wait_until_element_located_and_has_text(self.elements["virtual_machine_table_first_element"],
                                                     self.machine_name)
        vm_id = self.get_text("virtual_machine_table_first_element_2")[3:]
        self.click('virtual_machine_table_first_element')
        self.element_in_url(vm_id)

    def delete_virtual_machine(self, account='', cloudspace='', machine_name=''):
        self.account = account
        self.cloudspace = cloudspace
        self.machine_name = machine_name

        self.lg('open %s virtual machine' % machine_name)
        self.open_virtual_machine_page(self.account, self.cloudspace, self.machine_name)

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
                raise NameError("This %s list item isn't exist in %s" % (item, exist_menu))
