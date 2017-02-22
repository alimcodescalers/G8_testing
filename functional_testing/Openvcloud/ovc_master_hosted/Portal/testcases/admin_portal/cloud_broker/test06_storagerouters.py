class StorageRoutersTests(Framework):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test01_storagerrouters_page_basic_elements(self):
        """
        PRTL-001
        *Test case to make sure the basic elements in storage routers page as expected*

        **Test Scenario:**
        #. check page url & title
        #. check navigation bar
        #. check page title
        #. check 'show records per page' list
        """


    def test02_storagerrouters_page_paging_table(self):
        """
        PRTL-002
        *Test case to make sure that show 'records per page' of storage routers page is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. try paging from the available page numbers and verify it should succeed.
        """


    def test03_storagerrouters_page_table_paging_buttons(self):
        """
        PRTL-003
        *Test case to make sure that paging of storage routers page is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. try paging from start/previous/next/last and verify it should succeed.
        """


    def test04_storagerrouters_table_sorting(self):
        """
        PRTL-004
        *Test case to make sure that sorting of storage routers table is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. sorting of all fields of storage routers table, should be working as expected
        """

    def test05_storagerrouters_decommission(self):
        """
        PRTL-005
        *Test case to make sure that 'decommission nodes' is working as expected*

        **Test Scenario:**
        #. go to storage routers page.
        #. choose random node & confirm action decommission node, should succeed
        """
