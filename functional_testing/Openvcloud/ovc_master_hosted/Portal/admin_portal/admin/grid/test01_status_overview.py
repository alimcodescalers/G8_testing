from ....utils.utils import BaseTest
from ...page_elements_xpath.grid import status_overview


class StatusTests(BaseTest):

    def test01_status_overview_page(self):
        """ PRTL-000
        *Test case to make sure that the process status and health check are working as expected*

        **Test Scenario:**
        #. go to status overview page
        #. verify machines table status/color
        #. press on "Run Healthcheck"
        #. verify expected behavior
        """
