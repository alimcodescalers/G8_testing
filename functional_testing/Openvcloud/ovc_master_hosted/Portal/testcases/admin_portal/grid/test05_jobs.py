import re
import time
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
from nose_parameterized import parameterized
import unittest

class GridJobs(Framework):

    def setUp(self):
        super(GridJobs, self).setUp()
        self.Login.Login()

    #@unittest.skip("https://github.com/0-complexity/openvcloud/issues/810")
    def test01_jobs_page_basic_elements(self):
        """ PRTL-001

        *Test case to make sure that job_page is working as expected*

        **Test Scenario:**

        #. get job page from grid
        #. check driver url & title
        #. check navigation bar
        #. check page titles
        #. check 'show records per page' entries

        """
        self.lg('%s STARTED' % self._testID)
        jobs_headers=['Grid Portal','Jobs']
        jobs_titles=['Jobs','Jobs (Agent Controller 2)']
        self.lg('get job page')
        self.Jobs.get_it()
        self.assertTrue(self.Jobs.is_at())
        self.lg('check page headers')
        self.assertEqual(self.get_navigation_bar('navigation bar'),jobs_headers)
        self.lg('check page title')
        self.assertEqual(self.get_page_titles(),jobs_titles)
        self.assertTrue(self.Jobs.check_jobs_table_heads('jobs'))
        self.lg('click action button then click on purge')
        self.click('action_button')
        self.click('job_purge_button')
        self.lg('select 3 dayes before  and click on confirm, and check that all ECS are deleted')
        self.select('select_purge_options','Older than 3 Days')
        self.click('action_purge_confirm_button')
        self.assertEqual(self.Jobs.jobs_in_tables_after_purge(1,0),0)
        self.lg('check "show records per page" entries')
        self.assertTrue(self.element_is_enabled('table_jobs_selector'))
        self.lg('%s ENDED' % self._testID)

    def test02_jobs_page_table_paging_buttons(self):
        """ PRTL-002
        *Test case to make sure that paging of jobs_page are working as expected*

        **Test Scenario:**

        #. get job page from grid
        #. try paging from the available page numbers and verify it should succeed
        """

        self.lg('%s STARTED' % self._testID)
        self.Jobs.get_it()
        self.assertTrue(self.Jobs.is_at())
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons('jobs'))
        self.lg('%s ENDED' % self._testID)

    def test03_jobs_page_table_sorting(self):
        """ PRTL-003

        *Test case to make sure that sorting of jobs_page are working as expected*

        **Test Scenario:**

        #. get job page from grid
        #. get all table head elements
        #. sorting of all fields of job_page table, should be working as expected

        """
        self.lg('%s STARTED' % self._testID)
        self.Jobs.get_it()
        self.assertTrue(self.Jobs.is_at())
        self.lg('sorting of all fields of job page table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('job'))
        self.lg('%s ENDED' % self._testID)

    @parameterized.expand(['Create Time',
                           'Start',
                           'Stop',
                           'Command',
                          'Queue',
                          'State',
                           ])
    def test04_job_page_searchbox(self,column):
        """ PRTL-004

        *Test case to make sure that search boxes of job_page are working as expected*

        **Test Scenario:**

        #. go to job.
        #. try use general search box  to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column and  verfiy it return the right value

        """
        skip_columns=['Create Time','Start','Stop']
        if column in skip_columns:
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/811')
        self.Jobs.get_it()
        self.assertTrue(self.Jobs.is_at())
        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box('jobs',column ))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('jobs',column ))

    def test05_specific_job_page(self):
        """ PRTL-005
        *Test case to make sure that element on Job page are working as expected*

        **Test Scenario:**

        #. go to jobs page
        #. open one job page
        #. check job_page_basic_elements[titles,headers]
        #. check that you can get (type , APPLication Name,Category,Type,level,creation time,last_time,occurrence,Error Message Pub,Function Name,Function Line Number,Function File Number,node,Grid,tags)
        #. check that you can get  node page which error occure on it
        #. checl that you can get code and Backtrace

        """
        self.lg('%s STARTED' % self._testID)
        Job_headers=['Grid Portal','Jobs', 'Job']
        Job_titles=['Job Details','Job Params','Result','Logs','Additional Info']
        self.lg("open one job page")
        self.Jobs.get_it()
        self.assertTrue(self.Jobs.is_at())
        self.lg('2- open random image page')
        table = self.Tables.generate_table_elements('jobs')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        self.assertTrue(self.Jobs.open_Job_page(random_elemn_row[3],table))
        self.lg('3- check job_page_basic_elements[titles,headers]')
        self.assertEqual(self.get_navigation_bar('navigation bar'),Job_headers)
        self.assertEqual(self.get_page_titles(),Job_titles)
        self.lg('4-check that you can get (grid Id,Node,Roles,Jumpscript,Start,Stop,Queue,State')
        self.assertTrue(self.Jobs.check_exist_of_job_elements())
        self.lg('5- check that Start ,Stop,Queue ,State same as jobs table ')
        self.Jobs.check_job_elements()
        self.lg("7-check addition info in job bage")
        self.Jobs.check_exist_of_additional_info_elements()
        self.lg('6-check that you can get  Jumpscript and node page which job  on it')
        self.assertTrue(self.Jobs.get_cpu_node_page())
        self.assertTrue(self.Jobs.open_Job_page(random_elemn_row[3],table))
        self.assertTrue(self.Jobs.get_jumpscript_page())

    def test06_logs_table_in_job_page(self):
        """ PRTL-006
        *Test case to make sure that element on Job page are working as expected*

        **Test Scenario:**

        #. go to jobs page
        #. open one job page
        #. check 'show records per page' entries
        #. try paging from the available page numbers and verify it should succeed
        #. sorting of all fields of job page table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)
        Job_headers=['Grid Portal','Jobs', 'Job']
        Job_titles=['Job Details','Job Params','Result','Logs','Additional Info']
        self.lg("open one job page")
        self.Jobs.get_it()
        self.assertTrue(self.Jobs.is_at())
        self.lg('open random image page')
        table = self.Tables.generate_table_elements('jobs')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        self.assertTrue(self.Jobs.open_Job_page(random_elemn_row[3],table))
        self.lg('check "show records per page" entries')
        self.assertTrue(self.element_is_enabled('table_joblogs_selector'))
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_show_list('joblogs'))
        self.lg('sorting of all fields of job page table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('joblogs'))
        self.lg('%s ENDED' % self._testID)

    @parameterized.expand(['Start time',
                            'App Name',
                            'Category',
                            'Message',
                           'Level',
                           'Node ID',
                            ])
    def test04_logs_table_in_job_page_searchbox(self,column):
        """ PRTL-007

        *Test case to make sure that search boxes of job_page are working as expected*

        **Test Scenario:**

        #. go to jobs page
        #. open one job page
        #. try use general search box in ,logs table to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column in logs table and  verfiy it return the right value

        """
        skip_columns=['Start time','Level','Node ID']
        if column in skip_columns:
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/811')
        self.Jobs.get_it()
        self.assertTrue(self.Jobs.is_at())
        self.lg('open random image page')
        table = self.Tables.generate_table_elements('jobs')
        random_elemn_row=self.Tables.get_random_row_from_table(table)
        self.assertTrue(self.Jobs.open_Job_page(random_elemn_row[3],table))
        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box('joblogs',column ))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('joblogs',column ))
        self.lg('%s ENDED' % self._testID)
