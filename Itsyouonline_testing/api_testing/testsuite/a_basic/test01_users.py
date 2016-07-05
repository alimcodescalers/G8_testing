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

    def test002_get_addresses(self):
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

    def test003_get_emailaddresses(self):
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