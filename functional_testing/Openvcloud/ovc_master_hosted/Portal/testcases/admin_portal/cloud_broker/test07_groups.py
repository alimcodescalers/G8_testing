import uuid
import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class GroupsTests(Framework):

    def setUp(self):
        super(GroupsTests, self).setUp()
        self.Login.Login(username=self.admin_username, password=self.admin_password)
        self.navigation_bar = 'navigation bar'
        self.lg('go to groups page')
        self.Groups.get_it()
        self.assertTrue(self.Groups.is_at())

    def test01_groups_page_basic_elements(self):
        """
        PRTL-001
        *Test case to make sure the basic elements in groups page as expected*

        **Test Scenario:**
        #. go to groups page
        #. check page url & title
        #. check navigation bar
        #. check page title
        #. check 'show records per page' list
        """
        self.lg('check page url & title')
        self.assertEqual(self.driver.title, 'CBGrid - Groups')
        self.assertIn('cbgrid/groups', self.driver.current_url)
        self.lg('check navigation bar')
        self.assertEqual(self.get_navigation_bar(self.navigation_bar), ['Cloud Broker','Groups'])
        self.lg('check page title')
        self.assertEqual(self.get_text('page title'), 'Group List')
        self.lg('check "show records per page" list')
        self.assertTrue(self.element_is_enabled('table_groups_selector'))

    def test02_groups_page_paging_table(self):
        """
        PRTL-002
        *Test case to make sure that show 'records per page' of groups page is working as expected*

        **Test Scenario:**
        #. go to groups.
        #. try paging from the available page numbers and verify it should succeed.
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('try paging from the available page numbers and verify it should succeed')
        self.assertTrue(self.Tables.check_show_list('groups'))

        self.lg('%s ENDED' % self._testID)

    def test03_groups_page_table_paging_buttons(self):
        """
        PRTL-003
        *Test case to make sure that paging of groups page is working as expected*

        **Test Scenario:**
        #. go to groups page.
        #. try paging from start/previous/next/last and verify it should succeed.
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('try paging from start/previous/next/last and verify it should succeed')
        self.assertTrue(self.Tables.check_next_previous_buttons('groups'))
        self.lg('%s ENDED' % self._testID)

    def test04_groups_table_sorting(self):
        """
        PRTL-004
        *Test case to make sure that sorting of groups table is working as expected*

        **Test Scenario:**
        #. go to groups page.
        #. sorting of all fields of groups table, should be working as expected
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('sorting of all fields of groups table, should be working as expected')
        self.assertTrue(self.Tables.check_sorting_table('groups'))
        self.lg('%s ENDED' % self._testID)

    def test05_groups_add_group(self):
        """
        PRTL-005
        *Test case to make sure that adding new groups is working as expected*

        **Test Scenario:**
        #. go to groups page.
        #. add new group.
        #. open group page & validate it
        """
        self.lg('%s STARTED' % self._testID)
        name =  str(uuid.uuid4()).replace('-', '')[0:10]
        domain =  str(uuid.uuid4()).replace('-', '')[0:10]
        description =  str(uuid.uuid4()).replace('-', '')[0:10]
        self.assertTrue(self.Groups.create_new_group(name, domain, description))
        self.assertTrue(self.Groups.open_group_page(name))
        self.assertEqual(self.get_text('group_page_name'), 'Name: %s' % name)
        self.assertEqual(self.get_text('group_page_domain'), 'Domain: %s' % domain)
        self.assertEqual(self.get_text('group_page_description'), 'Description: %s' % description)
        self.assertTrue(self.Groups.delete_group(name))
        self.lg('%s ENDED' % self._testID)

    @unittest.skip('bug #782')
    def test06_groups_edit_group(self):
        """
        PRTL-006
        *Test case to make sure that editing groups is working as expected*

        **Test Scenario:**
        #. go to groups page.
        #. add new group.
        #. edit group info
        """
        self.lg('%s STARTED' % self._testID)
        name = str(uuid.uuid4()).replace('-', '')[0:10]
        self.assertTrue(self.Groups.create_new_group(name))
        self.assertTrue(self.Groups.edit_group(name))
        self.assertTrue(self.Groups.delete_group(name))
        self.lg('%s ENDED' % self._testID)

    def test07_groups_delete_group(self):
        """
        PRTL-007
        *Test case to make sure that deleting groups is working as expected*

        **Test Scenario:**
        #. go to groups page.
        #. add new group.
        #. delete the group
        """
        self.lg('%s STARTED' % self._testID)
        name =  str(uuid.uuid4()).replace('-', '')[0:10]
        self.assertTrue(self.Groups.create_new_group(name))
        self.assertTrue(self.Groups.delete_group(name))
        self.lg('%s ENDED' % self._testID)



    # def test05_groups_table_search(self):
    #     """
    #     PRTL-005
    #     *Test case to make sure that searching in groups table is working as expected*
    #
    #     **Test Scenario:**
    #     #. go to groups page.
    #     #. try general search box to search for values in all columns and verfiy it return the right value
    #     #. try the search box in every column and  verfiy it return the right value
    #     """
    #     self.lg('%s STARTED' % self._testID)
    #     self.lg('try general search box to search for values in all columns and verfiy it return the right value')
    #     self.assertTrue(self.Tables.check_search_box(self.data_table, self.table_info, self.search_box))
    #     self.lg('try the search box in every column and verfiy it return the right value')
    #     self.assertTrue(self.Tables.check_data_filters(self.data_table, self.table_info))
    #     self.lg('%s ENDED' % self._testID)
