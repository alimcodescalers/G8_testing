import logging
import unittest
import time
import os
import uuid

from testconfig import config
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pytractor import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from . import utils_xpath


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.environment_url = config['main']['url']
        self.admin_username = config['main']['admin']
        self.admin_password = config['main']['passwd']
        self.browser = config['main']['browser']
        self.elements = utils_xpath.elements.copy()

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('portal_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.set_browser()
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.get(self.environment_url)
        self.driver.maximize_window()
        self.wait_until_element_located(self.elements["username_textbox"])

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

    def element_is_enabled(self, element):
        return self.driver.find_element_by_xpath(self.elements[element]).is_enabled()

    def element_is_displayed(self, element):
        return self.driver.find_element_by_xpath(self.elements[element]).is_displayed()

    def element_background_color(self, element):
        return str(self.driver.find_element_by_xpath(self.elements[element]) \
                   .value_of_css_property('background-color'))

    def wait_until_element_located(self, name):
        for i in range(3):
            try:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, name)))
            except TimeoutException:
                continue

    def wait_element(self, element):
        self.wait_until_element_located(self.elements[element])
        return True

    def wait_unti_element_clickable(self, name):
        for i in range(3):
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, name)))
            except TimeoutException:
                continue
            else:
                return True

    def click(self, element):
        element = self.elements[element]
        self.wait_until_element_located(element)
        self.wait_unti_element_clickable(element)
        self.driver.find_element_by_xpath(element).click()
        time.sleep(1)

    def click_link(self, link):
        self.driver.get(link)

    def get_text(self, element):
        element = self.elements[element]
        self.wait_until_element_located(element)
        return self.driver.find_element_by_xpath(element).text

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
        if self.wait_element(element) == True:
            return True
        else:
            return False

    def get_url(self):
        return self.driver.current_url

    def select(self,list_element,item_value):
        list_xpath = self.elements[list_element]
        self.select_obeject = Select(self.driver.find_element_by_xpath(list_xpath))
        self.select_list = self.select_obeject.options
        self.lg("Debug Test" + str(self.select_list) + str(self.select_list[1].text))

        for option in self.select_list:
            self.lg("Debug Test"+str(option.text))
            if item_value in option.text:
                self.select_obeject.select_by_visible_text(option.text)
                item_value = option.text
                break

        self.assertEqual(item_value,self.select_obeject.first_selected_option.text)

    def open_base_page(self,menu_item='',sub_menu_item=''):
        self.driver.get(self.environment_url)
        time.sleep(5)
        if self.check_element_is_exist("left_menu") == False:
            self.click("left_menu_button")

        self.click(menu_item)
        self.click(sub_menu_item)

    def create_new_user(self, username='', password='', email='', group=''):
        self.username = username or str(uuid.uuid4()).replace('-', '')[0:10]
        self.password = password or str(uuid.uuid4()).replace('-', '')[0:10]
        self.email = email or str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        self.group = group or 'user'

        self.open_base_page("cloud_broker","users")

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
        return True

    def open_user_page(self,username=''):
        self.username = username
        self.open_base_page("cloud_broker","users")

        self.set_text("username_search", self.username)
        username_id = self.get_text("username_table_first")

        self.click("username_table_first")

        if username_id in self.get_url():
            return True
        else:
            raise NoSuchElementException

    def delete_user(self, username):
        self.open_base_page("cloud_broker","users")

        self.set_text("user_search", username)
        self.lg("check if this user is exist")
        if self.check_element_is_exist("user_table_first_element") == True:
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
        self.open_base_page("cloud_broker","accounts")

        self.click("add_account")
        self.assertTrue(self.check_element_is_exist("create_account"))

        self.set_text("account_name", self.account)
        self.set_text("account_username", self.username)

        self.click("account_confirm")

        self.set_text("account_search",self.account)
        for i in range(5):
            try:
                self.assertEqual(self.get_text("account_table_first_element"), self.account)
            except :
                time.sleep(1)
                continue
            else:
                break
        if account == '' :
            return self.account

    def open_account_page(self, account=''):
        self.account = account
        #self.driver.switch_to_window(self.driver.window_handles[-1])
        self.open_base_page("cloud_broker","accounts")

        self.set_text("account_search",self.account)
        #time.sleep(60)
        account_id = self.get_text("account_first_id")
        self.click("account_first_id")
        #time.sleep(20)

        if account_id in self.get_url():
            return True
        else:
            raise NoSuchElementException

    def delete_account(self,account=''):
        self.account = account

        self.lg('open %s account' % account)
        self.open_account_page(self.account)

        self.lg('delete the account')
        self.click('account_action')
        self.click('account_delete')
        self.set_text('account_delete_reason',"Test")
        self.click("account_delete_confirm")
        self.assertEqual(self.get_text('account_page_status'),"DESTROYED")


    def create_cloud_space(self,account='',cloud_space=''):
        self.account = account
        self.cloud_space_name = cloud_space or str(uuid.uuid4()).replace('-', '')[0:10]

        self.open_account_page(self.account)
        self.account_username = self.get_text("account_first_user_name")

        self.click("add_cloudspace")

        self.assertEqual(self.get_text("create_cloud_space"),"Create Cloud Space")

        self.set_text("cloud_space_name",self.cloud_space_name)
        self.set_text("cloud_space_user_name",self.account_username)

        self.click("cloud_space_confirm")

        self.set_text("cloud_space_search",self.cloud_space_name)
        self.assertEqual(self.get_text("cloud_space_table_first_element_2"),self.cloud_space_name)
        return self.cloud_space_name

    def open_cloudspace_page(self, account='', cloudspace=''):
        self.account = account
        self.cloudspace= cloudspace

        self.open_account_page(self.account)

        self.set_text("cloud_space_search",self.cloudspace)

        cloudspace_id = self.get_text("cloud_space_table_first_element_1")
        self.click("cloud_space_table_first_element_1")

        if cloudspace_id in self.get_url():
            return True
        else:
            raise NoSuchElementException

    def delete_cloudspace(self,account='', cloudspace=''):
        self.account = account
        self.cloudspace = cloudspace

        self.lg('open %s cloudspace' % cloudspace)
        self.open_cloudspace_page(self.account,self.cloudspace)

        self.lg('delete the cloudspace')
        self.click('cloudspace_action')
        self.click('cloudspace_delete')
        self.set_text('cloudspace_delete_reason',"Test")
        self.click("cloudspace_delete_confirm")
        self.assertEqual(self.get_text('cloudspace_page_status'),"DESTROYED")

    def create_virtual_machine(self, account='', cloudspace='', machine_name='',image='',memory='',disk=''):
        self.account = account
        self.cloudspace= cloudspace
        self.machine_name = machine_name or str(uuid.uuid4()).replace('-', '')[0:10]
        self.image = image or 'Ubuntu 15.10'
        self.memory = memory or '1024 MB'
        self.disk = disk or '50 GB'

        self.lg('open the cloudspace page')
        self.open_cloudspace_page(self.account,self.cloudspace)

        self.lg('add virtual machine')
        self.click('add_virtual_machine')
        self.assertEqual(self.get_text('create_virtual_machine_on_cpu_node'),'Create Machine On CPU Node')

        self.lg('enter the machine name')
        self.set_text('machine_name',self.machine_name)

        self.lg('enter the machien description')
        self.set_text('machine_description',str(uuid.uuid4()).replace('-', '')[0:10])

        self.lg('select the image')
        self.select('machine_images_list',self.image)

        self.lg('select the memory')
        self.select('machine_memory_list',self.memory)

        self.lg('select the disk')
        self.select('machine_disk_list',self.disk)

        self.lg('create machine confirm button')
        self.click('machine_confirm_button')

    def open_virtual_machine_page(self,account='',cloudspace='',machine_name=''):
        self.account = account
        self.cloudspace = cloudspace
        self.machine_name = machine_name

        self.lg('opne %s cloudspace' % cloudspace)
        self.open_cloudspace_page(self.account,self.cloudspace)

        self.lg('open %s virtual machine' % machine_name)
        self.set_text('virtual machine search',self.machine_name)
        vm_id = self.get_text("virtual_machine_tabkle_first_element_2")[3:]
        self.click('virtual_machine_table_first_element')

        if vm_id in self.get_url():
            return True
        else:
            raise NoSuchElementException

    def delete_virtual_machine(self,account='', cloudspace='', machine_name=''):
        self.account = account
        self.cloudspace = cloudspace
        self.machine_name = machine_name

        self.lg('open %s virtual machine' % machine_name)
        self.open_virtual_machine_page(self.account,self.cloudspace,self.machine_name)

        self.lg('delete the machine')
        self.click('virtual_machine_action')
        self.click('virtual_machine_delete')
        self.set_text('virtual_machine_delete_reason',"Test")
        self.click("virtual_machine_delete_confirm")
        self.assertEqual(self.get_text('virtual_machine_page_status'),"DESTROYED")

