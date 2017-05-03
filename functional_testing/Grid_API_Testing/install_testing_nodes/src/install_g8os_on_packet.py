from selenium import webdriver
from pyvirtualdisplay import Display
from install_testing_nodes.src.Basic import Basic
import g8core
from selenium.webdriver.support.ui import Select
from termcolor import colored
import time


class InstallG8OSOnPacket(Basic):
    def login(self):
        self.logging.info(' [*] Login .. ')
        print(colored(' [*] Login .. ', 'white'))
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        self.driver.get('https://app.packet.net/#/login')
        self.driver.find_element_by_id('login').send_keys(self.values['packet_username'])
        passwd = self.driver.find_element_by_id('password')
        passwd.send_keys(self.values['packet_password'])
        passwd.submit()
        self.logging.info(' [*] Logged in ')
        print(colored(' [*] Logged in', 'green'))

    def ctreate_new_machine(self, image, machine_name, type='Type 0'):
        self.logging.info(' [*] create new machine  .. ')
        print(colored(' [*] create new machine .. ', 'white'))
        image = self.add_zerotire_nw_to_image(image=image)
        self.driver.find_element_by_id('new-device').click()
        self.driver.find_element_by_xpath(
            '/html/body/app-view/content-offset/ui-view/offset/white-frame/form/offset[3]/button').click()
        self.driver.find_element_by_name('hostname').send_keys(machine_name)

        select_plan = Select(self.driver.find_element_by_name('rowType'))
        select_plan.select_by_visible_text(type)

        select_os = Select(self.driver.find_element_by_name('os'))
        select_os.select_by_value('custom_ipxe')
        self.driver.find_element_by_name('ipxe_script_url').send_keys(image)

        select_location = Select(self.driver.find_element_by_xpath(
            '/html/body/app-view/content-offset/ui-view/app-content/div/div[3]/offset/form-offset/form/input-group[1]/offset/offset/grid-table/table-row[2]/table-cell[4]/input-block/sw-drop-down/select'))
        select_location.select_by_visible_text('Sunnyvale, CA')

        self.driver.find_element_by_xpath(
            '/html/body/app-view/content-offset/ui-view/app-content/div/div[3]/offset/form-offset/form/input-group[2]/frame-offset/offset[2]/button').click()
        for _ in range(30):
            try:
                machine_link = self.driver.find_element_by_link_text(machine_name)
            except:
                time.sleep(3)
            else:
                machine_link.click()

        self.logging.info(' [*] created machine : %s  .. ' % machine_name)
        print(colored(' [*] G8os machine : %s  .. \n' % machine_name, 'green'))
        self.driver.get('https://app.packet.net/portal')

    def get_packt_machine_ip(self, machine_name):
        self.logging.info(' [*] get machine ip .. ')
        print(colored(' [*] get machine ip .. ', 'white'))
        machine_list = self.driver.find_element_by_class_name(
            '/html/body/app-view/content-offset/ui-view/app-content/hybrid-list/type-list/frame-offset/div[1]/white-frame/div/div[2]/grid-list/grid-body').text.split(
            '\n')
        for line in machine_list:
            if line == machine_name:
                ip = machine_name[machine_name.index(line) + 2]
                self.logging.info(' [*] Machine ip : %s ' % ip)
                print(colored(' [*] Machine ip : %s ' % ip, 'green'))
                return ip
            else:
                return None

    def get_packet_machine_mac(self, ip):
        self.logging.info(' [*] get machine mac .. ')
        print(colored(' [*] get machine mac .. ', 'white'))
        # client = telnetlib.Telnet(IP)
        # client.write((" ip addr | grep link/ether | awk '{print $2}'\n").encode('ascii'))
        # data = str(client.read_very_eager()).split()
        # return data[10].split('\\r\\n')[1]
        client = g8core.Client(ip)
        nic_list = client.info.nic()
        for nic in nic_list:
            if ip in nic['addrs'][0]['addr']:
                mac = nic['hardwareaddr']
                self.logging.info(' [*] Machine mac : %s ' % mac)
                print(colored(' [*] Machine mac : %s ' % mac, 'green'))
                return mac

    def add_zerotire_nw_to_image(self, image):
        return image % self.values['zerotire_nw']

    def driver_quit(self):
        self.driver.quit()
        self.display.stop()
