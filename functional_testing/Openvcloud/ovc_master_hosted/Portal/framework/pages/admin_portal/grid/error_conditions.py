import time
from random import randint
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
import uuid

class errorConditions():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.lg('get grid.error_conditions page')
        self.framework.LeftNavigationMenu.Grid.error_conditions()
        self.framework.assertTrue(self.framework.check_element_is_exist("error_conditions_page"))


