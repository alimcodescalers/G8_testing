from random import randint
from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.Navigation.left_navigation_menu import \
    leftNavigationMenu
from datetime import datetime, timedelta,date
import time
class Jobs():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.LeftNavigationMenu.Grid.Jobs()

    def is_at(self):
        if "grid/Jobs" in self.framework.driver.current_url:
            if "Grid Jobs" in self.framework.driver.title:
                return True
            else:
                self.framework.lg("title of page doesn't correct")
                return False
        else:
            self.framework.lg("url of page  doesn't correct")
            return False

    def check_jobs_table_heads(self,table):
        table = self.framework.Tables.generate_table_elements(table)
        heads=self.framework.get_table_head_elements(table['data'])
        jobs_heads=['Create Time','Start','Stop','Command','Queue','State']
        elements=[]
        for head in heads:
            elements.append(head.text)
        if elements != jobs_heads:
            self.framework.lg("jobs table heads %s not true "%elements)
            return False
        return True

    def jobs_in_tables_after_purge(self,num_days,num_hours):
        date_days_ago = datetime.now() - timedelta(days=num_days+1,hours=num_hours)
        date_days_ago = "{:%m/%d/%Y %H:%M }".format(date_days_ago)
        self.framework.set_text("job_table_date_end_search" ,date_days_ago)
        self.framework.assertTrue(self.framework.wait_until_element_located('EC_table_date_click_button'))
        self.framework.click("job_table_date_click_button")
        self.framework.assertTrue(self.framework.wait_until_element_located('table_jobs_info'))
        jobs_info = self.framework.Tables.get_table_info('table_jobs_info')
        Jobs= int(jobs_info[jobs_info.index('f') + 2:jobs_info.index('en') - 1].replace(',', ''))
        return Jobs


    def open_Job_page(self, Job='',table=''):
        self.framework.LeftNavigationMenu.Grid.Jobs()
        self.framework.set_text("table_jobs_search_box",Job)
        if self.framework.wait_until_element_located_and_has_text("job_first_element_command_column", Job):
            job_herf = self.framework.element_link("job_first_element_createtime_column")
            self.table_elements_aftersearch=self.framework.get_table_row(table,0)
            job_id = job_herf[job_herf.find('?id=')+len('?id='):]
            self.framework.click_link(job_herf)
            return self.framework.element_in_url(job_id )

        else:
            self.framework.lg('can\'t find job %s' % Job)
            return False

    def Job_details_table(self,table_element):
        self.table=[]
        table_rows= self.framework.get_table_rows(table_element)
        for row in table_rows:
            cells = row.find_elements_by_tag_name('td')
            self.table.append([x.text for x in cells])
        return self.table

    def check_job_elements(self):
        self.tableData=self.Job_details_table('job_details_table')
        self.Start=self.tableData[4][1]
        self.Stop=self.tableData[5][1]
        self.Queue=self.tableData[6][1]
        self.State=self.tableData[7][1]
        self.framework.assertTrue(str(self.Start) in self.table_elements_aftersearch[1])
        self.framework.assertTrue(str(self.Stop) in self.table_elements_aftersearch[2])
        self.framework.assertTrue(self.table_elements_aftersearch[4] in str(self.Queue))
        self.framework.assertTrue(self.table_elements_aftersearch[5] in str(self.State) )

    def check_exist_of_job_elements(self):
        self.tableData=self.Job_details_table('job_details_table')
        if self.tableData == False:
            self.framework.lg('can\'t get table details of job page')
            return False
        job_elements=['Grid ID','Node','Roles','Jumpscript','Start','Stop','Queue','State']
        for i,element in enumerate(job_elements):
            if str(self.tableData[i][0])==element:
                return True
            else:
                self.framework.lg("wrong job page element ")
                return False

    def check_exist_of_additional_info_elements(self):
        self.tableData=self.Job_details_table('job_addition_table')
        if self.tableData == False:
            self.framework.lg('can\'t get aadditional info  of job page')
            return False
        Additional_Info=['Job Completed','Category','Parent']
        for i,element in enumerate(Additional_Info):
            if str(self.tableData[i][0])==element:
                return True
            else:
                self.framework.lg("wrong additional info ")
                return False

    def get_cpu_node_page(self):
        self.framework.click_link(self.framework.element_link('job_node_page'))
        for _ in range(10):
            if 'grid%20node?id=' in self.framework.driver.current_url:
                return True
            else:
                time.sleep(1)
        else:
            return False

    def get_jumpscript_page(self):
        self.framework.click_link(self.framework.element_link('job_jumpscript_page'))
        for _ in range(10):
            if '/grid/jumpscript?id=' in self.framework.driver.current_url:
                return True
            else:
                time.sleep(1)
        else:
            return False
