from admin_portal.utils import BaseTest
from admin_portal.page_elements_xpath import machines_page
import time
import uuid
from nose_parameterized import parameterized
from random import randint


class Write(BaseTest):
    def __init__(self, *args, **kwargs):
        super(Read, self).__init__(*args, **kwargs)
        self.elements.update(machines_page.elements)

    def setUp(self):
        super(Read, self).setUp()
        self.login()
        if self.check_element_is_exist("left_menu") == False:
            self.click("left_menu_button")
        self.driver.implicitly_wait(20)

    def test01_machine_get(self):