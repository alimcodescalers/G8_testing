from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework

class StatusTests(Framework):
    def setUp(self):
        super(StatusTests, self).setUp()
        self.Login.Login()
        self.StatusOverview.get_it()

    def test01_check_process_status(self):
        """ PRTL-029
        *Test case to make sure that the process status is working as expected*

        **Test Scenario:**

        #. go to status overview page
        #. verify machines table status/color
        #. press on "Run Healthcheck"
        #. verify expected behavior

        """
        NodeStatus = self.StatusOverview.get_node_status()
        for status in NodeStatus:
            self.assertEqual(status, "RUNNING", "Error: %s " % status)


    def test02_health_check(self):
        """ PRTL-030
        *Test case to make sure that the health check is working as expected*

        **Test Scenario:**

        #. go to status overview page
        #. press on "Run Healthcheck"
        #. verify expected behavior
        """
        health_check = self.StatusOverview.run_health_check()
        self.assertEqual(health_check, 'Scheduled healthcheck', 'Health check message: %s' % health_check)

    #def test03_status_overview_page(self):
    #   """ PRTL-054
    #    *Test case to make sure that health check page is working as expected*
    #    **Test Scenario:**
    #   #. check that "process Status" in header of page
    #   #. check that last check in header
    #   #. check that you can get grid node page
    #   #. check that you can get Detail of status  page
    #   """


    #def test04_status_overview_page_table_sorting(self):
    #   """ PRTL-055
    #    *Test case to make sure that sorting of health check  page are working as expected*
    #    **Test Scenario:**
    #    #. go to Health check page.
    #    #. get all table head elements
    #    #. sorting of all fields of health_check page table, should be working as expected
    #    """


    #def test05_status_overview_page_table_paging_buttons(self)
    #""" PRTL-056
    #*Test case to make sure that paging of healthcheck page are working as expected*
    #**Test Scenario:**
    #  #. go to healthcheck page.
    #  #. try paging from the available page numbers and verify it should succeed
    #  #. try paging from start/previous/next/last and verify it should succeed
    # """

    #def test06_status_overview_page_searchbox(self):
    #    """ PRTL-057
    #    *Test case to make sure that search boxes of healthcheck page are working as expected*
    #        **Test Scenario:**
    #        #. go to healthchecks page.
    #        #. try use general search box  to search for values in  all columns and verfiy it return the right value
    #        #. try use the search box in every column and  verfiy it return the right value
    #        """


    #def test07_status_overview_details_page(self):
    #   """ PRTL-058
    #    *Test case to make sure that details_status_overview of every page running well*
    #    **Test Scenario:**
    #   #. check that "Monitoring Status " in header of page and last ckeck
    #   #. check that name of node and grid correct and can get their page
    #   #. press on "Run Healthcheck" and verify expected behavior
    #   #. check that you can pree all element and they have mnessage
    #   """
