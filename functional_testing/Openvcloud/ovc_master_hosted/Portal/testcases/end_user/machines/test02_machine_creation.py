from functional_testing.Openvcloud.ovc_master_hosted.Portal.framework.framework import Framework


class Read(Framework):
    def __init__(self, *args, **kwargs):
        super(Read, self).__init__(*args, **kwargs)

    def setUp(self):
        super(Read, self).setUp()
        self.Login.Login()
        self.lg('create new account')
        self.Accounts.create_new_account(self.account, self.admin_username+"@itsyouonline")
        self.lg('create new cloudspace')
        self.CloudSpaces.create_cloud_space(self.account, self.cloudspace)
        self.EUHome.get_it()

    def tearDown(self):
        super(Read, self).tearDown()
        self.Accounts.get_it()
        self.lg('delete cloudspace')
        self.CloudSpaces.delete_cloudspace(self.cloudspace)
        self.lg('delete account')
        self.Accounts.delete_account(self.account)
        self.Logout.Admin_Logout()


#     def test01_machine_get(self):
#         """
#         *Test case for get machine.*
#
#         **Test Scenario:**
#
#         #. create new machine, should succeed
#         #. get machine, should succeed
#         """
#
#     def test02_machine_list(self):
#         """
#         *Test case for list machine.*
#
#         **Test Scenario:**
#
#         #. create new machine, should succeed
#         #. list machines should see 1 machine, should succeed
#         """
#         pass
#
#     def test03_machine_getConsoleUrl(self):
#         """
#         *Test case for getConsoleUrl machine.*
#
#         **Test Scenario:**
#
#         #. create new machine, should succeed
#         #. getConsoleUrl machine, should succeed
#         """
#         pass
#
#     def test04_machine_listSnapshots(self):
#         """
#         *Test case for listSnapshots machine.*
#
#         **Test Scenario:**
#
#         #. create snapshot for a machine with the account user, should succeed
#         #. try to listSnapshots of created machine with new user [user], should return 403
#         #. add user to the machine with read access
#         #. listSnapshots of created machine with new user [user], should succeed
#         """
#         pass
#
#     def test05_machine_getHistory(self):
#         """
#         *Test case for getHistory machine.*
#
#         **Test Scenario:**
#
#         #. create new machine, should succeed
#         #. getHistory of created machine, should succeed
#         """
#         pass


    '''
    @parameterized.expand(["ubuntu_14_04",
                           "ubuntu_15_10",
                           "ubuntu_16_04",
                           "windows_2012"
                           ])
    '''

    def test06_machine_create(self, image_name="ubuntu_14_04"):
        """ PRTL-011
        *Test case for creating/deleting machine with all avaliable image name, random package and random disk size*

        **Test Scenario:**

        #. create new machine, should succeed
        #. delete the new machine

        """
        self.lg('%s STARTED' % self._testID)
        self.lg(' create %s machine ' % self.machine_name)
        self.assertTrue(self.EUMachines.end_user_create_virtual_machine(image_name,self.machine_name))
        self.lg('delete %s machine ' % self.machine_name)
        self.assertTrue(self.EUMachines.end_user_delete_virtual_machine(self.machine_name))
        self.lg('%s ENDED' % self._testID)
