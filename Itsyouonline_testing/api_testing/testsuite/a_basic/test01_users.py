from Itsyouonline_testing.api_testing.utils import BaseTest


class UsersTests(BaseTest):

    def setUp(self):
        super(UsersTests, self).setUp()
        self.response = self.client.api.GetUser(self.user)

    def test001_get_user(self):
        """ ITSYOU-001
        *Test case for check get user /users/{username}.*

        **Test Scenario:**

        #. check get user, should succeed
        #. validate all expected keys in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.response
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s" % self.user)
        self.assertIn('addresses', response.json().keys())
        self.assertIn('bankaccounts', response.json().keys())
        self.assertIn('digitalwallet', response.json().keys())
        self.assertIn('emailaddresses', response.json().keys())
        self.assertIn('expire', response.json().keys())
        self.assertIn('facebook', response.json().keys())
        self.assertIn('firstname', response.json().keys())
        self.assertIn('github', response.json().keys())
        self.assertIn('lastname', response.json().keys())
        self.assertIn('phonenumbers', response.json().keys())
        self.assertIn('publicKeys', response.json().keys())
        self.assertIn('username', response.json().keys())
        self.lg('%s ENDED' % self._testID)

    def test002_get_user_addresses(self):
        """ ITSYOU-002
        *Test case for check get user addressess /users/{username}/addresses.*

        **Test Scenario:**

        #. check get user addressess, should succeed
        #. validate all expected user addressess in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetUserAddresses(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s addresses" % self.user)
        self.assertEqual(response.json(), self.response.json()['addresses'])
        self.lg('%s ENDED' % self._testID)

    def test003_get_user_emailaddresses(self):
        """ ITSYOU-003
        *Test case for check get user email addressess /users/{username}/emailaddresses.*

        **Test Scenario:**

        #. check get user email addressess, should succeed
        #. validate all expected email addressess in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetEmailAddresses(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s email addresses" % self.user)
        self.assertEqual(response.json(), self.response.json()['emailaddresses'])
        self.lg('%s ENDED' % self._testID)

    def test004_get_user_notifications(self):
        """ ITSYOU-004
        *Test case for check get user notifications /users/{username}/notifications.*

        **Test Scenario:**

        #. check get user notifications, should succeed
        #. validate all expected notifications in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetNotifications(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s notifications" % self.user)
        self.assertEqual(response.json(), self.response.json()['notifications'])
        self.lg('%s ENDED' % self._testID)

    def test005_get_user_organizations(self):
        """ ITSYOU-005
        *Test case for check get user organizations /users/{username}/organizations.*

        **Test Scenario:**

        #. check get user organizations, should succeed
        #. validate all expected organizations in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetUserOrganizations(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s organizations" % self.user)
        self.assertEqual(response.json(), self.response.json()['organizations'])
        self.lg('%s ENDED' % self._testID)

    def test006_get_user_bankaccounts(self):
        """ ITSYOU-006
        *Test case for check get user bankaccounts /users/{username}/bankaccounts.*

        **Test Scenario:**

        #. check get user bankaccounts, should succeed
        #. validate all expected bankaccounts in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetUserBankAccounts(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s bankaccounts" % self.user)
        self.assertEqual(response.json(), self.response.json()['bankaccounts'])
        self.lg('%s ENDED' % self._testID)

    def test007_get_user_bankaccounts(self):
        """ ITSYOU-007
        *Test case for check get user bankaccounts /users/{username}/bankaccounts.*

        **Test Scenario:**

        #. check get user bankaccounts, should succeed
        #. validate all expected bankaccounts in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetUserBankAccounts(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s bankaccounts" % self.user)
        self.assertEqual(response.json(), self.response.json()['bankaccounts'])
        self.lg('%s ENDED' % self._testID)

    def test008_get_user_username(self):
        """ ITSYOU-008
        *Test case for check get user username /users/{username}/username.*

        **Test Scenario:**

        #. check get user username, should succeed
        #. validate all expected username in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetUser(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s username" % self.user)
        self.assertEqual(response.json(), self.response.json()['username'])
        self.lg('%s ENDED' % self._testID)

    def test009_get_user_apikeys(self):
        """ ITSYOU-009
        *Test case for check get user apikeys /users/{username}/apikeys.*

        **Test Scenario:**

        #. check get user apikeys, should succeed
        #. validate all expected apikeys in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.ListAPIKeys(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s apikeys" % self.user)
        self.assertEqual(response.json(), self.response.json()['apikeys'])
        self.lg('%s ENDED' % self._testID)

    def test010_get_user_info(self):
        """ ITSYOU-010
        *Test case for check get user info /users/{username}/info.*

        **Test Scenario:**

        #. check get user apikeys, should succeed
        #. validate all expected apikeys in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetUserInformation(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s info" % self.user)
        self.assertEqual(response.json(), self.response.json()['info'])
        self.lg('%s ENDED' % self._testID)

    def test011_get_user_contracts(self):
        """ ITSYOU-011
        *Test case for check get user info /users/{username}/contracts.*

        **Test Scenario:**

        #. check get user contracts, should succeed
        #. validate all expected contracts in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetUserContracts(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s contracts" % self.user)
        self.assertEqual(response.json(), self.response.json()['contracts'])
        self.lg('%s ENDED' % self._testID)

    def test012_get_user_authorizations(self):
        """ ITSYOU-012
        *Test case for check get user authorizations /users/{username}/authorizations.*

        **Test Scenario:**

        #. check get user authorizations, should succeed
        #. validate all expected authorizations in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetAllAuthorizations(self.user)
        if response.status_code != 200:
            raise AssertionError("Failed to get user %s authorizations" % self.user)
        self.assertEqual(response.json(), self.response.json()['authorizations'])
        self.lg('%s ENDED' % self._testID)
