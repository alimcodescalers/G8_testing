import os
import unittest
from testconfig import config
from .....utils.utils import BaseTest
from ...page_elements_xpath import defense_shield_page

@unittest.skip("Bug 347")
class DefenseShield(BaseTest):

    def __init__(self, *args, **kwargs):
        super(DefenseShield, self).__init__(*args, **kwargs)
        self.elements.update(defense_shield_page.elements)

    def setUp(self):
        super(DefenseShield, self).setUp()
        self.login()

    @unittest.skipIf(config['main']['browser'] not in ['chrome', 'firefox'],
                     "This test works only for chrome and firefox")
    def test001_defense_shield_page(self):
        """ PRTL-006
        *Test case for checking defense shield page*

        **Test Scenario:**

        #. do login using admin username/password, should succeed
        #. click defense shield picture
        #. click Download OpenVPN Config button, should download .zip file
        #. click Advanced Shield Configuration button
        #. click close button, should return to defense shield page
        """

        self.click("home")

        self.lg('click defense shield picture')
        self.click('defense_shield_pic')
        self.assertEqual(self.driver.title, 'OpenvCloud - NetworkDeck')

        self.assertEqual(self.get_text("defense_shield_header"),"Defense Shield")
        self.assertEqual(self.get_text("defense_shield_line"),
                         "The Defense Shield is your personal firewall that handles all incoming and "
                         "outgoing traffic for your Cloud Space, your routing and firewall settings.")

        self.lg('click Download OpenVPN Config button, should download .zip file')
        self.click('defense_shield_button1')
        file_path = os.path.expanduser("~")+"/Downloads/"
        self.assertTrue(os.path.isfile(file_path+"openvpn.zip"))
        os.remove(file_path+"openvpn.zip")

        self.lg('click Advanced Shield Configuration button')
        self.click('defense_shield_button2')

        self.lg('click close button, should return to defense shield page')
        self.click("close_button")
        self.assertEqual(self.get_text("defense_shield_header"),"Defense Shield")
        self.lg('%s ENDED' % self._testID)





