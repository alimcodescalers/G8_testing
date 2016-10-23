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
        return int(account_info[(account_info.index('f') + 2):(account_info.index('entries') - 1)])

    def get_previous_next_button(self):
        pagination = self.framework.get_list_items('pagination')
        previous_button = pagination[0].find_element_by_tag_name('a')
        next_button = pagination[(len(pagination) - 1)].find_element_by_tag_name('a')
        return previous_button, next_button

    def get_table_data(self, element):
        # This method will return a table data as a list
        self.framework.assertTrue(self.framework.check_element_is_exist('thead'))
        max_sort_value = 100

        account_max_number = self.get_table_max_number(element)
        self.framework.select('account selector', max_sort_value)
        time.sleep(3)
        page_numbers = (account_max_number / max_sort_value) + 1

        tableData = []
        for page in range(page_numbers):
            table_rows = self.framework.get_table_rows()
            self.framework.assertTrue(table_rows)
            for row in table_rows:
                tableData.append(row.text)

            if 0 < page < (page_numbers - 1):
                previous_button, next_button = self.get_previous_next_button()
                next_button.click()

        return tableData