import time
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
from datetime import datetime, timedelta,date



class grid():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.LeftNavigationMenu.Grid.grid_page()

    def is_at(self):
        for _ in range(10):
            if 'Grid Home' in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def get_VM_grid(self):
        self.framework.LeftNavigationMenu.Grid.vmachin_grid()
        for _ in range(10):
            if 'Virtual Machines' in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def open_grid_nodes(self):
        self.framework.click_link(self.framework.element_link('grid_node_link'))
        for _ in range(10):
            if 'Grid Nodes' in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def open_grid_failed_jobs(self):
        self.framework.click_link(self.framework.element_link('Failed_jobs_link'))
        for _ in range(10):
            if 'Grid Jobs' in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def open_grid_status_Overview(self):
        self.framework.click_link(self.framework.element_link('status_overview_link'))
        for _ in range(10):
            if 'Status Overview' in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def Running_VMs_in_table(self):
        self.framework.set_text_columns("VM_grid_table_element_search" ,'RUNNING', 2)
        self.framework.assertTrue(self.framework.wait_until_table_element_has_text("Vmachine_grid_table",0,1,'RUNNING'))
        vms_info = self.framework.Tables.get_table_info('Vmachine_grid_table_info')
        Running_VMs= int(vms_info[vms_info.index('f') + 2:vms_info.index('en') - 1].replace(',', ''))
        return Running_VMs

    def ECs_in_table_last_24Hr(self):
        date_day_ago = datetime.now() - timedelta(days=1)
        date_day_ago = "{:%m/%d/%Y %H:%M }".format(date_day_ago)
        self.framework.set_text("EC_table_date_start_search" ,date_day_ago)
        self.framework.assertTrue(self.framework.wait_until_element_located('EC_table_date_click_button'))
        self.framework.click("EC_table_date_click_button")
        self.framework.assertTrue(self.framework.wait_until_element_located('ec_entries_info'))
        ECs_info = self.framework.Tables.get_table_info('ec_entries_info')
        ECs= int(ECs_info[ECs_info.index('f') + 2:ECs_info.index('en') - 1].replace(',', ''))
        return ECs

    def get_error_condition_page(self):
        self.framework.LeftNavigationMenu.Grid.error_conditions()
        for _ in range(10):
            if 'Error Conditions' in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False
