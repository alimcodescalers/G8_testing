import time

class tables():
    def __init__(self, framework):
        self.framework = framework

    def get_table_info(self, element):
        for _ in range(10):
            account_info = self.framework.get_text(element)
            if "Showing" in account_info:
                return account_info
            else:
                time.sleep(1)
        else:
            self.framework.fail("Can't get the table info")

    def get_table_start_number(self, table_info_element):
        account_info = self.get_table_info(table_info_element)
        return int(account_info[(account_info.index('g') + 2):(account_info.index('to') - 1)])

    def get_table_end_number(self, table_info_element):
        account_info = self.get_table_info(table_info_element)
        return int(account_info[(account_info.index('to') + 3):(account_info.index('of') - 1)])

    def get_table_max_number(self, table_info_element):
        account_info = self.get_table_info(table_info_element)
        return int(account_info[(account_info.index('f') + 2):(account_info.index('entries') - 1)].replace(',',''))

    def get_previous_next_button(self , pagination=None):
        if pagination == None:
            pagination = self.framework.get_list_items('pagination')
        else:
            table = self.framework.find_element(pagination)
            pagination = table.find_element_by_tag_name('ul')
            pagination = pagination.find_elements_by_tag_name('li')

        previous_button = pagination[0].find_element_by_tag_name('a')
        next_button = pagination[(len(pagination) - 1)].find_element_by_tag_name('a')

        return previous_button, next_button

    def get_table_data(self, element, selector = 'account selector',table_element=None, pagination=None):
        # This method will return a table data as a list
        self.framework.assertTrue(self.framework.check_element_is_exist(element))
        max_sort_value = 100
        account_max_number = self.get_table_max_number(element)
        self.framework.select( selector , max_sort_value)
        time.sleep(3)
        page_numbers = (account_max_number / max_sort_value)
        if (account_max_number % max_sort_value) > 0:
            page_numbers += 1
        tableData = []
        for page in range(page_numbers):

            table_rows = self.framework.get_table_rows(table_element)
            self.framework.assertTrue(table_rows)
            for row in table_rows:
                cells = row.find_elements_by_tag_name('td')
                tableData.append([x.text for x in cells])
            if  page < (page_numbers-1):
                previous_button, next_button = self.get_previous_next_button(pagination)
                next_button.click()

                tb_max_number = self.get_table_max_number(element)
                tb_start_number = 1+((page+1)*max_sort_value)
                tb_end_number = (page+2)*max_sort_value

                if tb_end_number > tb_max_number:
                    tb_end_number = tb_max_number

                text = "Showing %s to %s of %s entries" %("{:,}".format(tb_start_number), "{:,}".format(tb_end_number), "{:,}".format(tb_max_number))
                if not self.framework.wait_until_element_located_and_has_text(element, text):
                    return False
        return tableData
