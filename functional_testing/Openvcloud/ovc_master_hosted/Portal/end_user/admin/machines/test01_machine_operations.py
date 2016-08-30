from .....utils.utils import BaseTest
from ...page_elements_xpath import machines_page
import time
import uuid

class Write(BaseTest):

    def __init__(self, *args, **kwargs):
        super(Write, self).__init__(*args, **kwargs)
        self.elements.update(machines_page.elements)

    def setUp(self):
        super(Write, self).setUp()
        self.login()
        self.click("machines_button")
        self.machine = self.element_link("first_machine")
        self.machine_name = self.get_text("first_machine_name")
        self.machine_memory = self.get_text("first_machine_memory")
        self.machine_cpu = self.get_text("first_machine_cpu")
        self.machine_storage = self.get_text("first_machine_storage")
        if self.get_text("first_machine_status") != "RUNNING":
            self.start_machine(self.machine)
        self.click_link(self.machine)
        self.machine_description = self.get_text("machine_description")
        self.machine_status = self.get_text("machine_status")
        self.machine_ipaddress = self.get_text("machine_ipaddress")
        self.machine_osimage = self.get_text("machine_osimage")
        self.machine_credentials = self.get_text("machine_credentials")

    def start_machine(self, machine):
        self.click_link(machine)
        if self.get_text("machine_status") != "RUNNING":
            self.click("machine_start")
            time.sleep(30)
            self.click("actions_tab")
            self.click("refresh_button")

    def wait_machine(self, status):
        for _ in range(30):
            if self.get_text("machine_status") == status:
                break
            time.sleep(1)

    def verify_machine_elements(self, status):
        self.assertEqual(self.machine_description, self.get_text("machine_description"))
        self.assertEqual(status, self.get_text("machine_status"))
        self.assertEqual(self.machine_ipaddress, self.get_text("machine_ipaddress"))
        self.assertEqual(self.machine_osimage, self.get_text("machine_osimage"))
        self.assertEqual(self.machine_credentials, self.get_text("machine_credentials"))
        self.assertEqual(self.machine_cpu, self.get_text("machine_cpu"))
        self.assertEqual(self.machine_memory, self.get_text("machine_memory"))
        self.assertEqual(self.machine_storage, self.get_text("machine_storage"))

    def verify_machine_console(self, status):
        if status == 'RUNNING':
            self.assertEqual(self.get_text("console_message_running"),
                             "Click the console screen or use the control buttons below to "
                             "get access to the screen. In case of a black screen, hit any key "
                             "to disable the screen saving mode of your virtual machine.")
            self.assertEqual(self.get_text("console_ipaddress"), self.machine_ipaddress)
            self.assertTrue(self.element_is_displayed("capture_button"))
            self.assertTrue(self.element_is_displayed("send_ctrl/alt/del_button"))
        else:
            self.assertEqual(self.get_text("console_message_halted"),
                             "A machine must be started to access the console!")
            self.assertFalse(self.element_is_displayed("capture_button"))
            self.assertFalse(self.element_is_displayed("send_ctrl/alt/del_button"))

    def test01_machine_stop_start_reboot_reset_pause_resume(self):
        """ PRTL-007
        *Test case for start/stop/reboot/reset/pause/resume machine.*

        **Test Scenario:**

        #. select running machine, should succeed
        #. stop machine, should succeed
        #. start machine, should succeed
        #. reboot machine, should succeed
        #. reset machine, should succeed
        #. reset machine using ctrl/alt/del button, should succeed
        #. pause machine, should succeed
        #. resume machine, should succeed
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('select running machine, should succeed')
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")

        self.lg('stop machine, should succeed')
        self.click("machine_stop")
        time.sleep(30)
        self.click("console_tab")
        self.verify_machine_console("HALTED")
        self.click("actions_tab")
        self.wait_machine("HALTED")
        self.verify_machine_elements("HALTED")
        self.click("refresh_button")
        self.wait_machine("HALTED")
        self.verify_machine_elements("HALTED")

        self.lg('start machine, should succeed')
        self.click("machine_start")
        time.sleep(30)
        self.verify_machine_console("RUNNING")
        self.click("actions_tab")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")
        self.click("refresh_button")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")

        self.lg('reboot machine, should succeed')
        self.click("machine_reboot")
        time.sleep(30)
        self.verify_machine_console("RUNNING")
        self.click("actions_tab")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")
        self.click("refresh_button")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")

        self.lg('reset machine, should succeed')
        self.click("machine_reset")
        time.sleep(30)
        self.verify_machine_console("RUNNING")
        self.click("actions_tab")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")
        self.click("refresh_button")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")

        self.lg('reset machine using ctrl/alt/del button, should succeed')
        self.click("console_tab")
        self.verify_machine_console("RUNNING")
        self.click("send_ctrl/alt/del_button")
        time.sleep(30)
        self.verify_machine_console("RUNNING")
        self.click("actions_tab")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")
        self.click("refresh_button")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")

        self.lg('pause machine, should succeed')
        self.click("machine_pause")
        time.sleep(10)
        self.click("console_tab")
        self.verify_machine_console("PAUSED")
        self.click("actions_tab")
        self.wait_machine("PAUSED")
        self.verify_machine_elements("PAUSED")
        self.click("refresh_button")
        self.wait_machine("PAUSED")
        self.verify_machine_elements("PAUSED")

        self.lg('resume machine, should succeed')
        self.click("machine_resume")
        time.sleep(10)
        self.click("console_tab")
        self.verify_machine_console("RUNNING")
        self.click("actions_tab")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")
        self.click("refresh_button")
        self.wait_machine("RUNNING")
        self.verify_machine_elements("RUNNING")

        self.lg('%s ENDED' % self._testID)

    def test02_machine_create_rollback_delete_snapshot(self):
        """
        *Test case for create snapshot machine.*

        **Test Scenario:**

        #. create new machine, should succeed
        #. create snapshot for a machine, should succeed
        #. rollback snapshot for a machine, should succeed
        #. delete snapshot for a machine, should succeed
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('select running machine, should succeed')
        self.wait_machine("RUNNING")

        self.lg('create snapshot for a machine, should succeed')
        snapshot_name = str(uuid.uuid4())
        self.click("machine_take_snapshot")
        self.set_text("snapshot_name_textbox", snapshot_name)
        self.click("snapshot_ok_button")
        time.sleep(5)
        self.click("snapshot_tab")
        time.sleep(2)
        self.assertEqual(snapshot_name, self.get_text("first_snapshot_name"))

        self.lg('rollback snapshot for a machine, should succeed')
        self.click("actions_tab")
        self.lg('stop machine, should succeed')
        self.click("machine_stop")
        time.sleep(30)
        self.click("snapshot_tab")
        self.click("first_snapshot_rollback")
        time.sleep(2)
        self.assertEqual(self.get_text("snapshot_confirm_message"),
                         "Snapshots newer then current snapshot will be removed.")
        self.click("snapshot_confirm_ok")
        time.sleep(5)
        self.click("first_snapshot_delete")
        time.sleep(2)
        self.assertEqual(self.get_text("snapshot_delete_message"),
                         "Are you sure you want to delete snapshot?")
        self.click("snapshot_delete_ok")
        time.sleep(2)

        self.lg('%s ENDED' % self._testID)
        
