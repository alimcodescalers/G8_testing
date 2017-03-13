class statusOverview():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.lg('get grid.status_overview page')
        self.framework.LeftNavigationMenu.Grid.status_overview()
        self.framework.assertEqual(self.framework.driver.title, "Grid Status Overview")

    def get_node_status(self):
        node_staus = []
        rows = self.framework.get_table_rows()
        if rows == False:
            self.framework.lg('There is no rows in this table')
            return False
        for row in rows:
            cells = self.framework.get_row_cells(row)
            if cells == False:
                self.framework.lg('There is no cells in this row')
                return False
            node_staus.append(cells[3].text)
        return node_staus

    def run_health_check(self,element):
        self.framework.click('Run Healthcheck')
        if not self.framework.wait_until_element_located_and_has_text(element,'Confirm Action Run Health Check'):
            self.framework.lg("can't find action-RunHealthcheckLabel element ")
            return False
        self.framework.click('confirm_alert')
        self.framework.wait_until_element_located('alert healthcheck')
        health_check=self.framework.get_text('alert healthcheck')
        if not health_check:
            self.framework.lg("can't find alert_healthcheck element ")
            return False
        if health_check != 'Scheduled healthcheck':
            self.framework.lg('Health check message: %s' % health_check)
            return False
        return True

    def open_Status_overview_page(self, SO='',table=''):
        self.framework.LeftNavigationMenu.Grid.status_overview()

        self.framework.set_text("table_Status_overview_search_box", SO)

        if self.framework.wait_until_element_located_and_has_text("table_Status_overview_node_name", SO):
            EC_herf = self.framework.element_link("table_Status_overview_details")
            EC_id = EC_herf[EC_herf.find('?id=')+len('?id='):]
            self.framework.click_link(EC_herf)
            return self.framework.element_in_url(EC_id )

        else:
            self.framework.lg('can\'t find node_status_overview %s' % SO)
            return False
