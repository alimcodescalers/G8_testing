from functional_testing.Openvcloud.ovc_master_hosted.Portal.utils.utils import BaseTest

class Support(BaseTest):

    def __init__(self, *args, **kwargs):
        super(Support, self).__init__(*args, **kwargs)

    def setUp(self):
        super(Support, self).setUp()
        self.login()
        self.click("support_button")

    def test01_support(self):
        """ PRTL-018
        *Test case for check user potal support page.*

        **Test Scenario:**

        #. check all support page elements, should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.assertEqual(self.get_text("support_subheader_label"),
                         "Support")
        self.assertEqual(self.get_text("support_line_label"),
                         "support@greenitglobe.com")
        self.lg('%s ENDED' % self._testID)