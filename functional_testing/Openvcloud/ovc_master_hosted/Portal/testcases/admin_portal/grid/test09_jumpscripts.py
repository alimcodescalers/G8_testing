import re
import time
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
from nose_parameterized import parameterized
import unittest

class GridJumpscripts(Framework):

    def setUp(self):
        super(GridJumpscripts, self).setUp()
        self.Login.Login()


    def test01_jumpscripts_page_basic_elements(self):
        """ PRTL-001

        *Test case to make sure that jumpscripts_page is working as expected*

        **Test Scenario:**

        #. get jumpscripts page from grid
        #. check driver url & title
        #. check navigation bar
        #. check page titles
        #. check 'show records per page' entries

        """
        self.lg('%s STARTED' % self._testID)
        jumpscripts_headers=['Grid Portal','JumpScripts']
        jumpscripts_titles=['JumpScripts']
        self.lg('get jumpscripts page')
        self.JumpScripts.get_it()
        self.assertTrue(self.JumpScripts.is_at())
        self.lg('check page headers')
        self.assertEqual(self.get_navigation_bar('navigation bar'),jumpscripts_headers)
        self.lg('check page title')
        self.assertEqual(self.get_page_titles(),jumpscripts_titles)
        self.assertTrue(self.JumpScripts.check_jumpscripts_table_heads('jumpscripts'))
        self.lg('check "show records per page" entries')
        self.assertTrue(self.element_is_enabled('table_jumpscripts_selector'))
        self.lg('%s ENDED' % self._testID)

    def test02_jumpscripts_page_table_paging_buttons(self):
        """ PRTL-002
        *Test case to make sure that paging of jumpscripts_page are working as expected*

        **Test Scenario:**

        #. get jumpscripts_page  from grid
        #. try paging from the available page numbers and verify it should succeed
        """

        self.lg('%s STARTED' % self._testID)
        self.lg('get jumpscripts page')
        self.JumpScripts.get_it()
        self.assertTrue(self.JumpScripts.is_at())
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons('jumpscripts'))
        self.lg('%s ENDED' % self._testID)

    def test03_jumpscripts_page_table_sorting(self):
        """ PRTL-003

        *Test case to make sure that sorting of jumpscripts_page are working as expected*

        **Test Scenario:**

        #. get jumpscripts_page  from grid
        #. get all table head elements
        #. sorting of all fields of jumpscript_page table, should be working as expected

        """
        self.lg('%s STARTED' % self._testID)
        self.lg('get jumpscripts page')
        self.JumpScripts.get_it()
        self.assertTrue(self.JumpScripts.is_at())
        self.lg('sorting of all fields of job page table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('jumpscripts'))
        self.lg('%s ENDED' % self._testID)

    @parameterized.expand(['ID',
                           'Name',
                           'Organization',
                           'Category',
                           'Description'
                           ])
    def test04_jumpscripts_page_searchbox(self,column):
        """ PRTL-004

        *Test case to make sure that search boxes of jumpscripts_page are working as expected*

        **Test Scenario:**

        #. go to jumpscripts_page.
        #. try use general search box  to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column and  verfiy it return the right value

        """
        skip_columns=['ID','Description']
        if column in skip_columns:
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/821')
        self.lg('get jumpscripts page')
        self.JumpScripts.get_it()
        self.assertTrue(self.JumpScripts.is_at())
        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box('jumpscripts',column ))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('jumpscripts',column ))

    def test05_specific_jumpscript_page(self):
        """ PRTL-005
        *Test case to make sure that element on jumpscript page are working as expected*

        **Test Scenario:**

        #. go to jumpscripts page
        #. open one jumpscript page
        #. check jumpscript_page_basic_elements[titles,headers]
        #. check that you can get all Properts
        #. check that you can get code of this jumpscript

        """
        self.lg('%s STARTED' % self._testID)
        JumpScript_titles=['JumpScript Details','Jobs that have executed this Jumpscript']
        self.lg('get jumpscripts page')
        self.JumpScripts.get_it()
        self.assertTrue(self.JumpScripts.is_at())
        self.lg('2- open random image page')
        table = self.Tables.generate_table_elements('jumpscripts')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        JumpScript_headers=['Grid Portal','JumpScripts',str('JumpScript: %s'%random_elemn_row[1])]
        self.assertTrue(self.JumpScripts.open_Jumpscript_page(random_elemn_row[0],table))
        self.lg('3- check job_page_basic_elements[titles,headers]')
        self.assertEqual(self.get_navigation_bar('navigation bar'),JumpScript_headers)
        self.assertEqual(self.get_page_titles(),JumpScript_titles)
        self.lg('4-check that you can get all Properts')
        self.assertTrue(self.JumpScripts.check_exist_of_jumpscript_properts())
        self.lg('5-check that you can get code of this jumpscript')
        self.assertTrue(self.JumpScripts.check_exist_of_code())

    def test06_Jobs_that_have_executed_Jumpscript(self):
        """ PRTL-006
        *Test case to make sure that table of Jobs that have executed Jumpscript are working as expected*

        **Test Scenario:**

        #. go to jumpscripts page
        #. open one jumpscript  page
        #. check 'show records per page' entries
        #. try paging from the available page numbers and verify it should succeed
        #. sorting of all fields of table, should be working as expected

        """
        self.lg('%s STARTED' % self._testID)
        self.lg('get jumpscripts page')
        self.JumpScripts.get_it()
        self.assertTrue(self.JumpScripts.is_at())
        self.lg('open random jumpscript page')
        table = self.Tables.generate_table_elements('jumpscripts')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        self.assertTrue(self.JumpScripts.open_Jumpscript_page(random_elemn_row[0],table))
        self.lg('check "show records per page" entries')
        self.assertTrue(self.element_is_enabled('table_jobs_selector'))
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_show_list('jobs'))
        self.lg('sorting of all fields of job page table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('jobs'))
        self.lg('%s ENDED' % self._testID)

    @parameterized.expand(['Create Time',
                           'Start',
                           'Stop',
                           'Command',
                          'Queue',
                          'State',
                           ])
    def test07_Jobs_that_have_executed_Jumpscript_table_searchbox(self,column):
        """ PRTL-007

        *Test case to make sure that search boxes of jobs in jumpscript page  are working as expected*

        **Test Scenario:**

        #. go to jumpscripts page
        #. open one jumpscript page
        #. try use general search box in ,logs table to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column in jobs in jumpscript table and  verfiy it return the right value

        """
        skip_columns=['Create Time','Start','Stop']
        if column in skip_columns:
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/811')
        self.JumpScripts.get_it()
        self.assertTrue(self.JumpScripts.is_at())
        self.lg('open random jumpscript page')
        table = self.Tables.generate_table_elements('jumpscripts')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        self.assertTrue(self.JumpScripts.open_Jumpscript_page(random_elemn_row[0],table))
        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box('jobs',column ))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('jobs',column ))
        self.lg('%s ENDED' % self._testID)
