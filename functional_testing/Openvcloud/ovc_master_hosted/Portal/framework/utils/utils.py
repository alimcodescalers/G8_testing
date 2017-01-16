import time
import unittest
import uuid
import logging
from testconfig import config
from pytractor.exceptions import AngularNotFoundException
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pytractor import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support.wait import WebDriverWait
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework import xpath
import os


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.environment_url = config['main']['env']
        self.environment_storage = config['main']['location']
        self.admin_username = config['main']['admin']
        self.admin_password = config['main']['passwd']
        self.GAuth_secret = config['main']['secret']
        self.browser = config['main']['browser']
        self.base_page = self.environment_url + '/ays'
        self.elements = xpath.elements.copy()

    def setUp(self):
        self.CLEANUP = {"users": [], "accounts": []}
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('portal_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.set_browser()
        self.wait = WebDriverWait(self.driver, 15)

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
        '''
        We have to use API to tear down all accounts and users
        '''

        # self.driver.quit()
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s ExecutionTime is %s sec.' % (self._testID, executionTime))


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

    def lg(self, msg):
        self._logger.info(msg)

    def find_elements(self, element):
        method = self.elements[element][0]
        value = self.elements[element][1]
        if method in ['XPATH', 'ID', 'LINK_TEXT', 'CLASS_NAME', 'NAME', 'TAG_NAME']:
            elements_value = self.driver.find_elements(getattr(By, method), value)
        else:
            self.fail("This %s method isn't defined" % method)
        return elements_value

    def find_element(self, element):
        method = self.elements[element][0]
        value = self.elements[element][1]
        if method in ['XPATH', 'ID', 'LINK_TEXT']:
            element_value = self.driver.find_element(getattr(By, method), value)
        elif method in ['CLASS_NAME', 'NAME', 'TAG_NAME']:
            item_order = self.elements[element][2]
            elements_value = self.driver.find_elements(getattr(By, method), value)
            if item_order == -1:
                element_value = elements_value
            else:
                element_value = elements_value[item_order]
        else:
            self.fail("This %s method isn't defined" % method)
        return element_value

    def check_side_list(self):
        for temp in range(3):
            try:
                if self.find_element("left_menu").location["x"] < 0:
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

    def get_page(self, page_url):
        try:
            self.driver.get(page_url)
            self.driver.ignore_synchronization = False
        except AngularNotFoundException:
            self.driver.ignore_synchronization = True
            self.driver.get(page_url)

    def element_is_enabled(self, element):
        return self.find_element(element).is_enabled()

    def element_is_displayed(self, element):
        self.wait_until_element_located(element)
        return self.find_element(element).is_displayed()

    def element_background_color(self, element):
        return str(self.find_element(element).value_of_css_property('background-color'))

    def wait_until_element_located(self, element):
        method = self.elements[element][0]
        value = self.elements[element][1]
        for temp in range(3):
            try:
                self.wait.until(EC.visibility_of_element_located((getattr(By, method), value)))
                return True
            except:
                time.sleep(1)
        else:
            return False

    def wait_element(self, element):
        if self.wait_until_element_located(element):
            return True
        else:
            return False

    def wait_until_element_located_and_has_text(self, element, text):
        method = self.elements[element][0]
        value = self.elements[element][1]
        for temp in range(10):
            try:
                self.wait.until(EC.text_to_be_present_in_element((getattr(By, method), value), text))
                return True
            except:
                time.sleep(1)
        else:
            return False

    def wait_unti_element_clickable(self, element):
        method = self.elements[element][0]
        value = self.elements[element][1]
        for temp in range(10):
            try:
                self.wait.until(EC.element_to_be_clickable((getattr(By, method), value)))
            except (TimeoutException, StaleElementReferenceException):
                time.sleep(1)
            else:
                return True
        else:
            self.fail('StaleElementReferenceException')

    def click(self, element):
        for temp in range(10):
            try:
                self.find_element(element).click()
                break
            except:
                time.sleep(1)
        else:
            self.fail("can't find %s element" % element)
        time.sleep(1)


    def click_item(self, element, ID):
        for temp in range(10):
            method = self.elements[element][0]
            value = self.elements[element][1]
            try:
                self.driver.find_element(getattr(By, method), value % tuple(ID)).click()
                break
            except:
                time.sleep(1)
        else:
            self.fail("can't find %s element" % element)
        time.sleep(1)

    def click_link(self, link):
        self.get_page(link)

    def get_text(self, element):
        for temp in range(10):
            try:
                return self.find_element(element).text
            except:
                time.sleep(0.5)
        else:
            self.fail('NoSuchElementException(%s)' % element)

    def get_size(self, element):
        self.wait_until_element_located(element)
        return self.find_element(element).size

    def get_value(self, element):
        return self.get_attribute(element, "value")

    def element_is_readonly(self, element):
        return self.get_attribute(element, "readonly")

    def element_link(self, element):
        return self.get_attribute(element, "href")

    def get_attribute(self, element, attribute):
        self.wait_until_element_located(element)
        return self.find_element(element).get_attribute(attribute)

    def get_url(self):
        return self.driver.current_url

    def set_text(self, element, value):
        self.wait_until_element_located(element)
        self.find_element(element).clear()
        self.find_element(element).send_keys(value)

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
        item_value = str(item_value)
        self.select_obeject = Select(self.find_element(list_element))
        self.select_list = self.select_obeject.options

        for option in self.select_list:
            if item_value in option.text:
                self.lg("select %s from list" % str(option.text))
                self.select_obeject.select_by_visible_text(option.text)
                item_value = option.text
                break
        else:
            self.fail("This %s item isn't an option in %s list" % (item_value, list_element))

        self.assertEqual(item_value, self.select_obeject.first_selected_option.text)

    def get_list_items(self, list_element):
        html_list = self.find_element(list_element)
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

    def get_storage_list(self):
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

    def get_table_rows(self):
        'This method return all rows in the current page else return false'
        try:
            tbody = self.driver.find_element_by_tag_name('tbody')
            rows = tbody.find_elements_by_tag_name('tr')
            return rows
        except:
            self.lg("Can't get the tbody elements")
            return False

    def get_row_cells(self, row):
        'This method take a row and return its cells elements else return false'
        try:
            cells = row.find_elements_by_tag_name('td')
            return cells
        except:
            self.lg("Can't get the row cells")
            return False

    def get_table_head_elements(self, element):
        # This method return a table head elements.
        for _ in range(10):
            try:
                table = self.find_element(element)
                thead = table.find_elements_by_tag_name('thead')
                thead_row = thead[0].find_elements_by_tag_name('tr')
                return thead_row[0].find_elements_by_tag_name('th')
            except:
                time.sleep(0.5)
        else:
            return False
