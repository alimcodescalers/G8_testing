from functional_testing.Itsyouonline.api_testing.utils import BaseTest
import types
import unittest
from random import randint
import json
import time

class OrganizationsTestsB(BaseTest):

    def setUp(self):
        super(OrganizationsTestsB, self).setUp()

    @unittest.skip('bug #411')
    def test000_post_organization(self):
        """
            #Test 000]
            - Create new organization -  succeed with 201
            - Get organization by globalid - should succeed with 200
            - Create new organization with unothorized user -  fail with 401
        """
        self.lg('[POST] Create new organization -  succeed with 201')
        globalid = self.random_value()
        data = {"dns":[],
                "globalid":globalid,
                "members":[],
                "owners":[self.user_1],
                "publicKeys":[],
                "secondsvalidity":0,
                "orgowners":[],
                "orgmembers":[],
                "requiredscopes":[]}

        response = self.client_1.api.CreateNewOrganization(data)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get organization by globalid - should succeed with 200')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)

        self.lg('- [POST] Create new organization with unothorized user -  fail with 401')
        globalid = self.random_value()
        data = {"dns":[],
        "globalid":globalid,
        "members":[],
        "owners":[self.user_2],
        "publicKeys":[],
        "secondsvalidity":0,
        "orgowners":[],
        "orgmembers":[],
        "requiredscopes":[]}

        response = self.client_1.api.CreateNewOrganization(data)
        self.assertEqual(response.status_code, 401)

    def test001_get_post_put_delete_organization(self):

        """
            #Test 001
            - Get user organization - should succeed with 200
            - Get user invalid organization - should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('[GET] Get user organization - should succeed with 200')
        response = self.client_1.api.GetOrganization(self.organization_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_1, response.json()['owners'])

        #bug 403 instead of 404
        # self.lg('[GET] Get user invalid organization - should fail with 404')
        # response = self.client_1.api.GetOrganization('fake_organization')
        # self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    def test002_get_post_put_delete_apikey(self):

        """
            #Test 002
            - Add a new apikey for the organization - should succeed with 201
            - Add a new apikey for the organization again - should succeed with 201
            - List organization\'s apikeys - should succeed with 200
            - Get apikey by label - should succeed with 200
            - Add a new apikey with existing label - should fail with 409
            - Update the apikey - should succeed with 201
            - Update the apikey with existing label - should fail with 409
            - Delete  apikey - should succeed with 204
            - Delete  apikey again - should succeed with 204
        """

        self.lg('%s STARTED' % self._testID)

        globalid = self.organization_1

        self.lg('[POST] Add a new apikey - should succeed with 201')
        label = self.random_value()
        callbackURL = self.random_value()
        data = {'label' : label, 'callbackURL':callbackURL}
        response = self.client_1.api.CreateNewOrganizationAPIKey(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Add a new apikey again - should succeed with 201')
        new_label = self.random_value()
        new_callbackURL = self.random_value()
        new_data = {'label' : new_label, 'callbackURL':new_callbackURL}
        response = self.client_1.api.CreateNewOrganizationAPIKey(new_data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] List organization\'s apikeys, should succeed with 200')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(label, response.json())
        self.assertIn(new_label, response.json())

        self.lg('[GET] Get apikeys by label, should succeed with 200')
        response = self.client_1.api.GetOrganizationAPIKey(new_label, globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_label, response.json()['label'])
        self.assertEqual(new_callbackURL, response.json()['callbackURL'])

        self.lg('[POST] Add a new apikey with the same label of the previous apikey, should fail with 409')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        new_label = response.json()[-1]
        new_callbackURL = self.random_value()
        new_data = {'label' : new_label, 'callbackURL':new_callbackURL}
        response = self.client_1.api.CreateNewOrganizationAPIKey(new_data, globalid)
        self.assertEqual(response.status_code, 409)

        #bug bad request require secret
        # self.lg('[PUT] Update the apikey\'s label, should succeed with 201')
        # response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        # self.assertEqual(response.status_code, 200)
        # label = response.json()[-1]
        # print label
        # new_label = self.random_value()
        # new_callbackURL = self.random_value()
        # new_data = {'label' : new_label, 'callbackURL':new_callbackURL}
        # response = self.client_1.api.UpdateOrganizationAPIKey(new_data, label, globalid)
        # self.assertEqual(response.status_code, 201)
        #
        # self.lg('[PUT] Update the apikey\'s label with existing label, should fail with 409')
        # response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        # self.assertEqual(response.status_code, 200)
        # label = response.json()[-1]
        # new_label = response.json()[-2]
        # new_callbackURL = self.random_value()
        # new_data = {'label' : new_label, 'callbackURL':new_callbackURL}
        # response = self.client_1.api.UpdateOrganizationAPIKey(data, label, globalid)
        # self.assertEqual(response.status_code, 409)

        self.lg('[DELETE] Delete valid apikey - should succeed with 204')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]
        response = self.client_1.api.DeleteOrganizationAPIKey(label, globalid)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete valid apikey again - should succeed with 204')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]
        response = self.client_1.api.DeleteOrganizationAPIKey(label, globalid)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


        self.lg('%s ENDED' % self._testID)

    def test003_get_post_put_delete_registry(self):

        """
            #Test 003
            - Register a new registry, should succeed with 201
            - Register a new registry again, should succeed with 201.
            - Get user registries, should succeed with 200
            - Get registry by key, should succeed with 200
            - Get invalid registry, should fail with 404
            - Register a new registry with existing key, should succeed with 201
            - Register a new registry with invalid inputs, should fail with 400
            - Delete registry, should succeed with 204
            - Delete registry again, should succeed with 204
            - Delete invalid registry, should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        globalid = self.organization_1

        self.lg('[POST] Register a new registry - should succeed with 201')
        key = self.random_value()
        value = self.random_value()
        data = {"Key": key,"Value": value}
        response = self.client_1.api.CreateOrganizationRegistry(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new registry again - should succeed with 201')
        key = self.random_value()
        value = self.random_value()
        new_data = {"Key": key,"Value": value}
        response = self.client_1.api.CreateOrganizationRegistry(new_data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get user registries - should succeed with 200')
        response = self.client_1.api.GetOrganizationRegistries(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data, response.json())
        self.assertIn(new_data, response.json())

        self.lg('[GET] Get registry by key - should succeed with 200')
        key = response.json()[-1]['Key']
        response = self.client_1.api.GetOrganizationRegistry(key, globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data, response.json())

        self.lg('[GET] Get invalid registry - should fail with 404')
        response = self.client_1.api.GetOrganizationRegistry('fake_key', globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('[POST] Register a new registry with existing key - should succeed with 201')
        response = self.client_1.api.GetOrganizationRegistries(globalid)
        self.assertEqual(response.status_code, 200)
        key = response.json()[-1]['Key']
        value = self.random_value()
        new_data = {"Key": key,"Value": value}
        response = self.client_1.api.CreateOrganizationRegistry(new_data, globalid)
        self.assertEqual(response.status_code, 201)


        self.lg('[POST] Register a new registry with invalid inputs - should fail with 400')
        key = ''
        value = ''
        new_data = {"Key": key,"Value": value}
        response = self.client_1.api.CreateOrganizationRegistry(new_data, globalid)
        self.assertEqual(response.status_code, 400)

        self.lg('[DELETE] Delete registry - should succeed with 204')
        response = self.client_1.api.GetOrganizationRegistries(globalid)
        self.assertEqual(response.status_code, 200)
        key = response.json()[-1]['Key']
        response = self.client_1.api.DeleteOrganizaitonRegistry(key, globalid)
        self.assertEqual(response.status_code, 204)

        #bug internal server error when deleting last registry
        # self.lg('[DELETE] Delete registry again - should succeed with 204')
        # response = self.client_1.api.GetOrganizationRegistries(globalid)
        # self.assertEqual(response.status_code, 200)
        # key = response.json()[-1]['Key']
        # response = self.client_1.api.DeleteOrganizaitonRegistry(key, globalid)
        # self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete invalid registry - should fail with 404')
        response = self.client_1.api.DeleteOrganizaitonRegistry('fake_key', globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    def test004_get_post_put_delete_dns(self):

        """
            #Test 003
            - Register a new dns name, should succeed with 201
            - Register a new dns name again, should succeed with 201
            - Register a new dns name with name already exists , should fail with 409
            - Get organization dns names, should succeed with 200
            - Register a new dns name with invalid name , should fail with 400
            - Update organization dns name, should succeed with 201
            - Update organization dns name with name already exists, should fail with 409
            - Update nonexisting organization dns name, should fail with 404
            - Update organization dns name with invalid name, should fail with 400
            - Delete dns name, should succeed with 204
            - Delete dns name again, should succeed with 204
            - Delete invalid dns name, should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        globalid = self.organization_1

        self.lg('[POST] Register a new dns name, should succeed with 201')
        name = "www.abc.com"
        data = {"name":name}
        print data
        response = self.client_1.api.CreateOrganizationDNS(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new dns name again, should succeed with 201')
        name = "www.xyz.com"
        new_data = {"name": name}
        response = self.client_1.api.CreateOrganizationDNS(new_data, globalid)
        self.assertEqual(response.status_code, 201)

        # #bug
        # self.lg('[POST] Register a new dns name with name already exists , should fail with 409')
        # name = "www.abc.com"
        # new_data = {"name": name}
        # response = self.client_1.api.CreateOrganizationDNS(new_data, globalid)
        # self.assertEqual(response.status_code, 409)

        self.lg('[GET] Get organization dns names, should succeed with 200')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data['name'], response.json()['dns'])
        self.assertIn(new_data['name'], response.json()['dns'])

        self.lg('[POST] Register a new dns name with invalid name , should fail with 400')
        name = self.random_value()
        new_data = {"name": name}
        response = self.client_1.api.CreateOrganizationDNS(new_data, globalid)
        self.assertEqual(response.status_code, 400)

        self.lg('[PUT] Update organization dns name, should succeed with 201')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        dnsname = response.json()['dns'][-1]
        new_dnsname = "www.mno.com"
        new_data = {"name":new_dnsname}
        response = self.client_1.api.UpdateOrganizationDNS(new_data, dnsname, globalid)
        self.assertEqual(response.status_code, 201)

        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)

        self.assertIn(new_dnsname, response.json()['dns'])
        self.assertNotIn(dnsname, response.json()['dns'])

        # #bug
        # self.lg('[PUT] Update organization dns name with name already exists, should fail with 409')
        # response = self.client_1.api.GetOrganization(globalid)
        # self.assertEqual(response.status_code, 200)
        # dnsname = response.json()['dns'][-1]
        # new_dnsname = response.json()['dns'][-2]
        # new_data = {"name":new_dnsname}
        # response = self.client_1.api.UpdateOrganizationDNS(new_data, dnsname, globalid)
        # self.assertEqual(response.status_code, 409)

        self.lg('[PUT] Update organization dns name with invalid name, should fail with 400')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        dnsname = response.json()['dns'][-1]
        new_dnsname = self.random_value()
        new_data = {"name":new_dnsname}
        response = self.client_1.api.UpdateOrganizationDNS(new_data, dnsname, globalid)
        self.assertEqual(response.status_code, 400)

        ## bug
        # self.lg('[PUT] Update nonexisting organization dns name, should fail with 404')
        # new_data = {"name":"www.qwe.com"}
        # response = self.client_1.api.UpdateOrganizationDNS(new_data, 'fakse_dnsname', globalid)
        # self.assertEqual(response.status_code, 404)

        self.lg('[DELETE] Delete dns name, should succeed with 204')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        dnsname = response.json()['dns'][-1]
        response = self.client_1.api.DeleteOrganizaitonDNS(dnsname, globalid)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete dns name again, should succeed with 204')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        dnsname = response.json()['dns'][-1]
        response = self.client_1.api.DeleteOrganizaitonDNS(dnsname, globalid)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['dns'], [])

        self.lg('[DELETE] Delete invalid dns name, should fail with 404')
        response = self.client_1.api.DeleteOrganizaitonDNS('fake_dns', globalid)
        self.assertEqual(response.status_code, 404)


        self.lg('%s ENDED' % self._testID)

    def test005_get_delete_invitation(self):

        """
            #Test 005
            - Send invitation to user_2 to join org_1 role owner, should succeed with 201
            - Get pending invitations, should succeed with 200
            - Check user_2 invitations, should succeed with 200
            - Cancel a pending invitation for user_2 to join org_1, should succeed with 201
            - Check pendings invitations, should succeed with 200
            - Check user_2 invitations, should succeed with 200
            - Send invitation to user_2 to join org_1 role member, should succeed with 201
            - Get pending invitations, should succeed with 200
            - Check user_2 invitations, should succeed with 200
            - Cancel a pending invitation for user_2 to join org_1, should succeed with 201
            - Check pendings invitations, should succeed with 200
            - Check user_2 invitations, should succeed with 200
        """

        self.lg('%s STARTED' % self._testID)

        globalid = self.organization_1
        for role in ['member', 'owner']:
            self.lg('Send invitation to user_2 to join org_1 role %s , should succeed with 201' % role)
            data = {'searchstring': self.user_2}
            if role =="member":
                response = self.client_1.api.AddOrganizationMember(data, globalid)
            elif role == "owner":
                response = self.client_1.api.AddOrganizationOwner(data, globalid)
            self.assertEqual(response.status_code, 201)

            self.lg('Check pendings invitations, should succeed with 200')
            response = self.client_1.api.GetPendingOrganizationInvitations(globalid)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()[-1]['status'], 'pending')
            self.assertEqual(response.json()[-1]['organization'], globalid)
            self.assertEqual(response.json()[-1]['user'], self.user_2)
            self.assertEqual(response.json()[-1]['role'], role)

            self.lg('Check user_2 invitations, should succeed with 200')
            response = self.client_2.api.GetNotifications(self.user_2)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.organization_1, response.json()['invitations'][-1]['organization'])
            self.assertEqual(role, response.json()['invitations'][-1]['role'])
            self.assertEqual('pending', response.json()['invitations'][-1]['status'])

            self.lg('Cancel a pending invitation for user_2 to join org_1 role %s , should succeed with 201' % role)
            response = self.client_1.api.RemovePendingOrganizationInvitation(self.user_2, globalid)
            self.assertEqual(response.status_code, 204)

            self.lg('Check pendings invitations, should succeed with 200')
            response = self.client_1.api.GetPendingOrganizationInvitations(globalid)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), [])

            self.lg('Check user_2 invitations, should succeed with 200')
            response = self.client_2.api.GetNotifications(self.user_2)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['invitations'], [])

        self.lg('%s ENDED' % self._testID)

    def test006_get_post_put_delete_description(self):
        """
            #Test 006
            - Add new description with langkey en, should succeed with 201
            - Get description by langkey, should succeed with 200
            - Add new description with random langkey, should succeed with 201
            - Update description, should succeed with 200
            - Delete description, should succeed with 204
            - Get description withfallback, should succeed with 200
        """
        self.lg('%s STARTED' % self._testID)

        globalid = self.organization_1

        self.lg('Add new description with langkey en, should succeed with 201')
        text = self.random_value()
        langkey = 'en'
        data = {"langkey": langkey, "text": text}
        response = self.client_1.api.AddOrganizationDescription(data, globalid)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)

        self.lg('Get description by langkey, should succeed with 200')
        langkey = 'en'
        response = self.client_1.api.GetOrganizationDescription(langkey, globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['langkey'], langkey)

        self.lg('Add new description with random langkey, should succeed with 201')
        text = self.random_value()
        new_langkey = self.random_value(2)
        new_data = {"langkey": new_langkey, "text": text}
        response = self.client_1.api.AddOrganizationDescription(new_data, globalid)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), new_data)

        self.lg('Update description, should succeed with 200')
        text = self.random_value()
        new_data = {"langkey": new_langkey, "text": text}
        response = self.client_1.api.UpdateOrganizationDescription(new_data, globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), new_data)

        self.lg('Delete description, should succeed with 204')
        response = self.client_1.api.DeleteOrganizationDescription(new_langkey, globalid)
        self.assertEqual(response.status_code, 204)

        self.lg('Get description withfallback, should succeed with 200')
        response = self.client_1.api.GetOrganizationDescriptionWithfallback(new_langkey, globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['langkey'], 'en')












        self.lg('%s ENDED' % self._testID)
