from functional_testing.Itsyouonline.api_testing.utils import BaseTest
import types
import unittest


class OrganizationsTests(BaseTest):


    def setUp(self):
        super(OrganizationsTests, self).setUp()
        response = self.client_1.api.GetUserOrganizations(self.user_1)
        self.lg('GetUserOrganizations [%s] response [%s]' % (self.user_1, response.json()))
        self.assertEqual(response.status_code, 200)
        self.organization_id = response.json()['owner'][-1]
        self.lg('organization_id %s' % self.organization_id)

    #Currently fail due to issue https://github.com/itsyouonline/identityserver/issues/233
    @unittest.skip("fail due to issue https://github.com/itsyouonline/identityserver/issues/233")
    def test001_get_organization(self):
        """ ITSYOU-013
        *Test case for check get organization GET /organizations/{globalid}.*

        **Test Scenario:**

        #. check get organizations, should succeed
        #. validate all expected keys in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client_1.api.GetOrganization(self.organization_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), types.DictType)
        self.lg('%s ENDED' % self._testID)

    def test002_get_organization_tree(self):
        """ ITSYOU-014
        *Test case for check get organization tree GET /organizations/{globalid}/tree.*

        **Test Scenario:**

        #. check get organizations tree, should succeed
        #. validate all expected keys in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client_1.api.GetOrganizationTree(self.organization_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), types.DictType)
        self.lg('%s ENDED' % self._testID)

    #Currently fail due to issue https://github.com/itsyouonline/identityserver/issues/233
    @unittest.skip("fail due to issue https://github.com/itsyouonline/identityserver/issues/233")
    def test003_get_organization_contracts(self):
        """ ITSYOU-015
        *Test case for check get organization contracts GET /organizations/{globalid}/contracts.*

        **Test Scenario:**

        #. check get organizations contracts, should succeed
        #. validate all expected keys in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client_1.api.GetOrganizationContracts(self.organization_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), types.ListType)
        self.lg('%s ENDED' % self._testID)

    #Currently fail due to issue https://github.com/itsyouonline/identityserver/issues/233
    @unittest.skip("fail due to issue https://github.com/itsyouonline/identityserver/issues/233")
    def test004_get_organization_invitations(self):
        """ ITSYOU-016
        *Test case for check get organization invitations GET /organizations/{globalid}/invitations.*

        **Test Scenario:**

        #. check get organizations invitations, should succeed
        #. validate all expected keys in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client_1.api.GetPendingOrganizationInvitations(self.organization_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), types.ListType)
        self.lg('%s ENDED' % self._testID)

    #Currently fail due to issue https://github.com/itsyouonline/identityserver/issues/233
    @unittest.skip("fail due to issue https://github.com/itsyouonline/identityserver/issues/233")
    def test005_get_organization_apikeys(self):
        """ ITSYOU-017
        *Test case for check get organization apikeys GET /organizations/{globalid}/apikeys.*

        **Test Scenario:**

        #. check get organizations apikeys, should succeed
        #. validate all expected keys in the returned response
        """
        self.lg('%s STARTED' % self._testID)
        response = self.client_1.api.GetOrganizationAPIKeyLabels(self.organization_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), types.ListType)
        label = response.json()[0]
        response = self.client_1.api.GetOrganizationAPIKey(label, self.organization_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), types.DictType)
        self.lg('%s ENDED' % self._testID)
