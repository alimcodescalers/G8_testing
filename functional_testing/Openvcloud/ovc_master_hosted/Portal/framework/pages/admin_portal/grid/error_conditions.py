from random import randint
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
from datetime import datetime, timedelta,date
import time
class errorConditions():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.lg('get grid.error_conditions page')
        self.framework.LeftNavigationMenu.Grid.error_conditions()
        self.framework.assertTrue(self.framework.check_element_is_exist("error_conditions_page"))

    def check_EC_table_heads(self,table):
        table = self.framework.Tables.generate_table_elements(table)
        heads=self.framework.get_table_head_elements(table['data'])
        EC_heads=['Last Occurrence','Error Message','App name','Occurrences','Node ID','Grid ID']
        elements=[]
        for head in heads:
            elements.append(head.text)
        if elements != EC_heads:
            self.framework.lg("error condition table heads %s not true "%elements)
            return False
        return True

    def open_EC_page(self, EC='',table=''):
        self.framework.LeftNavigationMenu.Grid.error_conditions()

        self.framework.set_text("table_ECs_search_box", EC)

        if self.framework.wait_until_element_located_and_has_text("EC_table_first_element_2", EC):
            EC_herf = self.framework.element_link("EC_table_first_element_1")
            self.table_elements_aftersearch=self.framework.get_table_row(table,0)
            EC_id = EC_herf[EC_herf.find('?id=')+len('?id='):]
            self.framework.click_link(EC_herf)
            return self.framework.element_in_url(EC_id )

        else:
            self.framework.lg('can\'t find image %s' % image)
            return False

    def random_element(self,random_elemn_row):
        EC_element=random_elemn_row[1]
        skip_characters=['.',':','\'','&']
        if EC_element[0]== '<':
            EC_element=EC_element[(EC_element.index('>')+2) :]
        for i in skip_characters:
            EC_element=EC_element[ :(EC_element.find(i))]
        return EC_element

    def get_headers(self,header_element):
        head =self.framework.find_element(header_element)
        header_elements=head.find_elements_by_tag_name('li')
        header_list=[]
        for header in range(len(header_elements)):
            header_list.append(str(header_elements[header].text))
        return header_list

    def Error_Condition_action(self):
        self.framework.click('Error_Condition_action')
        self.framework.click('Error_Condition_delete_action')
        self.framework.assertEqual(self.framework.get_text("EC_action_edit_page"), 'Confirm Action Delete')
        self.framework.click('close_Delete_message')

    def get_job_page(self,application_name):
        table=self.framework.find_element('EC_detail_table')
        tbody=table.find_elements_by_tag_name('tbody')
        rows=tbody[0].find_elements_by_tag_name('tr')
        row=rows[2].find_elements_by_tag_name('td')
        job_link=row[1]
        if ('worker' or 'jsagent')in application_name :
            job_Id = job_link.text
            if job_Id == 'N/A':
                return False
            self.framework.click_link(self.framework.element_link('job_Ec_link'))
            time.sleep(1)
            return self.framework.element_in_url(job_Id)

        return True
    def Error_Condition_details_table(self):
        self.table=[]
        table_rows= self.framework.get_table_rows('EC_detail_table')
        if len(table_rows)!=15:
            return False
        for row in table_rows:
            cells = row.find_elements_by_tag_name('td')
            self.table.append([x.text for x in cells])
        return self.table

    def check_EC_elements(self):
        self.tableData=self.Error_Condition_details_table()
        self.application_name=self.tableData[0][1]
        self.accurrence=self.tableData[7][1]
        self.cpu_node=self.tableData[12][1]
        self.grid_Id=self.tableData[13][1]
        self.framework.assertEqual(str(self.application_name),self.table_elements_aftersearch[2])
        self.framework.assertEqual(str(self.accurrence),self.table_elements_aftersearch[3])
        self.framework.assertTrue(self.table_elements_aftersearch[4] in str(self.cpu_node))
        self.framework.assertTrue(self.table_elements_aftersearch[5] in str(self.grid_Id) )

    def check_exist_of_EC_elements(self):
        self.tableData=self.Error_Condition_details_table()
        if self.tableData == False:
            self.framework.lg('can\'t get table details of job page')
            return False
        EC_elements=['Application Name','Category','Job','Type','Level','Creation Time','Last Time','Occurrences','Error Message Pub','Function Name','Function Line Number','Function File Name','Node','Grid','Tags']
        for i,element in enumerate(EC_elements):
            if str(self.tableData[i][0])==element:
                return True
            else:
                self.framework.lg("wrong EC table page elements ")
                return False


    def ECs_in_tables_after_purge(self,num_days):
        date_days_ago = datetime.now() - timedelta(days=num_days)
        date_days_ago = "{:%m/%d/%Y %H:%M }".format(date_days_ago)
        self.framework.set_text("EC_table_date_end_search" ,date_days_ago)
        self.framework.assertTrue(self.framework.wait_until_element_located('EC_table_date_click_button'))
        self.framework.click("EC_table_date_click_button")
        self.framework.assertTrue(self.framework.wait_until_element_located('table_ECs_info'))
        ECs_info = self.framework.Tables.get_table_info('table_ECs_info')
        ECs= int(ECs_info[ECs_info.index('f') + 2:ECs_info.index('en') - 1].replace(',', ''))
        return ECs

    def get_cpu_node_page(self):
        self.framework.click_link(self.framework.element_link('EC_node_page'))
        for _ in range(10):
            if 'grid%20node?id=' in self.framework.driver.current_url:
                return True
            else:
                time.sleep(1)
        else:
            return False
