import re
import time
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
from nose_parameterized import parameterized
import unittest

class VMachinesTests(Framework):

    def setUp(self):
        super(VMachinesTests, self).setUp()
        self.Login.Login()

    def test01_grid_virtual_machine_page_basic_elements(self):
        """ PRTL-000

        *Test case to make sure that virtual_machine_page is working as expected*

        **Test Scenario:**

        #. get virtual machines page from grid
        #. check driver url & title
        #. check navigation bar
        #. check page titles
        #. check 'show records per page' entries

        """
        self.VM_titles=['Virtual Machines']
        self.VM_headers=['Grid Portal', 'Virtual Machines']
        self.lg('get virtualmachines page from grid and check url&title')
        self.GridVirtualMachines.get_it()
        self.assertTrue(self.GridVirtualMachines.is_at())
        self.lg('check navigation bar')
        self.assertEqual(self.get_navigation_bar('navigation bar'),self.VM_headers)
        self.lg('check page titles')
        self.assertEqual(self.get_page_titles(),self.VM_titles)
        self.lg('check "show records per page" entries')
        self.assertTrue(self.element_is_enabled('table_GridVM_selector'))

    def test02_grid_virtual_machine_page_table_paging_buttons(self):
        """ PRTL-000
        *Test case to make sure that paging of virtual_machine_page are working as expected*

        **Test Scenario:**

        #. get virtual machines page from grid
        #. try paging from the available page numbers and verify it should succeed
        #. try paging from start/previous/next/last and verify it should succeed
        """

        self.lg('%s STARTED' % self._testID)
        self.GridVirtualMachines.get_it()
        self.assertTrue(self.GridVirtualMachines.is_at())
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_show_list('GridVM'))
        self.lg('%s ENDED' % self._testID)

    def test03_grid_virtual_machine_page_table_sorting(self):
        """ PRTL-000

        *Test case to make sure that sorting of grid_virtual_machine_page are working as expected*

        **Test Scenario:**

        #. get virtual machines page from grid
        #. get all table head elements
        #. sorting of all fields of grid_virtual_machine_page table, should be working as expected

        """
        self.lg('%s STARTED' % self._testID)
        self.GridVirtualMachines.get_it()
        self.assertTrue(self.GridVirtualMachines.is_at())
        self.lg('sorting of all fields of grid_virtual_machine_page table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('GridVM'))
        self.lg('%s ENDED' % self._testID)

    @parameterized.expand(['Name',
                           'Status',
                           'Active',
                           'Memory',
                          'MAC Address',
                          'Node',
                          'CPU Cores'
                           ])
    def test05_status_overview_page_searchbox(self,column):
        """ PRTL-052

        *Test case to make sure that search boxes of grid_virtual_machine_page are working as expected*

        **Test Scenario:**

        #. go to grid_virtual_machine_page.
        #. try use general search box  to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column and  verfiy it return the right value

        """
        skip_columns=['Memory','MAC Address','Active']
        if column in skip_columns:
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/811')
        self.GridVirtualMachines.get_it()
        self.assertTrue(self.GridVirtualMachines.is_at())
        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box('GridVM',column ))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('GridVM',column ))
