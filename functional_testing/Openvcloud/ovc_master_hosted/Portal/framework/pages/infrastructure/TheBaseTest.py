import logging
import os
import time
import unittest
import uuid
from pytractor import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support.wait import WebDriverWait
from testconfig import config
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework import xpath

class TheBaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TheBaseTest, self).__init__(*args, **kwargs)
        self.environment_url = config['main']['env']
        self.environment_storage = config['main']['location']
        self.admin_username = config['main']['admin']
        self.admin_password = config['main']['passwd']
        self.browser = config['main']['browser']
        self.base_page = self.environment_url + '/ays'
        self.elements = xpath.elements.copy()

    def runTest(self):
        pass

    def setUp(self):
        self.CLEANUP = {"users": [], "accounts": []}
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('portal_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.wait = WebDriverWait(self.driver, 30)


        self.username = str(uuid.uuid4()).replace('-', '')[0:10]
        self.account = str(uuid.uuid4()).replace('-', '')[0:10]
        self.cloudspace = str(uuid.uuid4()).replace('-', '')[0:10]
        self.machine_name = str(uuid.uuid4()).replace('-', '')[0:10]
        self.password = str(uuid.uuid4()).replace('-', '')[0:10]
        self.email = str(uuid.uuid4()).replace('-', '')[0:10] + "@g.com"
        self.group = 'user'

    def lg(self, msg):
        self._logger.info(msg)

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

    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        '''
        We have to use API to tear down all accounts and users
        '''

        self.driver.quit()
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s ExecutionTime is %s sec.' % (self._testID, executionTime))