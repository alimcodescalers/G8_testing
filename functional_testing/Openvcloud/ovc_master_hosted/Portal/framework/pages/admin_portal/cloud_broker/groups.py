import time
import uuid
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu


class groups():
    def __init__(self, framework):
        self.framework = framework
        self.LeftNavigationMenu = leftNavigationMenu(framework)

    def get_it(self):
        self.LeftNavigationMenu.CloudBroker.Groups()

    def is_at(self):
        for _ in range(10):
            if 'Groups' in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def create_new_group(self, name='', domain='', description=''):
        name = name or str(uuid.uuid4()).replace('-', '')[0:10]
        domain = domain or str(uuid.uuid4()).replace('-', '')[0:10]
        description = description or str(uuid.uuid4()).replace('-', '')[0:10]

        self.LeftNavigationMenu.CloudBroker.Groups()
        self.framework.click('groups_action')
        self.framework.click('groups_action_add_group')
        self.framework.set_text('groups_action_name', name)
        self.framework.set_text('groups_action_domain', domain)
        self.framework.set_text('groups_action_description', description)
        self.framework.click('groups_acrion_add_group_confirm')
        self.framework.set_text("table_groups_search_box", name)

        if self.framework.wait_until_element_located_and_has_text("groups_table_first_element_name", name):
            self.framework.CLEANUP["groups"].append(name)
            return True
        else:
            self.framework.lg("Cannot create %s group" % name)
            return False


    def open_group_page(self, name):
        self.LeftNavigationMenu.CloudBroker.Groups()
        self.framework.set_text("table_groups_search_box", name)
        if self.framework.wait_until_element_located_and_has_text('groups_table_first_element_name', name):
            self.framework.click('groups_table_first_element_name')
            return self.framework.element_in_url(name)
        else:
            self.framework.lg("Cannot open %s group page" % name)
            return False

    def delete_group(self, name):
        if self.open_group_page(name):
            self.framework.click('group_action')
            self.framework.click('group_action_delete_group')
            self.framework.click('group_acrion_delete_group_confirm')
            self.framework.CLEANUP["groups"].remove(name)
            return True
        else:
            self.framework.lg("There is no %s group" % name)
            return False


    def edit_group(self, name):
        if self.open_group_page(name):
            items = [['group_page_name','group_acrion_edit_domain'], ['group_page_domain','group_acrion_edit_description']]
            for item in items:
                self.framework.click('group_action')
                self.framework.click('group_action_edit_group')
                new_value = str(uuid.uuid4()).replace('-', '')[0:10]
                self.framework.set_text(item[1], new_value)
                self.framework.click('groups_acrion_edit_group_confirm')
                for _ in range(5):
                    if new_value in self.get_text(item[0]):
                        return True
                    else:
                        time.sleep(1)
                else:
                    return False
