import re
import time
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
from nose_parameterized import parameterized
import unittest
from random import randint

class GridTests(Framework):
    def setUp(self):
        super(GridTests, self).setUp()
        self.Login.Login()
        self.ErrorConditions.get_it()


    def test001_error_condition_page(self):
        """ PRTL-021
        *Test case for checking error condition page in the admin portal*

        **Test Scenario:**

        #. do login using admin username/password, should succeed
        #. click grid arrow then click on error condition
        #. check that all elements on error condition page exist
        #. check if show 10 and 25 entries works as expected
        #. click action button then click on purge
        #. select All and click on confirm, and check that all ECS are deleted
        """
        self.lg('%s STARTED' % self._testID)
        EC_headers=['Grid Portal','Error Conditions']
        EC_titles=['Error Conditions']
        self.lg('check page headers')
        self.assertEqual(self.get_navigation_bar('navigation bar'),EC_headers)
        self.lg('check page title')
        self.assertEqual(self.get_page_titles(),EC_titles)
        self.assertTrue(self.ErrorConditions.check_EC_table_heads('ECs'))
        self.lg('click action button then click on purge')
        self.click('ec_action_button')
        self.click('purge_button')
        self.lg('select 3 dayes before  and click on confirm, and check that all ECS are deleted')
        self.select('select_purge_options','Older than 3 Days')
        self.click('action_purge_confirm_button')
        self.assertEqual(self.ErrorConditions.ECs_in_tables_after_purge(3),0)
        self.lg('%s ENDED' % self._testID)

    def test002_EC_page_table_sorting(self):
        """ PRTL-050

        *Test case to make sure that sorting of EC  page are working as expected*

        **Test Scenario:**

        #. go to EC page.
        #. get all table head elements
        #. sorting of all fields of EC table, should be working as expected

        """
        self.lg('%s STARTED' % self._testID)
        self.assertTrue(self.Tables.check_sorting_table('ECs'))

    def test003_EC_page_table_paging_buttons(self):
        """ PRTL-051

        *Test case to make sure that paging of Ec page are working as expected*

        **Test Scenario:**

        #. go to EC page.
        #. get number of ECS
        #. try paging from start/previous/next/last and verify it should succeed

        """
        self.lg('%s STARTED' % self._testID)
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons('ECs'))
        self.lg('%s ENDED' % self._testID)

    @parameterized.expand(['Last Occurrence',
                           'Error Message',
                           'App name',
                           'Occurrences',
                          'Node ID',
                          'Grid ID' ])
    def test004_EC_page_searchbox(self,column):
        """ PRTL-052

        *Test case to make sure that search boxes of EC page are working as expected*

        **Test Scenario:**

        #. go to ECs page.
        #. try use general search box  to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column and  verfiy it return the right value

        """
        skip_columns=['Last Occurrence','Occurrences','Node ID','Grid ID']
        if column in skip_columns:
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/762')
        if column == 'Error Message':
           self.skipTest('https://github.com/0-complexity/openvcloud/issues/771')
        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box('ECs',column ))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('ECs',column ))

    def test005_specific_Ec_page(self):
        """ PRTL-053
        *Test case to make sure that element on EC page are working as expected*

        **Test Scenario:**

        #. go to ECs page
        #. open one EC page
        #. check that all elements on grid page exist(headers)
        #. check that right error message
        #. check that you can get (type , APPLication Name,Category,Type,level,creation time,last_time,occurrence,Error Message Pub,Function Name,Function Line Number,Function File Number,node,Grid,tags)
        #. check that you can get  node page which error occure on it
        #. checl that you can get code and Backtrace

        """
        self.lg('%s STARTED' % self._testID)
        EC_headers=['Grid Portal','Error Conditions', 'Error Condition']
        EC_titles=['Details']
        self.lg("open one EC page")
        self.ErrorConditions.get_it()
        self.lg('2- open random image page')
        table = self.Tables.generate_table_elements('ECs')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        EC_element=self.ErrorConditions.random_element(random_elemn_row)
        self.assertTrue(self.ErrorConditions.open_EC_page(EC_element,table))
        self.lg('3-  check that all elements on grid page exist(headers)')
        self.assertEqual(self.get_navigation_bar('navigation bar'),EC_headers)
        self.assertEqual(self.get_page_titles(),EC_titles)
        self.assertEqual(self.get_text('Error_message_title'),'Error Message')
        self.lg('4- check that can use delete opion from action ')
        self.ErrorConditions.Error_Condition_action()
        self.lg('5- check that right error message %s'%EC_element)
        self.assertTrue(EC_element in self.get_text('Error_condition_message'))
        self.lg('6-check that you can get (type ,Category,Type,level,creation time,Error Message Pub,Function Name,Function Line Number,Function File Number,tags)')
        self.ErrorConditions.check_exist_of_EC_elements()
        self.lg('7- check that APPLication Name,last_time,occurrence,node,Grid same as ECs table ')
        self.ErrorConditions.check_EC_elements()
        self.lg('8-check that you can get code and Backtrace')
        self.assertEqual(str(self.get_text('EC_code')),'Code')
        self.assertEqual(str(self.get_text('EC_baketrace')),'BackTrace')
        self.lg('9-check that you can get  node page which error occure on it')
        self.assertTrue(self.ErrorConditions.get_cpu_node_page())

    @unittest.skip('https://github.com/0-complexity/openvcloud/issues/774')
    def test006_get_job_from_Ec_page(self):
        """ PRTL-054
        *Test case to make sure that element on EC page are working as expected*

        **Test Scenario:**

        #. go to ECs page
        #. open one EC page
        #. check that you can get job page of error

        """
        self.lg('%s STARTED' % self._testID)
        self.lg("open one EC page")
        self.ErrorConditions.get_it()
        self.lg('2- open random image page')
        table = self.Tables.generate_table_elements('ECs')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        EC_element=self.ErrorConditions.random_element(random_elemn_row)
        self.assertTrue(self.ErrorConditions.open_EC_page(EC_element,table))
        self.lg('3- check that you can get job page of error')
        self.assertTrue(self.ErrorConditions.get_job_page(random_elemn_row[2]))
