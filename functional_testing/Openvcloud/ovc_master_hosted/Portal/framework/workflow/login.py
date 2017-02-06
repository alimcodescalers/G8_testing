from pytractor.exceptions import AngularNotFoundException
import time
import pyotp

class login():
    def __init__(self, framework):
        self.framework = framework

    def GetIt(self):
        self.framework.get_page(self.framework.environment_url)
        time.sleep(5)
        self.framework.click('landing_page_login')

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
        self.framework.lg('Do login using')
        self.framework.set_text('username_textbox', username)
        self.framework.set_text('password_textbox', password)
        self.framework.click('login_button')
        time.sleep(20)

        if len(self.framework.find_elements('GAuth_textbox')) > 0:
            self.framework.set_text('GAuth_textbox', self.get_GAuth_code())
            self.framework.click('login_button')
            time.sleep(20)

        if len(self.framework.find_elements("authorize_button")) > 0:
            self.framework.click('authorize_button')
            time.sleep(20)

        self.framework.wait_until_element_located('logout_button')
        self.framework.assertEqual(self.framework.driver.title, 'OpenvCloud - Decks', "Can't Login")

    def LoginFail(self, username='', password=''):
        username = username
        password = password
        self.GetIt()
        self.framework.lg('check the login page title, should succeed')
        self.framework.assertEqual(self.framework.driver.title, 'Log in - It\'s You Online')
        self.framework.lg('Do login')
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
