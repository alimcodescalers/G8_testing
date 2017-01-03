from pytractor.exceptions import AngularNotFoundException
import time
import pyotp

class login():
    def __init__(self, framework):
        self.framework = framework

    def GetIt(self):
        for temp in range(5):
            try:
                self.framework.driver.get(self.framework.environment_url)
            except AngularNotFoundException:
                time.sleep(1)
            else:
                #self.framework.click('confirm_alert')
                self.framework.click('landing_page_login')
                break
        else:
            self.framework.fail('AngularNotFoundException')
        self.framework.driver.set_window_size(1920, 1080)
        if not self.IsAt():
            self.framework.fail("The login page isn't loading well.")

    def IsAt(self):
        for temp in range(5):
            if self.framework.wait_until_element_located("username_textbox"):
                return True
            else:
                self.framework.driver.refresh()
        else:
            return False

    def get_GAuth_code(self):
        totp = pyotp.TOTP(self.framework.GAuth_secret)
        GAuth_code = totp.now()
        return GAuth_code

    def Login(self, username='', password=''):
        username = username or self.framework.admin_username
        password = password or self.framework.admin_password
        self.GetIt()
        self.framework.lg('check the login page title, should succeed')
        self.framework.assertEqual(self.framework.driver.title, 'Log in - It\'s You Online')
        self.framework.lg('Do login using username [%s] and passsword [%s]' % (username, password))
        self.framework.set_text('username_textbox', username)
        self.framework.set_text('password_textbox', password)
        self.framework.click('login_button')

        #chech if google auth code is required
        require_GAuth_code = self.framework.wait_until_element_located('GAuth_textbox')
        if require_GAuth_code :
            self.framework.set_text('GAuth_textbox', self.get_GAuth_code())
            self.framework.click('login_button')

        require_authorize = self.framework.wait_until_element_located('authorize_button')
        if require_authorize:
            self.framework.click('authorize_button')

        time.sleep(15)
        self.framework.assertEqual(self.framework.driver.title, 'OpenvCloud - Decks',
                                   "Can't Login using username [%s] and passsword [%s]" % (username, password))

    def LoginFail(self, username='', password=''):
        username = username
        password = password
        self.GetIt()
        self.framework.lg('check the login page title, should succeed')
        self.framework.assertEqual(self.framework.driver.title, 'Log in - It\'s You Online')
        self.framework.lg('Do login using username [%s] and passsword [%s]' % (username, password))
        self.framework.set_text('username_textbox', username)
        self.framework.set_text('password_textbox', password)
        self.framework.click('login_button')
        if password and not username:
            self.framework.assertEqual(self.framework.find_element('username_textbox').get_attribute('aria-invalid'),"true")
            self.framework.assertEqual(self.framework.find_element('password_textbox').get_attribute('aria-invalid'),"false")
        elif username and not password:
            self.framework.assertEqual(self.framework.find_element('password_textbox').get_attribute('aria-invalid'),"true")
            self.framework.assertEqual(self.framework.find_element('username_textbox').get_attribute('aria-invalid'),"false")
        elif not (username and password):
            self.framework.assertEqual(self.framework.find_element('password_textbox').get_attribute('aria-invalid'),"true")
            self.framework.assertEqual(self.framework.find_element('username_textbox').get_attribute('aria-invalid'),"true")
        else:
            self.framework.wait_until_element_located('error_message')
            self.framework.assertEqual(self.framework.find_element('error_message').get_attribute('innerHTML'), "Invalid credentials")
