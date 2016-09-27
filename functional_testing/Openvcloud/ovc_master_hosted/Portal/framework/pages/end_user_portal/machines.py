import uuid
from random import randint
import time


class machines():
    def __init__(self, framework):
        self.framework = framework

    def end_user_create_virtual_machine(self, image_name="ubuntu_14_04", machine_name=''):
        self.framework.RightNavigationMenu.Machines.home()

        self.framework.click("create_machine_button")

        machine_name = machine_name or str(uuid.uuid4()).replace('-', '')[0:10]
        machine_description = str(uuid.uuid4()).replace('-', '')[0:10]
        randome_package = randint(1, 6)
        if image_name != "windows_2012":
            random_disk_size = randint(1, 8)
        else:
            random_disk_size = randint(1, 6)
            self.framework.click("windows")

        self.framework.lg("Create a machine name: %s image:%s" % (machine_name, image_name))
        self.framework.set_text("machine_name", machine_name)
        self.framework.set_text("machine_description_", machine_description)
        self.framework.click(image_name)
        self.framework.click("package_%i" % randome_package)
        self.framework.click("disk_size_%i" % random_disk_size)

        self.framework.click("create_machine")
        for temp in range(30):
            if "console" in self.framework.get_url():
                break
            else:
                time.sleep(1)

        if self.framework.get_text("machine_status") == "RUNNING":
            self.framework.lg(' machine is created')
            return True
        else:
            self.framework.lg("FAIL : %s Machine isn't RUNNING" % machine_name)
            return False

    def end_user_get_machine_page(self, machine_name=''):
        machine_name = machine_name
        self.framework.click("machines_button")
        if self.framework.check_element_is_exist("end_user_machine_table"):
            machine_table = self.framework.driver.find_element_by_xpath(
                self.framework.elements["end_user_machine_table"])
            machine_table_rows = machine_table.find_elements_by_class_name("ng-scope")

            for row in machine_table_rows:
                items = row.find_elements_by_class_name("ng-binding")
                if machine_name == items[1].text:
                    self.framework.machine = items[1]
                    self.framework.machine_memory = items[3].text
                    self.framework.machine_cpu = items[4].text
                    self.framework.machine_storage = items[5].text
                    row.find_element_by_link_text(machine_name).click()
                    for _ in range(3):
                        if not self.framework.check_element_is_exist("end_user_machine_name"):
                            time.sleep(1)
                        else:
                            break
                    self.framework.assertIn(machine_name, self.framework.get_text("end_user_machine_name",
                                                                                  "can't find %s machine in the table" % machine_name))
                    break
            else:
                self.framework.fail("can't find %s machine in the table" % machine_name)

    def end_user_get_machine_info(self, machine_name=''):
        self.framework.assertIn(machine_name, self.framework.get_text("end_user_machine_name",
                                                                      "can't find %s machine in the table" % machine_name))

        if self.framework.check_element_is_exist("machine_description"):
            self.framework.machine_description = self.framework.get_text("machine_description")
        else:
            self.framework.machine_description = ''
        self.framework.machine_status = self.framework.get_text("machine_status")
        self.framework.machine_ipaddress = self.framework.get_text("machine_ipaddress")
        self.framework.machine_osimage = self.framework.get_text("machine_osimage")
        self.framework.machine_credentials = self.framework.get_text("machine_credentials")

    def end_user_wait_machine(self, status):
        for _ in range(30):
            if self.framework.get_text("machine_status") == status:
                break
            time.sleep(1)

    def end_user_verify_machine_elements(self, status):
        if self.framework.machine_description:
            self.framework.assertEqual(self.framework.machine_description, self.framework.get_text("machine_description"))
        self.framework.assertEqual(status, self.framework.get_text("machine_status"))
        self.framework.assertEqual(self.framework.machine_ipaddress, self.framework.get_text("machine_ipaddress"))
        self.framework.assertEqual(self.framework.machine_osimage, self.framework.get_text("machine_osimage"))
        self.framework.assertEqual(self.framework.machine_credentials, self.framework.get_text("machine_credentials"))
        self.framework.assertEqual(self.framework.machine_cpu, self.framework.get_text("machine_cpu"))
        self.framework.assertEqual(self.framework.machine_memory, self.framework.get_text("machine_memory"))
        self.framework.assertEqual(self.framework.machine_storage, self.framework.get_text("machine_storage"))


    def end_user_verify_machine_console(self, status):
        if status == 'RUNNING':
            self.framework.assertEqual(self.framework.get_text("console_message_running"),
                             "Click the console screen or use the control buttons below to "
                             "get access to the screen. In case of a black screen, hit any key "
                             "to disable the screen saving mode of your virtual machine.")
            self.framework.assertEqual(self.framework.get_text("console_ipaddress"), self.framework.machine_ipaddress)
            self.framework.assertTrue(self.framework.element_is_displayed("capture_button"))
            self.framework.assertTrue(self.framework.element_is_displayed("send_ctrl/alt/del_button"))
        else:
            self.framework.assertEqual(self.framework.get_text("console_message_halted"),
                             "A machine must be started to access the console!")
            self.framework.assertFalse(self.framework.element_is_displayed("capture_button"))
            self.framework.assertFalse(self.framework.element_is_displayed("send_ctrl/alt/del_button"))


    def end_user_start_machine(self, machine):
        self.framework.click_link(machine)
        if self.framework.get_text("machine_status") != "RUNNING":
            self.framework.click("machine_start")
            time.sleep(30)
            self.framework.click("actions_tab")
            self.framework.click("refresh_button")


    def end_user_delete_virtual_machine(self, virtual_machine):
        self.framework.lg('Open end user home page')
        self.framework.get_page(self.framework.environment_url)

        if self.framework.check_element_is_exist("machines_button"):
            self.framework.lg(' Start creation of machine')
            self.framework.click("machines_button")

            if self.framework.check_element_is_exist("end_user_machine_table"):
                self.framework.lg('Open the machine page to destroy it')
                machine_table = self.framework.driver.find_element_by_xpath(self.framework.elements["end_user_machine_table"])
                machine_table_rows = machine_table.find_elements_by_class_name("ng-scope")

                for counter in range(len(machine_table_rows)):
                    machine_name_xpath = self.framework.elements["end_user_machine_name_table"] % (counter+1)
                    machine_name = self.framework.driver.find_element_by_xpath(machine_name_xpath)
                    if virtual_machine == machine_name.text:
                        machine_name.click()
                        break
                else:
                    self.framework.lg("can't find %s machine in the table" % virtual_machine)
                    return False

                self.framework.lg("Destroy the machine")
                self.framework.click("destroy_machine")
                self.framework.click("destroy_machine_confirm")
                time.sleep(10)
                if self.framework.get_text("machine_list") == "Machines":
                    return True
                else:
                    self.framework.lg("FAIL : Can't delete %s machine" % virtual_machine)
                    return False
            else:
                self.framework.lg("There is no machines")
                return False
        else:
            self.framework.lg("FAIL : Machine button isn't exist for this user")
            return False

    def end_user_choose_account(self, account=''):
        account = account or self.framework.account
        self.framework.lg('Open end user home page')
        self.framework.get_page(self.framework.environment_url)
        if self.framework.check_element_is_exist("end_user_selected_account"):
            print(account,self.framework.get_text("end_user_selected_account"))
            if account not in self.framework.get_text("end_user_selected_account"):
                accounts_xpath = self.framework.elements["end_user_accounts_list"]
                for temp in range(100):
                    try:
                        account_item = self.framework.driver.find_element_by_xpath(accounts_xpath % temp)
                    except:
                        self.framework.lg("Can't choose %s account from the end user" % account)
                        return False
                    else:
                        if account in account_item.text:
                            account_item.click()
                            cloud_space_xpath = self.framework.elements["end_user_cloud_space"] % account
                            self.framework.driver.find_element_by_xpath(cloud_space_xpath).click()
                            return True
            else:
                return True
        else:
            self.framework.lg("This user doesn't has any account")
            return False