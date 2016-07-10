from Itsyouonline_testing.jwt_testing.utils import BaseTest


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
        pass
        self.lg('%s ENDED' % self._testID)
