from end_user.utils import *
from end_user.page_elements_xpath import home_page

class Support(BaseTest):

    def __init__(self, *args, **kwargs):
        super(Support, self).__init__(*args, **kwargs)
        self.elements.update(home_page.elements)

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