import time
import unittest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework

class GridTests(Framework):
    def setUp(self):
        super(GridTests, self).setUp()
        self.Login.Login()

    def test001_grid_page(self):
        """
        Prtl-000
       *Test case for check grid page in the admin portal*

        **Test Scenario:**

        #. get grid page
        #. check that "Grid Portal" in head of page side of administration
        #. check that all elements on grid page exist(headers,Events counter,Running VMs counter,Grid Nodes,Events Dashboard,last check,alert)
        #. check that grid containers have right values
        #. check that you can get grid nodes page from grid page
        #. check that you can get failed jobs page from grid page
        #. check that you can get status overview from grid page
        #. check that all nodes running well from alert element in grid page

        """
        self.lg('%s STARTED' % self._testID)
        self.lg('get grid page ')
        self.Grid.get_it()
        self.assertTrue(self.Grid.is_at())
        self.lg('check that "Grid portal" in head of page side of administration ')

        self.assertEqual(self.get_text("grid_portal_title"),"Grid Portal")
        self.lg('check that all headers on grid page exist')
        self.assertEqual(self.get_text("grid_portal_header1"),"Grid Portal")
        self.assertEqual(self.get_text("grid_portal_header2"),"Home")
        self.lg('check that all elements on grid page exist(Events counter,Running VMs counter,Grid Nodes,Events Dashboard,last check,alert')
        self.assertEqual(self.get_text("grid_counter1"),"Events in the last 24 hours")
        self.assertEqual(self.get_text("grid_counter2"),"Running Virtual Machines")
        self.assertEqual(self.get_text("grid_nodes"),"Grid Nodes")
        self.assertEqual(self.get_text("grid_events_dashboard"),"Events Dashboard")
        self.assertTrue("Grid was last checked at" in  self.get_text("grid_last_check"))
        self.assertEqual(self.get_text("grid_details"),"For more details, check status overview.")
        self.lg("check that you can get grid nodes page from grid page")
        self.assertTrue(self.Grid.open_grid_nodes())
        self.lg("check that you can get failed jobs page from grid page")
        self.Grid.get_it()
        self.assertTrue(self.Grid.is_at())
        self.assertTrue(self.Grid.open_grid_failed_jobs())
        self.lg("check that you can get status overview page from grid page")
        self.Grid.get_it()
        self.assertTrue(self.Grid.is_at())
        self.assertTrue(self.Grid.open_grid_status_Overview())
        self.lg("check that all nodes running well from alert element in grid page")
        #skip " Issue in env "
        #self.assertEqual(self.get_text("grid_alert","Every thing is Ok")

    #@unittest.skip("https://github.com/0-complexity/openvcloud/issues/759")
    def test002_Running_VM_gauge(self):
        """
        Prtl-000

       *Test case for checking running VMs gauge in the grid page*

        **Test Scenario:**

        #. get grid page
        #. get value of  Running VM container
        #. get running VMs from vm table in vm page in cloudbroker and check that it same of value in running container
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('get grid page ')
        self.assertTrue(self.Grid.get_VM_grid())
        cloudbroker_running_VMs=self.Grid.Running_VMs_in_table()

        self.Grid.get_it()
        result = self.Grid.is_at()
        self.assertTrue(result)

        grid_running_VMs=int(self.get_text("grid_running_VMS"))
        self.assertEqual(grid_running_VMs,cloudbroker_running_VMs)
        self.lg('%s ENDED' % self._testID)

    @unittest.skip("https://github.com/0-complexity/openvcloud/issues/759")
    def test003_last_events_24hr_gauge(self):
        """
        Prtl-000
       *Test case for checking last events 24hr gauge in the grid page*

        **Test Scenario:**

        #. get grid page
        #. get value of  last Events in  last 24 hour
        #. get ErrorConditions from Ec table in Ec page in grid and check that it same of value in Event gauge
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('get grid page ')
        self.assertTrue(self.Grid.get_error_condition_page())
        ECs_last_24Hr=self.Grid.ECs_in_table_last_24Hr()
        self.Grid.get_it()
        result = self.Grid.is_at()
        self.assertTrue(result)
        grid_last_events_24hr=self.get_text("Events_in_the_last24hr")
        self.assertEqual(grid_last_events_24hr,ECs_last_24Hr)
        self.lg('%s ENDED' % self._testID)
