from ...utils.utils import BaseTest
from ..page_elements_xpath import menu_page

class AdminMenu(BaseTest):
    def __init__(self, *args, **kwargs):
        super(AdminMenu, self).__init__(*args, **kwargs)
        self.elements.update(menu_page.elements)

    def setUp(self):
        super(AdminMenu, self).setUp()
        self.login()
        self.get_page(self.base_page)

    def test01_admin_menu_items(self):
        """ PRTL-000
        *Test case to make sure that the admin portal menu work as expected*

        **Test Scenario:**
        #. click on the admin menu
        #. verify all items
        #. for every main item verify its items and behavior
        #. for all items verify redirect page
        """

        compo_menu = ["At Your Service", "Cloud Broker", "Statistics", "Grid", "Storage", "System", "End User"]
        ays_menu = ['Services', 'Templates']
        cloud_broker_menu = ['Accounts', 'Cloud Spaces', 'Locations', 'Stacks', 'Images', 'Public Networks',
                             'Private Networks', 'Users', 'Groups', 'Virtual Machines', 'Software Versions']
        grid_menu = ['Audits', 'Error Conditions', 'Jobs', 'Job Queues', 'JumpScript', 'Logs', 'Grid Nodes',
                     'Status Overview', 'Virtual Machines']

        storage_menu = self.get_storage_list()

        system_menu = ['Spaces', 'System Config', 'System Macros', 'Users', 'Groups', 'Code', 'API', 'Portal Logs',
                       'Access Overview']

        self.lg("check left menu")
        self.compare_original_list_with_exist_list("ays_arrow", "left_menu", compo_menu)

        self.lg("check ays menu")
        self.compare_original_list_with_exist_list("ays_text", "ays_menu",ays_menu)

        self.lg("check cloudbroker menu")
        self.compare_original_list_with_exist_list("cloudbroker_arrow", "cloudbroker_menu", cloud_broker_menu)

        self.lg("check grid menu")
        self.compare_original_list_with_exist_list("grid_arrow", "grid_menu", grid_menu)

        self.lg("check storage menu")
        self.compare_original_list_with_exist_list("storage_arrow", "storage_menu", storage_menu)

        self.lg("check system menu")
        self.compare_original_list_with_exist_list("system_arrow","system_menu",system_menu)

        self.lg("check ays items redirect page")
        self.check_redirect_page("ays_text", "AYS")
        self.check_redirect_page("ays_sub_service", "Services")
        self.check_redirect_page("ays_sub_templates", "Templates")

        self.lg("check cloudbroker items redirect page")
        self.check_redirect_page("cloudbroker_text", "cbgrid")
        self.check_redirect_page("cloudbroker_sub_accounts", "accounts")
        self.check_redirect_page("cloudbroker_sub_cs", "Cloud Spaces")
        self.check_redirect_page("cloudbroker_sub_locations", "locations")
        self.check_redirect_page("cloudbroker_sub_stacks", "Stacks")
        self.check_redirect_page("cloudbroker_sub_images", "images")
        self.check_redirect_page("cloudbroker_sub_public_nw", "public networks")
        self.check_redirect_page("cloudbroker_sub_private_nw", "private networks")
        self.check_redirect_page("cloudbroker_sub_users", "users")
        self.check_redirect_page("cloudbroker_sub_groups", "groups")
        self.check_redirect_page("cloudbroker_sub_vm", "Virtual Machines")
        self.check_redirect_page("cloudbroker_sub_sv", "Version")

        self.lg("check statistics items redirect page")
        self.check_redirect_page("statistics", "home/external")
        self.get_page(self.base_page)

        self.lg("check grid items redirect page")
        self.check_redirect_page("grid_text", "grid")
        self.check_redirect_page("grid_sub_audits", "Audits")
        self.check_redirect_page("grid_sub_ec", "Error Conditions")
        self.check_redirect_page("grid_sub_jobs", "Jobs")
        self.check_redirect_page("grid_sub_jq", "job queues")
        self.check_redirect_page("grid_sub_jumpsacale", "Jumpscripts")
        self.check_redirect_page("grid_sub_logs", "Logs")
        self.check_redirect_page("grid_sub_gn", "Grid Nodes")
        self.check_redirect_page("grid_sub_so", "Status Overview")
        self.check_redirect_page("grid_sub_vm", "Virtual Machines")

        self.lg("check system items redirect page")
        self.check_redirect_page("system_text", "system")
        self.check_redirect_page("system_sub_spaces", "spaces")
        self.check_redirect_page("system_sub_sc", "Systemconfig")
        self.check_redirect_page("system_sub_sm", "systemmacros")
        self.check_redirect_page("system_sub_users", "userlist")
        self.check_redirect_page("system_sub_groups", "groups")
        self.check_redirect_page("system_sub_code", "code")
        self.check_redirect_page("system_sub_api", "actorsdocs")
        self.check_redirect_page("system_sub_pl", "PortalLogs")
        self.check_redirect_page("system_sub_ao", "overviewaccess")

        self.lg("check end user page")
        self.check_side_list()
        self.driver.ignore_synchronization = False
        self.click("end_user")
        self.driver.get(self.get_url())
        self.assertEqual(self.get_text("end_user_home"),"Home")

    def check_redirect_page(self, clickable_item, check_value):
        self.check_side_list()
        self.click(clickable_item)
        self.assertTrue(self.element_in_url(check_value))
