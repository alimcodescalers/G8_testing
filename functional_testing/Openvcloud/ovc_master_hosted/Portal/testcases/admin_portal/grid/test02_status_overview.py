from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework

class StatusTests(Framework):
    def setUp(self):
        super(StatusTests, self).setUp()
        self.Login.Login()
        self.StatusOverview.get_it()

    def test01_status_overview_page(self):
        """ PRTL-029
        *Test case to make sure that the process status and health check are working as expected*

        **Test Scenario:**
        #. go to status overview page
        #. verify machines table status/color
        #. press on "Run Healthcheck"
        #. verify expected behavior
        """
        NodeStatus = self.StatusOverview.get_node_status()
        for status in NodeStatus:
            self.assertEqual(status, "RUNNING", "Error: %s " % status)





