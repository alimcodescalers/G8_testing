from .....utils.utils import BaseTest
import unittest

@unittest.skip("bug #344")
class BasicPortalTests(BaseTest):

    def test001_login_and_portal_title(self):
        """ PRTL-001
        *Test case for check user potal login and titles.*

        **Test Scenario:**

        #. check the login page title, should succeed
        #. do login using admin username/password, should succeed
        #. check the home page title, should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('check the login page title, should succeed')
        self.assertEqual(self.driver.title, 'Green IT Globe Login')
        self.lg('do login using admin username/password, should succeed')
        self.login()
        self.lg('check the home page title, should succeed')
        self.assertEqual(self.driver.title, 'OpenvCloud - Decks')
        self.lg('%s ENDED' % self._testID)

    def test002_logout_and_portal_title(self):
        """ PRTL-002
        *Test case for check user potal logout and titles.*

        **Test Scenario:**

        #. check the login page title, should succeed
        #. do login using admin username/password, should succeed
        #. check the home page title, should succeed
        #. do logout, should succeed
        #. check the login page title, should succeed
        #. do login using admin username/password, should succeed
        #. check the home page title, should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('check the login page title, should succeed')
        self.assertEqual(self.driver.title, 'GreenITGlobe Login')
        self.lg('do login using admin username/password, should succeed')
        self.login()
        self.lg('check the home page title, should succeed')
        self.assertEqual(self.driver.title, 'OpenvCloud - Decks')
        self.lg('do logout, should succeed')
        self.logout()
        self.wait_until_element_located("id", "input_0")
        self.assertEqual(self.driver.title, 'GreenITGlobe Login')
        self.lg('do login using admin username/password again, should succeed')
        self.login()
        self.lg('check the home page title, should succeed')
        self.assertEqual(self.driver.title, 'OpenvCloud - Decks')
        self.lg('%s ENDED' % self._testID)
