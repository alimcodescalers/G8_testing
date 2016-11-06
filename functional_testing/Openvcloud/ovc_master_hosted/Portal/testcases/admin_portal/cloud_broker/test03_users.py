from ....utils.utils import BaseTest
from ...page_elements_xpath.cloud_broker import users


class UsersTests(BaseTest):

    def test01_users_page_paging_table_sorting(self):
        """ PRTL-000
        *Test case to make sure that paging and sorting of users page are working as expected*

        **Test Scenario:**
        #. go to users page.
        #. try paging from the available page numbers and verify it should succeed
        #. try paging from start/previous/next/last and verify it should succeed
        #. try sorting for all fields and verify it should succeed
        """


