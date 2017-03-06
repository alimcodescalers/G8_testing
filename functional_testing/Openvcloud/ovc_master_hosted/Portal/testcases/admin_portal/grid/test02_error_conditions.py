import re
import time
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
import unittest
from random import randint

class GridTests(Framework):
    def setUp(self):
        super(GridTests, self).setUp()
        #self.Login.Login()
        cookies = {"name":"beaker.session.id", "value":"46def9bf87574cb2bce7511404fb5595"}
        self.get_page(self.environment_url)
        self.driver.add_cookie(cookies)
        self.driver.refresh()

    @unittest.skip('bug #695')
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
        self.ErrorConditions.get_it()

        self.lg('check that all elements on error condition page exist')
        self.assertEqual(self.get_text("grid_portal_header1"), "Grid Portal")
        self.assertEqual(self.get_text("error_conditions_header1"), "Error Conditions")
        self.assertEqual(self.get_text("error_conditions_header2"), "Error Conditions")
        self.assertEqual(self.get_text("ec_table_header1"), "Last Occurrence")
        self.assertEqual(self.get_text("ec_table_header2"), "Error Message")
        self.assertEqual(self.get_text("ec_table_header3"), "App name")
        self.assertEqual(self.get_text("ec_table_header4"), "Occurrences")
        self.assertEqual(self.get_text("ec_table_header5"), "Node ID")
        self.assertEqual(self.get_text("ec_table_header6"), "Grid ID")

        self.lg('check if show 10 and 25 entries works as expected')

        def wait_until_entries_info_change():
            match2 = re.search("(\d+)\s+of", self.get_text("table_ECs_info"))
            while int(match2.group(1)) == 10:
                match2 = re.search("(\d+)\s+of", self.get_text("table_ECs_info"))
                time.sleep(1)

        table_body_height_10 = float(self.get_size("ec_table_body")['height'])
        table_row_height = float(self.get_size("ec_table_row")['height'])
        match = re.search("([\d]*[,]*[\d]*)\s+entries", self.get_text("table_ECs_info"))
        entries_no = int(match.group(1).replace(',', ''))
        if entries_no >= 10:
            self.lg('check the number of table\'s rows,  should be equal to 10')
            self.assertEqual(round(table_body_height_10 / table_row_height), 10.0)
            self.lg('- select show 25 entries')
            self.click('entries_select')
            self.click('entries_select_option2')
            self.click('entries_select')
            if entries_no >= 25:
                self.lg('check the number of table\'s rows,  should be equal to 25')
                wait_until_entries_info_change()
                self.assertEqual(round(float(self.get_size("ec_table_body")['height'])
                                       / table_row_height), 25.0)
            else:
                self.lg('check the number of table\'s rows,  should be between 10 and 25')
                wait_until_entries_info_change()
                num = round(float(self.get_size("ec_table_body")['height']) / table_row_height)
                self.assertTrue(num > 10.0 and num < 25.0)
        else:
            self.lg('check the number of table\'s rows,  should be less than 10')
            self.assertTrue(round(float(self.get_size("ec_table_body")['height'])
                                  / table_row_height) < 10.0)

        self.lg('click action button then click on purge')
        self.click('ec_action_button')
        self.click('purge_button')

        self.lg('select All and click on confirm, and check that all ECS are deleted')
        self.click('action_purge_confirm_button')
        for _ in range(10):
            if self.get_text("ec_table_no_data_text") != "No data available in table":
                time.sleep(1)
            else:
                return True
        else:
            return False

        self.lg('%s ENDED' % self._testID)
    #def test002_EC_page_table_sorting(self):
    #   """ PRTL-050
    #    *Test case to make sure that sorting of EC  page are working as expected*
    #    **Test Scenario:**
    #    #. go to EC page.
    #    #. get all table head elements
    #    #. sorting of all fields of EC table, should be working as expected
    #    """

    #
    # def test003_EC_page_table_paging_buttons(self)
    # """ PRTL-051
    # *Test case to make sure that paging of Ec page are working as expected*
    # **Test Scenario:**
    #  #. go to EC page.
    #  #. get number of ECS
    #  #. try paging from start/previous/next/last and verify it should succeed
    # """

    #def test004_EC_page_searchbox(self):
    #    """ PRTL-052
    #    *Test case to make sure that search boxes of EC page are working as expected*
    #        **Test Scenario:**
    #        #. go to ECs page.
    #        #. try use general search box  to search for values in  all columns and verfiy it return the right value
    #        #. try use the search box in every column and  verfiy it return the right value
    #        """

    def test01_specific_Ec_page(self):
        """ PRTL-053
        *Test case to make sure that element on EC page are working as expected*

        **Test Scenario:**

        #. go to ECs page
        #. open one EC page
        #. check that all elements on grid page exist(headers)
        #. check that right error message
        #. check that you can get job page of error
        #. check that you can get (type , APPLication Name,Category,Type,level,creation time,last_time,occurrence,Error Message Pub,Function Name,Function Line Number,Function File Number,node,Grid,tags)
        #. check that you can get Grid page and node which error occure on it
        #. checl that you can get code and Backtrace
        """
        EC_headers=['Grid Portal','Error Conditions', 'Error Condition']
        self.lg('%s STARTED' % self._testID)
        self.lg("open one EC page")
        self.ErrorConditions.get_it()
        self.lg('2- open random image page')
        table_elements=self.Tables.get_table_data('table_ECs_info')
        self.assertTrue(table_elements)
        EC_element=self.ErrorConditions.random_element(table_elements)
        self.assertTrue(self.ErrorConditions.open_EC_page(EC_element))
        self.lg('3-  check that all elements on grid page exist(headers)')
        self.assertEqual(self.ErrorConditions.get_headers('error_condition_headers'),EC_headers)
        self.assertEqual(self.get_text('Error_Condition_details_title'),'Details')
        self.assertEqual(self.get_text('Error_message_title'),'Error Message')
        self.lg('4- check that can use delete opion from action ')
        self.ErrorConditions.Error_Condition_action()
        self.lg('5- check that right error message %s'%EC_element)
        self.assertTrue(EC_element in self.get_text('Error_condition_message'))
        self.lg('6- check that you can get job page of error')
        #Skip('https://github.com/0-complexity/openvcloud/issues/774')
        #self.assertTrue(self.ErrorConditions.get_job_page(random_element[1][2]))
        self.lg('7-check that you can get (type ,Category,Type,level,creation time,Error Message Pub,Function Name,Function Line Number,Function File Number,tags)')
        self.ErrorConditions.check_exist_of_EC_elements()
        self.lg('8- check that APPLication Name,last_time,occurrence,node,Grid same as ECs table ')
        self.ErrorConditions.check_EC_elements()
        self.lg('9-check that you can get code and Backtrace')
        self.assertEqual(str(self.get_text('EC_code')),'Code')
        self.assertEqual(str(self.get_text('EC_baketrace')),'BackTrace')
        self.lg('10-check that you can get Grid page and node which error occure on it')
        self.ErrorConditions.get_cpu_node_page()
        #skip("https://github.com/0-complexity/openvcloud/issues/750")
        #self.assertTrue(self.ErrorConditions.open_EC_page(EC_element))
        #self.ErrorConditions.get_Grid_page()
