class GridVirtualMachines():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.LeftNavigationMenu.Grid.vmachin_grid()

    def is_at(self):
        if "grid/Virtual%20Machines" in self.framework.driver.current_url:
            if "Grid Virtual Machines" in self.framework.driver.title:
                return True
            else:
                self.framework.lg("title of page doesn't correct")
                return False
        else:
            self.framework.lg("url of page  doesn't correct")
            return False
