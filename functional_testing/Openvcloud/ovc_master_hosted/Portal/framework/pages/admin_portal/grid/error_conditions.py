from random import randint
import time
class errorConditions():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.lg('get grid.error_conditions page')
        self.framework.LeftNavigationMenu.Grid.error_conditions()
        self.framework.assertTrue(self.framework.check_element_is_exist("error_conditions_page"))


    def open_EC_page(self, EC='',Ec_date=''):
        self.LeftNavigationMenu.Grid.error_conditions()

        self.framework.set_text("error_conditions_search", EC)

        out=self.framework.wait_until_element_located_and_has_text("EC_table_first_element_2",
                                                               EC)
        EC_herf = self.framework.element_link("EC_table_first_element_1")
        self.table_elements_aftersearch=self.framework.Tables.get_table_data('table_ECs_info')
        EC_id = EC_herf[EC_herf.find('?id=')+len('?id='):]
        self.framework.click_link(EC_herf)
        return self.framework.element_in_url(EC_id )

    def random_element(self,table):
        rows= len(table)
        random_elemn= randint(0,rows-1)
        EC_element=table[random_elemn][1]
        skip_characters=['.',':','\'']
        if EC_element[0]== '<':
            EC_element=EC_element[(EC_element.index('>')+2) :]
        #skip 'https://github.com/0-complexity/openvcloud/issues/771'
        EC_element=EC_element[ :(EC_element.find('.'))]
        EC_element=EC_element[ :(EC_element.find(':'))]
        EC_element=EC_element[ :(EC_element.find('\''))]
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
            #print job_link.get_attribute("href")
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
        self.framework.assertEqual(str(self.application_name),self.table_elements_aftersearch[0][2])
        self.framework.assertEqual(str(self.accurrence),self.table_elements_aftersearch[0][3])
        self.framework.assertTrue(self.table_elements_aftersearch[0][4] in str(self.cpu_node))
        self.framework.assertEqual(str(self.grid_Id),self.table_elements_aftersearch[0][5])

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
            if 'grid node?id=%s'%self.cpu_node in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def get_Grid_page(self):
        self.framework.click_link(self.framework.element_link('EC_Grid_page'))
        for _ in range(10):
            if 'grid?id=%s'%self.grid_Id in self.framework.driver.title:
                return True
            else:
                time.sleep(1)
        else:
            return False
