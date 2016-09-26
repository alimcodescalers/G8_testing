from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.login import login
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.users import users
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.accounts import accounts
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.utils.utils import BaseTest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.cloudspaces import cloudspaces
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.virtualmachines import virtualmachines
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import leftNavigationMenu

class Framework(BaseTest):
    def __init__(self, *args, **kwargs):
        super(Framework, self).__init__(*args, **kwargs)

        #Pages.AdminPortal
        self.Login = login()
        self.Users = users()
        self.Accounts = accounts()
        self.CloudSpaces = cloudspaces()
        self.VirtualMachines = virtualmachines()

        #NAvigation
        self.LeftNavigationMenu = leftNavigationMenu()
