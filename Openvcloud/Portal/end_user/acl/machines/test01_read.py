

class Read():

    def test01_machine_get(self):
        """
        *Test case for get machine.*

        **Test Scenario:**

        #. try to get machine with new user [user], should return 403
        #. add user to the machine with read access
        #. get machine with new user [user], should succeed
        #. create new machine with user2, should succeed
        #. get machine with user2, should succeed
        """
        pass

    def test02_machine_list(self):
        """
        *Test case for list machine.*

        **Test Scenario:**

        #. try to list machines with new user [user], should return 403
        #. add user to the machine with read access
        #. list machines with new user [user], should succeed
        #. create new machine with user2, should succeed
        #. list machines with new user [user] still see 1 machine, should succeed
        """
        pass

    def test03_machine_getConsoleUrl(self):
        """ 
        *Test case for getConsoleUrl machine.*

        **Test Scenario:**

        #. try to getConsoleUrl machine with new user [user], should return 403
        #. add user to the machine with read access
        #. getConsoleUrl machine with new user [user], should succeed
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

        #. try to getHistory of created machine with new user [user], should return 403
        #. add user to the machine with read access
        #. getHistory of created machine with new user [user], should succeed
        """
        pass
