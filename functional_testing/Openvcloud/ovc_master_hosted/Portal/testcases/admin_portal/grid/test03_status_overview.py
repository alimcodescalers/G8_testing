from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
from nose_parameterized import parameterized


class StatusTests(Framework):
    def setUp(self):
        super(StatusTests, self).setUp()
        self.Login.Login()
        self.StatusOverview.get_it()

    def test01_health_check(self):
        """ PRTL-030
        *Test case to make sure that the health check is working as expected*

        **Test Scenario:**

        #. go to status overview page
        #. press on "Run Healthcheck"
        #. verify expected behavior
        """
        self.assertTrue(self.StatusOverview.run_health_check('action-RunHealthcheckLabel'))

    def test02_status_overview_page_basic_elements(self):
        """ PRTL-054

        *Test case to make sure that health check page is working as expected*

        **Test Scenario:**

        #. check that "process Status" in header of page
        #. check that last check in header
        #. check that you can get grid node page
        #. check that you can get Detail of status  page

        """
        self.lg('check page url & title')
        self.assertEqual(self.driver.title, 'Grid Status Overview')
        self.assertIn('grid/Status%20Overview', self.driver.current_url)
        self.lg('check navigation bar')
        self.assertEqual(self.get_navigation_bar('navigation bar'), ['Grid Portal','Status Overview'])
        self.lg('check page title')
        self.assertEqual(self.get_text('page title'), 'Process Status')
        self.lg('check "show records per page" list')
        self.assertTrue(self.element_is_enabled('table_storge_routers_selector'))

    def test03_status_overview_page_table_sorting(self):
        """ PRTL-055

        *Test case to make sure that sorting of status_overview  page are working as expected*

        **Test Scenario:**

        #. go to Health check page.
        #. get all table head elements
        #. sorting of all fields of status_overview page table, should be working as expected

        """
        self.lg('%s STARTED' % self._testID)
        self.lg('sorting of all fields of Status_overview_ table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('Status_overview'))
        self.lg('%s ENDED' % self._testID)

    def test04_status_overview_page_table_paging_buttons(self):

        """ PRTL-056
        *Test case to make sure that paging of healthcheck page are working as expected*

        **Test Scenario:**

        #. go to healthcheck page.
        #. try paging from the available page numbers and verify it should succeed
        #. try paging from start/previous/next/last and verify it should succeed
        """

        self.lg('%s STARTED' % self._testID)
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons('Status_overview'))
        self.lg('%s ENDED' % self._testID)


    @parameterized.expand(['Grid ID',
                           'Node ID',
                           'Node Name',
                           'Node Status',
                          'Details',
                           ])
    def test05_status_overview_page_searchbox(self,column):
        """ PRTL-052

        *Test case to make sure that search boxes of EC page are working as expected*

        **Test Scenario:**

        #. go to ECs page.
        #. try use general search box  to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column and  verfiy it return the right value

        """
        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box('Status_overview',column ))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('Status_overview',column ))


    def test06_node_status_overview_page_basic_elements(self):
        """ PRTL-058

        *Test case to make sure that details_status_overview of every page running well*

        **Test Scenario:**
        #. get node status overview page
        #. check that "Monitoring Status " in header of page and last ckeck
        #. check that name of node and grid correct and can get their page
        #. press on "Run Healthcheck" and verify expected behavior
        #. check that you can pree all element and they have mnessage

        """
        table = self.Tables.generate_table_elements('Status_overview')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        Status_overview_header=['Grid Portal','Status Overview',str('Node Status: %s'%random_elemn_row[2])]
        Status_overview_titles= ['Monitoring Status',str('du-conv-2: %s (%s:%s)'%(random_elemn_row[2],random_elemn_row[0],random_elemn_row[1])),'Actions']
        self.lg("get node status overview page ")
        self.StatusOverview.open_Status_overview_page(random_elemn_row[2],table)
        self.lg('check page url & title')
        self.assertEqual(self.driver.title, 'Grid NodeStatus')
        self.lg('check navigation bar')
        self.assertEqual(self.get_navigation_bar('navigation bar'),Status_overview_header)
        self.lg('check page title')
        self.assertEqual(self.get_page_titles(),Status_overview_titles )

    def test07_node_status_health_check(self):
        """ PRTL-030
        *Test case to make sure that the health check is working as expected*

        **Test Scenario:**

        #. go to status overview pag
        #. choose random node and get it
        #. press on "Run Healthcheck"
        #. verify expected behavior
        """
        table = self.Tables.generate_table_elements('Status_overview')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        self.StatusOverview.open_Status_overview_page(random_elemn_row[2],table)
        self.assertTrue(self.StatusOverview.run_health_check('action-RunHealthchecknodeLabel'))
