from random import randint
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
import datetime
import time
class Audits():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.LeftNavigationMenu.Grid.Audits()

    def is_at(self):
        if "grid/Audits" in self.framework.driver.current_url:
            if "Grid Audits" in self.framework.driver.title:
                return True
            else:
                self.framework.lg("title of page doesn't correct")
                return False
        else:
            self.framework.lg("url of page  doesn't correct")
            return False

    def check_Audits_table_heads(self,table):
        table = self.framework.Tables.generate_table_elements(table)
        heads=self.framework.get_table_head_elements(table['data'])
        Audits_heads=['Time' ,'User','Call', 'Response Time' , 'Status Code']

        elements=[]
        for head in heads:
            elements.append(head.text)
        if elements != Audits_heads:
            self.framework.lg("Audits table heads %s not true "%elements)
            return False
        return True

    def open_Audit_page(self, Call='',table=''):
        self.framework.LeftNavigationMenu.Grid.Audits()
        self.framework.set_text("table_Audits_search_box",Call)
        if self.framework.wait_until_element_located_and_has_text("Audit_first_element_call_column", Call):
            Audit_herf = self.framework.element_link("Audit_first_element_time_column")
            self.table_elements_aftersearch=self.framework.get_table_row(table,0)
            Audit_id = Audit_herf[Audit_herf.find('?id=')+len('?id='):]
            self.framework.click_link(Audit_herf)
            return self.framework.element_in_url(Audit_id )

        else:
            self.framework.lg('can\'t find Audit %s' % Call)
            return False

    def audit_details_table(self,table_element):
        self.table=[]
        table_rows= self.framework.get_table_rows(table_element)
        for row in table_rows:
            cells = row.find_elements_by_tag_name('td')
            self.table.append([x.text for x in cells])
        return self.table

    def check_audit_elements(self):
        self.tableData=self.audit_details_table('Audit_details_table')
        self.Time=self.tableData[0][1]
        d=datetime.datetime.strptime( self.table_elements_aftersearch[0], '%m/%d/%Y, %H:%M:%S %p')
        self.Time_aftersearch=d.strftime('%m-%d')
        self.User=self.tableData[1][1]
        self.Call=self.tableData[2][1]
        self.Status_Code=self.tableData[3][1]
        self.framework.assertTrue(self.Time_aftersearch in self.Time )
        self.framework.assertEqual(str(self.User),self.table_elements_aftersearch[1])
        self.framework.assertEqual(self.table_elements_aftersearch[2] ,str(self.Call))
        self.framework.assertEqual(self.table_elements_aftersearch[4] ,str(self.Status_Code ))

    def check_exist_of_audit_elements(self):
        self.tableData=self.audit_details_table('Audit_details_table')
        if self.tableData == False:
            self.framework.lg('can\'t get table details of audit page')
            return False
        Audits_elements=['Time','User','Call','Status Code','Response Time','Tags','Link to Error Condition']
        for i,element in enumerate(Audits_elements):
            if str(self.tableData[i][0])==element:
                return True
            else:
                self.framework.lg("wrong audit page element ")
                return False
