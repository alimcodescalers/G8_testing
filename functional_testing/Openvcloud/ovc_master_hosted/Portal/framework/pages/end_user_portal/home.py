class home():
    def __init__(self, framework):
        self.framework = framework

    def get_it(self):
        self.framework.lg('Open end user home page')
        self.framework.get_page(self.framework.environment_url)
        self.framework.assertEqual(self.framework.get_text("end_user_home"),"Machines","FAIL: Can't open the end user home page")
