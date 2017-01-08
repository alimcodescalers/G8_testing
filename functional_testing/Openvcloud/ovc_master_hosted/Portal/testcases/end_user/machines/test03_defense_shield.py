import os
import shutil
import time

from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class DefenseShield(Framework):

    def __init__(self, *args, **kwargs):
        super(DefenseShield, self).__init__(*args, **kwargs)

    def setUp(self):
        super(DefenseShield, self).setUp()
        self.Login.Login()

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
        time.sleep(5)
        download_directory = os.path.abspath('.') + '/downloaded_files'
        downloaded_file_path = download_directory + '/openvpn.zip'
        self.assertTrue(os.path.exists(downloaded_file_path))
        shutil.rmtree(download_directory)
        self.lg('end test case')
