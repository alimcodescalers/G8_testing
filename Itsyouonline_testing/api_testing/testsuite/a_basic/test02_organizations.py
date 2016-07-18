from Itsyouonline_testing.api_testing.utils import BaseTest
import types
import uuid


class OrganizationsTests(BaseTest):


    def setUp(self):
        super(OrganizationsTests, self).setUp()
        self.organization_id = str(uuid.uuid4()).replace('-', '')[0:10]
        self.response = self.client.api.CreateNewOrganization(self.organization_id)
        self.assertEqual(self.response.status_code, 200)

    def test001_get_organization(self):
        """ ITSYOU-013
        *Test case for check get organization GET /organizations/{globalid}.*

        **Test Scenario:**

        #. check get organizations, should succeed
        #. validate all expected keys in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client.api.GetOrganization(self.organization_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), types.DictType)
        self.lg('%s ENDED' % self._testID)