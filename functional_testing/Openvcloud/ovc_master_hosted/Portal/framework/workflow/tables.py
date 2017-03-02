import time
from random import randint

class tables():
    def __init__(self, framework):
        self.framework = framework

    def generate_table_elements(self, table):
        table_dict = {'data':'table_%s_data' % table,
                     'info':'table_%s_info' % table,
                     'selector':'table_%s_selector' % table,
                     'pagination':'table_%s_pagination' % table,
                     'search_box':'table_%s_search_box' % table}
        return table_dict


    def get_table_info(self, element):
        for _ in range(10):
            account_info = self.framework.get_text(element)
            if "Showing" in account_info:
                return account_info
            else:
                time.sleep(1)
        else:
            self.framework.fail("Can't get the table info")

    def get_table_start_number(self, table_info):
        account_info = self.get_table_info(table_info)
        return int(account_info[(account_info.index('g') + 2):(account_info.index('to') - 1)])

    def get_table_end_number(self, table_info):
        account_info = self.get_table_info(table_info)
        return int(account_info[(account_info.index('to') + 3):(account_info.index('of') - 1)])

    def get_table_max_number(self, table_info):
        account_info = self.get_table_info(table_info)
        return int(account_info[(account_info.index('f') + 2):(account_info.index('entries') - 1)].replace(',',''))

    def get_previous_next_button(self, pagination):
        pagination = self.framework.find_element(pagination)
        pagination = pagination.find_element_by_tag_name('ul')
        pagination = pagination.find_elements_by_tag_name('li')
        previous_button = pagination[0].find_element_by_tag_name('a')
        next_button = pagination[(len(pagination) - 1)].find_element_by_tag_name('a')

        return previous_button, next_button

    def get_table_data(self, table):
        self.framework.assertTrue(self.framework.check_element_is_exist(table['info']))
        max_sort_value = 100
        account_max_number = self.get_table_max_number(table['info'])
        self.framework.select(table['selector'] , max_sort_value)
        time.sleep(3)
        page_numbers = (account_max_number / max_sort_value)
        if (account_max_number % max_sort_value) > 0:
            page_numbers += 1
        tableData = []
        for page in range(page_numbers):

            table_rows = self.framework.get_table_rows(table['data'])
            self.framework.assertTrue(table_rows)
            for row in table_rows:
                cells = row.find_elements_by_tag_name('td')
                tableData.append([x.text for x in cells])
            if  page < (page_numbers-1):
                previous_button, next_button = self.get_previous_next_button(table['pagination'])
                next_button.click()

                tb_max_number = self.get_table_max_number(table['info'])
                tb_start_number = 1+((page+1)*max_sort_value)
                tb_end_number = (page+2)*max_sort_value

                if tb_end_number > tb_max_number:
                    tb_end_number = tb_max_number

                text = "Showing %s to %s of %s entries" %("{:,}".format(tb_start_number), "{:,}".format(tb_end_number), "{:,}".format(tb_max_number))
                if not self.framework.wait_until_element_located_and_has_text(table['info'], text):
                    return False
        return tableData

    def check_show_list(self, table):
        table = self.generate_table_elements(table)
        paging_options = [25, 50, 100, 10]
        rows_max_number = self.get_table_max_number(table['info'])
        for option in paging_options:
            self.framework.select(table['selector'], option)
            time.sleep(3)
            rows_max_number_ = self.get_table_max_number(table['info'])
            rows_end_number_ = self.get_table_end_number(table['info'])
            if rows_max_number != rows_max_number_:
                return False
            if rows_max_number > option:
                if rows_end_number_ != option:
                    return False
            else:
                if not rows_end_number_ < option:
                    return False

        return True

    def check_next_previous_buttons(self, table):
        table = self.generate_table_elements(table)
        rows_max_number = self.get_table_max_number(table['info'])
        pagination = self.framework.find_element(table['pagination'])
        pagination = pagination.find_element_by_tag_name('ul')
        pagination = pagination.find_elements_by_tag_name('li')

        for _ in range((len(pagination) - 3)):
            page_start_number = self.get_table_start_number(table['info'])
            page_end_number = self.get_table_end_number(table['info'])
            previous_button, next_button = self.get_previous_next_button(table['pagination'])
            next_button.click()
            time.sleep(4)
            page_start_number_ = self.get_table_start_number(table['info'])
            page_end_number_ = self.get_table_end_number(table['info'])

            if page_start_number_ != page_start_number+10:
                return False
            if page_end_number_ < rows_max_number:
                if page_end_number_ != page_end_number+10:
                    return False
            else:
                if page_end_number_ != rows_max_number:
                    return False

            previous_button, next_button = self.get_previous_next_button(table['pagination'])
            previous_button.click()
            time.sleep(4)
            page_start_number__ = self.get_table_start_number(table['info'])
            page_end_number__ = self.get_table_end_number(table['info'])

            if page_start_number__ != page_start_number_-10:
                return False

            previous_button, next_button = self.get_previous_next_button(table['pagination'])
            next_button.click()
            time.sleep(4)

        return True

    def check_sorting_table(self, table):
        table = self.generate_table_elements(table)
        self.framework.select(table['selector'] , 100)
        table_location = self.framework.find_element(table['data']).location
        table_head_elements = self.framework.get_table_head_elements(table['data'])
        for column, element in enumerate(table_head_elements):
            if 'sorting_disabled' in element.get_attribute('class'):
                continue

            current_column = element.text
            self.framework.driver.execute_script("window.scrollTo(0,%d)" % (table_location['y']-50))
            element.click()
            self.framework.wait_until_element_attribute_has_text(element, 'aria-sort', 'ascending')
            table_before = self.get_table_data(table)

            if not table_before:
                return False

            self.framework.driver.execute_script("window.scrollTo(0,%d)" % (table_location['y']-50))
            element.click()
            self.framework.wait_until_element_attribute_has_text(element, 'aria-sort', 'descending')
            table_after = self.get_table_data(table)

            if not table_after:
                return False

            for temp in range(len(table_before)):
                if not table_before[temp][column] == table_after[(len(table_after)-temp-1)][column]:
                    return False

            self.framework.lg('coulmn %s passed' % current_column)

        return True

    def check_search_box(self, table):
        table = self.generate_table_elements(table)
        table_head_elements = self.framework.get_table_head_elements(table['data'])
        table_before = self.get_table_data(table)
        columns = len(table_head_elements)
        rows = len(table_before)
        random_element = randint(0,rows-1)
        for column in range(columns):
            self.framework.set_text(table['search_box'], table_before[random_element][column])
            time.sleep(2)
            table_after = self.get_table_data(table)

            if not any(table_before[random_element][column] in s for s in table_after[0]):
                return False

        self.framework.clear_text(table['search_box'])
        return True

    def check_data_filters(self, table):
        table = self.generate_table_elements(table)
        table_before = self.get_table_data(table)
        table_head_elements = self.framework.get_table_head_elements(table['data'])
        columns = len(table_head_elements)
        rows = len(table_before)
        random_element = randint(0,rows-1)

        table_data = self.framework.find_element(table['data'])
        footer = table_data.find_element_by_tag_name('tfoot')
        items = footer.find_elements_by_tag_name('td')
        filters = [x.find_elements_by_tag_name('input')[0] for x in items]

        for column in range(columns):
            if 'nofilter' in table_head_elements[column].get_attribute('class'):
                continue

            current_filter = filters[column]
            current_filter.send_keys(table_before[random_element][column])
            time.sleep(1)
            table_after = self.get_table_data(table)

            if not table_after[0][column] == table_before[random_element][column]:
                return False

            self.framework.clear_element_text(current_filter)

        return True
