from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.utils.utils import BaseTest
from pytractor.exceptions import AngularNotFoundException
import time


class login(BaseTest):
    def __init__(self, *args, **kwargs):
        super(login, self).__init__(*args, **kwargs)


    def GetIt(self):
        for temp in range(5):
            try:
                self.driver.get(self.environment_url)
                break
            except AngularNotFoundException:
                time.sleep(1)
        else:
            self.fail('AngularNotFoundException')
        self.driver.set_window_size(1920, 1080)
        if not self.IsAt():
            self.fail("The login page isn't loading well.")

    def IsAt(self):
        for temp in range(5):
            if self.wait_until_element_located(self.elements["username_textbox"]):
                return True
            else:
                self.driver.refresh()
        else:
            return False

    def Login(self, username='', password=''):
        username = username or self.admin_username
        password = password or self.admin_password
        self.GetIt()
        self.lg('Do login using username [%s] and passsword [%s]' % (username, password))
        self.set_text('username_textbox', username)
        self.set_text('password_textbox', password)
        self.click('login_button')
        self.assertEqual(self.get_text("end_user_home"),"Home", "Login failed using username [%s] and passsword [%s]" % (username, password))
        self.lg('Login successfully using username [%s] and passsword [%s]' % (username, password))

