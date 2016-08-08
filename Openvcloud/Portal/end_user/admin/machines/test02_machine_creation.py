

class Read():

    def test01_machine_get(self):
        """
        *Test case for get machine.*

        **Test Scenario:**

        #. create new machine, should succeed
        #. get machine, should succeed
        """
        pass

    def test02_machine_list(self):
        """
        *Test case for list machine.*

        **Test Scenario:**

        #. create new machine, should succeed
        #. list machines should see 1 machine, should succeed
        """
        pass

    def test03_machine_getConsoleUrl(self):
        """ 
        *Test case for getConsoleUrl machine.*

        **Test Scenario:**

        #. create new machine, should succeed
        #. getConsoleUrl machine, should succeed
        """
        pass

    def test04_machine_listSnapshots(self):
        """
        *Test case for listSnapshots machine.*

        **Test Scenario:**

        #. create snapshot for a machine with the account user, should succeed
        #. try to listSnapshots of created machine with new user [user], should return 403
        #. add user to the machine with read access
        #. listSnapshots of created machine with new user [user], should succeed
        """
        pass

    def test05_machine_getHistory(self):
        """
        *Test case for getHistory machine.*

        **Test Scenario:**

        #. create new machine, should succeed
        #. getHistory of created machine, should succeed
        """
        pass

