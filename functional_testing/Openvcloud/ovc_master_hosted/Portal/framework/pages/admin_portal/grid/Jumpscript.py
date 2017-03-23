from random import randint
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
from datetime import datetime, timedelta,date
import time

class JumpScripts():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.LeftNavigationMenu.Grid.Jumpscripts()

    def is_at(self):
        if "grid/Jumpscripts" in self.framework.driver.current_url:
            if "Grid JumpScripts" in self.framework.driver.title:
                return True
            else:
                self.framework.lg("title of page doesn't correct")
                return False
        else:
            self.framework.lg("url of page  doesn't correct")
            return False

    def check_jumpscripts_table_heads(self,table):
        table = self.framework.Tables.generate_table_elements(table)
        heads=self.framework.get_table_head_elements(table['data'])
        jumpscripts_heads=['ID','Name','Organization','Category','Description']
        elements=[]
        for head in heads:
            elements.append(str(head.text))
        if elements != jumpscripts_heads:
            self.framework.lg("jumpscripts table heads %s not true "%elements)
            return False
        return True

    def open_Jumpscript_page(self, JumpScript='',table=''):
        self.framework.LeftNavigationMenu.Grid.Jumpscripts()
        self.framework.set_text("jumpscript_ID_coulmn_search",JumpScript)
        if self.framework.wait_until_element_located_and_has_text("jumpscript_first_element_ID_column", JumpScript):
            jumpscript_herf = self.framework.element_link("jumpscript_first_element_ID_column")
            self.table_elements_aftersearch=self.framework.get_table_row(table,0)
            jumpscript_id = jumpscript_herf[jumpscript_herf.find('?id=')+len('?id='):]
            self.framework.click_link(jumpscript_herf)
            return self.framework.element_in_url(jumpscript_id )

        else:
            self.framework.lg('can\'t find jumpscript %s' % JumpScript)
            return False

    def check_exist_of_jumpscript_properts(self):
        self.tableData=self.framework.Tables.get_details_table_data('details_table')
        if self.tableData == False:
            self.framework.lg('can\'t get table details of jumpscript page')
            return False
        jumpscript_elements=['Category','Log','Descr','Author','Version','Organization','Argsdefaults','Enable','Roles','Args','Argsvarargs',
                             'Startatboot','Path','Name','License','Enabled','Queue','Argskeywords','Timeout','Async','Order','Period',
                             'Gid','Guid','Id']
        for i,element in enumerate(jumpscript_elements):
            if str(self.tableData[i][0])==element:
                return True
            else:
                self.framework.lg("jumpscript property %s missing "%element)
                return False

    def check_exist_of_code(self):
        code=self.framework.get_attribute('jumpscript_code',"value")
        if str(code) =='':
            return False
        return True
