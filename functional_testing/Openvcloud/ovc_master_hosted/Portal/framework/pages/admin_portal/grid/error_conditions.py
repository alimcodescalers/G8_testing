from random import randint
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
import time
class errorConditions():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.lg('get grid.error_conditions page')
        self.framework.LeftNavigationMenu.Grid.error_conditions()
        self.framework.assertTrue(self.framework.check_element_is_exist("error_conditions_page"))


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
        self.framework.assertEqual(len(table_rows),15)
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
        self.framework.assertEqual(str(self.tableData[0][0]),'Application Name')
        self.framework.assertEqual(str(self.tableData[1][0]),'Category')
        self.framework.assertEqual(str(self.tableData[2][0]),'Job')
        self.framework.assertEqual(str(self.tableData[3][0]),'Type')
        self.framework.assertEqual(str(self.tableData[4][0]),'Level')
        self.framework.assertEqual(str(self.tableData[5][0]),'Creation Time')
        self.framework.assertEqual(str(self.tableData[6][0]),'Last Time')
        self.framework.assertEqual(str(self.tableData[7][0]),'Occurrences')
        self.framework.assertEqual(str(self.tableData[8][0]),'Error Message Pub')
        self.framework.assertEqual(str(self.tableData[9][0]),'Function Name')
        self.framework.assertEqual(str(self.tableData[10][0]),'Function Line Number')
        self.framework.assertEqual(str(self.tableData[11][0]),'Function File Name')
        self.framework.assertEqual(str(self.tableData[11][0]),'Function File Name')
        self.framework.assertEqual(str(self.tableData[12][0]),'Node')
        self.framework.assertEqual(str(self.tableData[13][0]),'Grid')
        self.framework.assertEqual(str(self.tableData[14][0]),'Tags')

    def get_cpu_node_page(self):
        self.framework.click_link(self.framework.element_link('EC_node_page'))
        for _ in range(10):
            if 'grid%20node?id=' in self.framework.driver.current_url:
                return True
            else:
                time.sleep(1)
        else:
            return False
