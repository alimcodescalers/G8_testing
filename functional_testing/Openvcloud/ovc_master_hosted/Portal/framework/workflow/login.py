from pytractor.exceptions import AngularNotFoundException
import time


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
                self.framework.click('confirm_alert')
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

    def Login(self, username='', password=''):
        username = username or self.framework.admin_username
        password = password or self.framework.admin_password
        self.GetIt()
        self.framework.lg('check the login page title, should succeed')
        self.framework.assertEqual(self.framework.driver.title, 'Green IT Globe Login')
        self.framework.lg('Do login using username [%s] and passsword [%s]' % (username, password))
        self.framework.set_text('username_textbox', username)
        self.framework.set_text('password_textbox', password)
        self.framework.click('login_button')
        time.sleep(0.5)
        self.framework.assertEqual(self.framework.driver.title, 'OpenvCloud - Decks',
                                   "Can't Login using username [%s] and passsword [%s]" % (username, password))

    def LoginFail(self, username='', password=''):
        username = username
        password = password
        self.GetIt()
        self.framework.lg('check the login page title, should succeed')
        self.framework.assertEqual(self.framework.driver.title, 'Green IT Globe Login')
        self.framework.lg('Do login using username [%s] and passsword [%s]' % (username, password))
        self.framework.set_text('username_textbox', username)
        self.framework.set_text('password_textbox', password)
        self.framework.click('login_button')
        if password and not username:
            self.framework.assertEqual(self.framework.get_text("error_password_message"),
                                       "Required.")
        elif username and not password:
            self.framework.assertEqual(self.framework.get_text("error_message"),
                                       "Required.")
        elif not (username and password):
            self.framework.assertEqual(self.framework.get_text("error_message"),
                                       "Required.")
            self.framework.assertEqual(self.framework.get_text("error_password_message"),
                                       "Required.")
        else:
            self.framework.assertEqual(self.framework.get_text("error_message"),
                                       "The login or password you entered is incorrect.")
