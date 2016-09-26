from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.utils.utils import BaseTest
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.pages.admin_portal.cloudspaces import cloudspaces
import uuid

class virtualmachines(BaseTest):
    def __init__(self, *args, **kwargs):
        super(virtualmachines, self).__init__(*args, **kwargs)

    def create_virtual_machine(self, cloudspace='', machine_name='', image='', memory='', disk=''):
        cloudspace = cloudspace
        machine_name = machine_name or str(uuid.uuid4()).replace('-', '')[0:10]
        self.image = image or 'Ubuntu 14.04'
        self.memory = memory or '1024 MB'
        self.disk = disk or '50 GB'

        self.lg('open the cloudspace page')
        cloudspaces().open_cloudspace_page(cloudspace)

        self.lg('add virtual machine')
        self.click('add_virtual_machine')
        self.assertEqual(self.get_text('create_virtual_machine_on_cpu_node'), 'Create Machine On CPU Node')

        self.lg('enter the machine name')
        self.set_text('machine_name_admin', machine_name)

        self.lg('enter the machien description')
        self.set_text('machine_description_admin', str(uuid.uuid4()).replace('-', '')[0:10])

        self.lg('select the image')
        self.select('machine_images_list', self.image)

        self.lg('select the memory')
        self.select('machine_memory_list', self.memory)

        self.lg('select the disk')
        self.select('machine_disk_list', self.disk)

        self.lg('create machine confirm button')
        self.click('machine_confirm_button')

        self.set_text('virtual machine search', machine_name)
        self.wait_until_element_located_and_has_text(self.elements["virtual_machine_table_first_element"],
                                                     machine_name)

    def open_virtual_machine_page(self, cloudspace='', machine_name=''):
        cloudspace = cloudspace
        machine_name = machine_name

        self.lg('opne %s cloudspace' % cloudspace)
        cloudspaces().open_cloudspace_page(cloudspace)

        self.lg('open %s virtual machine' % machine_name)
        self.set_text('virtual machine search', machine_name)
        self.wait_until_element_located_and_has_text(self.elements["virtual_machine_table_first_element"],
                                                     machine_name)
        vm_id = self.get_text("virtual_machine_table_first_element_2")[3:]
        self.click('virtual_machine_table_first_element')
        self.element_in_url(vm_id)

    def delete_virtual_machine(self, cloudspace='', machine_name=''):
        cloudspace = cloudspace
        machine_name = machine_name

        self.lg('open %s virtual machine' % machine_name)
        self.open_virtual_machine_page(cloudspace, machine_name)

        self.lg('delete the machine')
        self.click('virtual_machine_action')
        self.click('virtual_machine_delete')
        self.set_text('virtual_machine_delete_reason', "Test")
        self.click("virtual_machine_delete_confirm")
        self.wait_until_element_located_and_has_text(self.elements["virtual_machine_page_status"],
                                                     "DESTROYED")
