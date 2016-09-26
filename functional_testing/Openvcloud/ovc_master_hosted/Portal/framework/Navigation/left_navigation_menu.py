from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.utils.utils import BaseTest

class Base(BaseTest):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

    def check_side_list(self):
        for temp in range(3):
            try:
                if self.driver.find_element_by_xpath(self.elements["left_menu"]).location["x"] < 0:
                    self.click("left_menu_button")
                break
            except:
                self.lg("can't locate the left menu")

    def open_base_page(self, menu_item='', sub_menu_item=''):
        self.get_page(self.base_page)
        self.check_side_list()
        self.click(menu_item)
        self.check_side_list()
        self.click(sub_menu_item)

class AtYourService(Base):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
    pass

class CloudBroker(Base):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

    def Accounts(self):
        self.open_base_page("cloud_broker", "cloudbroker_sub_accounts")

    def CloudSpaces(self):
        self.open_base_page("cloud_broker", "cloudbroker_sub_cs")

    def Locations(self):
        self.open_base_page("cloud_broker", "cloudbroker_sub_locations")

    def Stacks(self):
        self.open_base_page("cloud_broker","cloudbroker_sub_stacks")

    def Images(self):
        self.open_base_page("cloud_broker", "cloudbroker_sub_images")

    def PublicNetworks(self):
        self.open_base_page("cloud_broker", "cloudbroker_sub_public_nw")

    def Users(self):
        self.open_base_page("cloud_broker", "cloudbroker_sub_users")

    def Groups(self):
        self.open_base_page("cloud_broker","cloudbroker_sub_groups")

    def VirtualMachines(self):
        self.open_base_page("cloud_broker","cloudbroker_sub_vm")

    def SoftwareVersions(self):
        self.open_base_page("cloud_broker","cloudbroker_sub_sv")

class Statics(Base):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
    pass

class Grid(Base):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
    pass

class Storage(Base):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
    pass

class Systems(Base):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
    pass

class EndUser(Base):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
    pass

class leftNavigationMenu(Base):
    def __init__(self, *args, **kwargs):
        super(leftNavigationMenu, self).__init__(*args, **kwargs)

        self.CloudBroker = CloudBroker()
        self.AtYourService = AtYourService()
        self.Statics = Statics()
        self.Grid = Grid()
        self.Storage = Storage()
        self.Systems = Systems()
        self.EndUser = EndUser()

    def compare_original_list_with_exist_list(self, menu_click, menu_element, original_list):
        self.check_side_list()
        if menu_click != "":
            self.click(menu_click)
        exist_menu = self.get_list_items_text(menu_element)
        for item in original_list:
            if not item in exist_menu:
                self.fail("This %s list item isn't exist in %s" % (item, exist_menu))

    def check_redirect_page(self, clickable_item, check_value):
        self.check_side_list()
        self.click(clickable_item)
        self.assertTrue(self.element_in_url(check_value))




