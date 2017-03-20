import re
import time
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
from nose_parameterized import parameterized
import unittest

class GridAudits(Framework):

    def setUp(self):
        super(GridAudits, self).setUp()
        self.Login.Login()
    @unittest.skip("https://github.com/0-complexity/openvcloud/issues/815")
    def test01_Audits_page_basic_elements(self):
        """ PRTL-001

        *Test case to make sure that Audits page is working as expected*

        **Test Scenario:**

        #. get audits page from grid
        #. check driver url & title
        #. check navigation bar
        #. check page titles
        #. check 'show records per page' entries

        """
        self.lg('%s STARTED' % self._testID)
        Audits_headers=['Grid Portal','Audits']
        Audits_titles=['Audits']
        self.lg('get job page')
        self.Audits.get_it()
        self.assertTrue(self.Audits.is_at())
        self.lg('check page headers')
        self.assertEqual(self.get_navigation_bar('navigation bar'),Audits_headers)
        self.lg('check page title')
        #self.assertEqual(self.get_page_titles(),jobs_titles)
        self.assertTrue(self.Audits.check_Audits_table_heads('Audits'))
        self.lg('check "show records per page" entries')
        self.assertTrue(self.element_is_enabled('table_Audits_selector'))
        self.lg('%s ENDED' % self._testID)

    def test02_Audits_page_table_paging_buttons(self):
        """ PRTL-002
        *Test case to make sure that paging of Audits_page are working as expected*

        **Test Scenario:**

        #. get Audits page from grid
        #. try paging from the available page numbers and verify it should succeed
        """

        self.lg('%s STARTED' % self._testID)
        self.Audits.get_it()
        self.assertTrue(self.Audits.is_at())
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons('Audits'))
        self.lg('%s ENDED' % self._testID)

    def test03_Audits_page_table_sorting(self):
        """ PRTL-003

        *Test case to make sure that sorting of Audits_page are working as expected*

        **Test Scenario:**

        #. get Audits page from grid
        #. get all table head elements
        #. sorting of all fields of Audits_page table, should be working as expected

        """
        self.lg('%s STARTED' % self._testID)
        self.Audits.get_it()
        self.assertTrue(self.Audits.is_at())
        self.lg('sorting of all fields of Audit page table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('Audits'))
        self.lg('%s ENDED' % self._testID)

    @parameterized.expand(['Time',
                           'User',
                           'Call',
                           'Response Time',
                          'Status Code',
                           ])
    def test04_Audits_page_searchbox(self,column):
        """ PRTL-004

        *Test case to make sure that search boxes of Audits_page are working as expected*

        **Test Scenario:**

        #. go to Audits.
        #. try use general search box  to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column and  verfiy it return the right value

        """
        skip_columns=['Time','Response Time','Status Code']
        if column in skip_columns:
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/811')
        self.Audits.get_it()
        self.assertTrue(self.Audits.is_at())
        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box('Audits',column ))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('Audits',column ))

    def test05_specific_Audit_page(self):
        """ PRTL-005
        *Test case to make sure that element on Audits page are working as expected*

        **Test Scenario:**

        #. go to Audits page
        #. open one Audits page
        #. check Audits_page_basic_elements[titles,headers]
        #. check that you can get (type , APPLication Name,Category,Type,level,creation time,last_time,occurrence,Error Message Pub,Function Name,Function Line Number,Function File Number,node,Grid,tags)
        #. check that you can get  node page which error occure on it
        #. checl that you can get code and Backtrace

        """
        self.lg('%s STARTED' % self._testID)
        audit_headers=['Grid Portal','Audits', 'Audit']
        audit_titles=['Audit:','Arguments:','Keyword Arguments:','Result:']
        self.lg("open one job page")
        self.Audits.get_it()
        self.assertTrue(self.Audits.is_at())
        self.lg('2- open random Audit page')
        table = self.Tables.generate_table_elements('Audits')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        self.assertTrue(self.Audits.open_Audit_page(random_elemn_row[2],table))
        self.lg('3- check audit_page_basic_elements[titles,headers]')
        self.assertEqual(self.get_navigation_bar('navigation bar'),audit_headers)
        self.assertEqual(self.get_page_titles(),audit_titles)
        self.lg('4-check that you can get (Time,User,Call,Status Code,Response Time,Tags,Link to Error Condition')
        self.assertTrue(self.Audits.check_exist_of_audit_elements())
        self.lg('5- check that it contain correct elemnts ')
        self.Audits.check_audit_elements()
