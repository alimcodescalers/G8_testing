from Itsyouonline_testing.api_testing.utils import BaseTest


class JWTBasicTests(BaseTest):

    def setUp(self):
        super(JWTBasicTests, self).setUp()
        self.response = self.Client.jwt.GetScope(self.user)

    def test001_get_scope(self):
        """ ITSYOU-001
        *Test case for check get scope /users/{username}.*

        **Test Scenario:**

        #. check get user, should succeed
        #. validate all expected keys in the returned response
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('%s ENDED' % self._testID)