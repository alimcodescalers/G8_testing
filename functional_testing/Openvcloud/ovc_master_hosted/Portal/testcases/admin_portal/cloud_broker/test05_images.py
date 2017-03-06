import time
import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework
from nose_parameterized import parameterized
from random import randint


class ImagesTests(Framework):
    def setUp(self):
        super(ImagesTests, self).setUp()
        #self.Login.Login(username=self.admin_username, password=self.admin_password)
        cookies = {"name":"beaker.session.id", "value":"46def9bf87574cb2bce7511404fb5595"}
        self.get_page(self.environment_url)
        self.driver.add_cookie(cookies)
        self.driver.refresh()


    def test01_image_page_paging_table(self):
        """ PRTL-041
        *Test case to make sure that paging and sorting of image  page are working as expected*

        **Test Scenario:**cd
        #. go to Images page.
        #. get number of images
        #. try paging from the available page numbers and verify it should succeed
        """
        pass
        self.lg('%s STARTED' % self._testID)
        self.lg('1- go to Images page')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        self.lg('2- try paging from the available page numbers and verify it should succeed ')
        self.assertTrue(self.Tables.check_show_list('images'))

    def test02_image_page_table_sorting(self):
        """ PRTL-042
        *Test case to make sure that paging and sorting of images page are working as expected*

        **Test Scenario:**
        #. go to image page.
        #. get all table head elements
        #. sorting of all fields of images table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('- go to image bage')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        self.assertTrue(self.Tables.check_sorting_table('images'))

    def test03_image_page_table_paging_buttons(self):
        """ PRTL-043
        *Test case to make sure that paging and sorting of images page are working as expected*

        **Test Scenario:**

        #. go to images page.
        #. get number of images
        #. try paging from start/previous/next/last and verify it should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        self.assertTrue(self.Tables.check_next_previous_buttons('images'))


    @parameterized.expand(['Name',
                           'Location',
                           'Type',
                           'Status',
                          'Size'])
    def test04_image_page_searchbox(self,opertaion):
        """ PRTL-044
        *Test case to make sure that search boxes of images page are working as expected*

        **Test Scenario:**

        #. go to images page.
        #. try use general search box  to search for values in  all columns and verfiy it return the right value
        #. try use the search box in every column and  verfiy it return the right value
        """

        if (opertaion == 'Location' ) or  (opertaion == 'Size'):
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/696')
        if opertaion == 'Size':
           self.skipTest('https://github.com/0-complexity/openvcloud/issues/696')
        self.lg('1- go to Images page')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        self.lg('try general search box to search for values in all columns and verfiy it return the right value')
        self.assertTrue(self.Tables.check_search_box('images',opertaion ))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('images',opertaion ))


    def test05_stack_table_in_image_page_test(self):
        """ PRTL-045

        **Test Scenario:**

        #. go to images page.
        #. open random image page
        #. get number of stacks
        #. try paging from the available page numbers in stack table  and verify it should succeed
        #. sorting of all fields of virtual machine table, should be working as expected
        #. try paging from start/previous/next/last and verify it should succeed
        """
        self.lg('- go to Images page')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        self.lg('- open random image page')
        table = self.Tables.generate_table_elements('images')
        table_elements=self.Tables.get_table_data(table)
        rows= len(table_elements)
        random_elemn= randint(0,rows-1)
        image_element=table_elements[random_elemn][0]
        self.Images.open_image_page(image_element)
        time.sleep(2)
        self.lg('-  try paging from the available page numbers and verify it should succeed ')
        self.assertTrue(self.Tables.check_show_list('stacks'))
        self.lg('- sorting of all fields of stack table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('stacks'))
        self.lg('- try paging from start/previous/next/last and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons('stacks'))


    def test06_VM_table_in_image_page_test(self):
        """ PRTL-046

        **Test Scenario:**

        #. go to images page.
        #. open random image page
        #. get number of vms
        #. try paging from the available page numbers in stack table  and verify it should succeed
        #. sorting of all fields of virtual machine table, should be working as expected
        #. try paging from start/previous/next/last and verify it should succeed
        """
        self.lg('1- go to Images page')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        table = self.Tables.generate_table_elements('images')
        table_elements=self.Tables.get_table_data(table)
        self.lg('2- open random Image page')
        rows= len(table_elements)
        random_elemn= randint(0,rows-1)
        image_element=table_elements[random_elemn][0]
        self.Images.open_image_page(image_element)
        time.sleep(2)
        self.lg('-  try paging from the available page numbers and verify it should succeed ')
        self.assertTrue(self.Tables.check_show_list('machines'))
        self.lg('- sorting of all fields of stack table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('machines'))
        self.lg('- try paging from start/previous/next/last and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons('machines'))

    @parameterized.expand(['ID',
                           'GridID',
                           'Name',
                           'Status',
                          'Reference ID',
                          'Type',
                          'Description'])
    def test07_search_boxes_in_stack_in_image_page_test(self,column):
        """ PRTL-047
        *Test case to make sure that search boxes of stack table  image page are working as expected*

        **Test Scenario:**

        #. go to images page.
        #. open one random  image page
        #. try use general search box  to search for values in  all columns and verfiy it return the right value in stack table
        #. try use the search box in every column and  verfiy it return the right value in stack table
        """
        if column == 'GridID':
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/696')
        if column == 'Reference ID':
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/696')
        self.lg('1- go to Images page')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        self.lg('2-open one random image page')
        table = self.Tables.generate_table_elements('images')
        random_row=self.Tables.get_random_row_from_table(table)
        image_element=random_row[0]
        self.Images.open_image_page(image_element)
        self.lg('-try search boxes in stack table')
        self.assertTrue(self.Tables.check_search_box('stacks',column))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('stacks',column))

    @parameterized.expand(['Name',
                           'Hostname',
                           'Status',
                           'Cloud Space',
                          'Stack ID']
                          )
    def test08_search_boxes_in_VM_in_image_page_test(self,column):
        """ PRTL-048
        *Test case to make sure that search boxes of VM table in image page  are working as expected*

        **Test Scenario:**

        #. go to images page.
        #. open one random  image page
        #. try use general search box  to search for values in  all columns and verfiy it return the right value in VM table
        #. try use the search box in every column and  verfiy it return the right value in VM table
        """
        if column == 'Cloud Space':
            self.skipTest('https://github.com/0-complexity/openvcloud/issues/696')
        self.lg('1- go to Images page')
        self.Images.get_it()
        self.assertTrue(self.Images.is_at())
        self.lg('2-open one random image page')
        table = self.Tables.generate_table_elements('images')
        random_row=self.Tables.get_random_row_from_table(table)
        image_element=random_row[0]
        self.Images.open_image_page(image_element)
        self.lg('-try search boxes in VM table')
        self.assertTrue(self.Tables.check_search_box('machines',column))
        self.lg('try the search box in every column and verfiy it return the right value')
        self.assertTrue(self.Tables.check_data_filters('machines',column))
