from functional_testing.Itsyouonline.api_testing.utils import BaseTest
import types
import unittest
from random import randint
import json
import time

class OrganizationsTestsB(BaseTest):

    def setUp(self):
        super(OrganizationsTestsB, self).setUp()

        self.org_11_globalid = self.random_value()
        self.org_12_globalid = self.random_value()
        self.org_21_globalid = self.random_value()
        self.org_22_globalid = self.random_value()

        #### org-11 user_1 owner
        org_11_data = {"globalid":self.org_11_globalid}
        response = self.client_1.api.CreateNewOrganization(org_11_data)
        self.assertEqual(response.status_code, 201)
        #### org-12 user_1 owner & user_2 member
        org_12_data = {"globalid":self.org_12_globalid}
        response = self.client_1.api.CreateNewOrganization(org_12_data)
        self.assertEqual(response.status_code, 201)
        ## user_1 invite user_2
        data = {'searchstring': self.user_2}
        response = self.client_1.api.AddOrganizationMember(data, self.org_12_globalid)
        self.assertEqual(response.status_code, 201)
        ## user_2 accept invitation
        response = self.client_2.api.AcceptMembership(self.org_12_globalid , 'member', self.user_2)
        self.assertEqual(response.status_code, 201)
        #### org-21 user_2 owner
        org_21_data = {"globalid":self.org_21_globalid}
        response = self.client_2.api.CreateNewOrganization(org_21_data)
        self.assertEqual(response.status_code, 201)
        #### org-22 user_2 owner & user_1 member
        org_22_data = {"globalid":self.org_22_globalid}
        response = self.client_2.api.CreateNewOrganization(org_22_data)
        self.assertEqual(response.status_code, 201)
        ## user_1 invite user_2
        data = {'searchstring': self.user_1}
        response = self.client_2.api.AddOrganizationMember(data, self.org_22_globalid)
        self.assertEqual(response.status_code, 201)
        ## user_2 accept invitation
        response = self.client_1.api.AcceptMembership(self.org_22_globalid , 'member', self.user_1)
        self.assertEqual(response.status_code, 201)

    def test000_post_organization(self):
        """
            #Test 000_post_organization
            - Create new organization, succeed with 201
            - Create new organization with globalid already exists, should fail with 409
            - Get organization by globalid, should succeed with 200
            - Delete organization, should succeed with 204
        """
        self.lg('[POST] Create new organization, succeed with 201')

        globalid = self.random_value()
        data = {"globalid":globalid}
        response = self.client_1.api.CreateNewOrganization(data)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Create new organization with globalid already exists,  succeed with 409')
        response = self.client_1.api.CreateNewOrganization(data)
        self.assertEqual(response.status_code, 409)

        self.lg('[GET] Get organization by globalid, should succeed with 200')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(globalid, response.json()['globalid'])
        self.assertEqual([self.user_1], response.json()['owners'])

        self.lg('[GET] Delte organization by globalid, should succeed with 204')
        response = self.client_1.api.DeleteOrganization(globalid)
        self.assertEqual(response.status_code, 204)

    @unittest.skip('bug: #442 #447 #448 #450')
    def test001_get_post_put_delete_organization(self):

        """
            #Test 001_get_post_put_delete_organization
            - Create new organization, should succeed with 201
            - Get organization, should succeed with 200
            - Get invalid organization, should fail with 404
            - Create suborganization (1), should succeed with 201
            - Get organization tree, should succeed with 200
            - Create suborganization with globalid already exists (globalid of suborganization(1)), should succeed with 409
            - Update organization globalid, should fail with 403
            - Update organization info, should succeed with 201
            - Delete suborganization, should succeed with 204
            - Delete organization, should succeed with 204
            - Delete nonexisting organization, should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        globalid = self.random_value()

        self.lg('[POST] Create new organization, should succeed with 201')
        data = {"globalid":globalid}
        response = self.client_1.api.CreateNewOrganization(data)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get organization - should succeed with 200')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_1, response.json()['owners'])

        #bug #442
        self.lg('[GET] Get invalid organization - should fail with 404')
        response = self.client_1.api.GetOrganization('fake_organization')
        self.assertEqual(response.status_code, 404)

        self.lg('[POST] Create suborganization, should succeed with 201')
        sub_org_1_globalid = globalid+'.'+self.random_value()
        sub_org_1_data = {"globalid":sub_org_1_globalid}
        response = self.client_1.api.CreateNewSubOrganization(sub_org_1_data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get organization org-11 tree, should succeed with 200')
        response = self.client_1.api.GetOrganizationTree(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(globalid, response.json()['globalid'])
        self.assertIn(sub_org_1_globalid, [x['globalid'] for x in response.json()['children']])

        self.lg('[POST] Create suborganization with globalid already exists (globalid of suborganization(1)), should succeed with 409')
        response = self.client_1.api.CreateNewSubOrganization(sub_org_1_data, globalid)
        self.assertEqual(response.status_code, 409)

        self.lg('[PUT] Update organization globalid, should fail with 403')
        sub_org_1_data_new = {"globalid": self.random_value()}
        response = self.client_1.api.UpdateOrganization(sub_org_1_data_new, globalid)
        self.assertEqual(response.status_code, 403)

        #bug #450
        self.lg('[PUT] Update organization info, should succeed with 201')
        data_new = {"globalid":globalid, "dns":["www.a.com"]}
        response = self.client_1.api.UpdateOrganization(data_new, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[DEL] Delete suborganization, should succedd with 204')
        response = self.client_1.api.DeleteOrganization(sub_org_1_globalid)
        self.assertEqual(response.status_code, 204)

        self.lg('[DEL] Delete organization, should succedd with 204')
        response = self.client_1.api.DeleteOrganization(globalid)
        self.assertEqual(response.status_code, 204)

        #bug #448
        self.lg('[DEL] Delete nonexisting organization, should fail with 404')
        response = self.client_1.api.DeleteOrganization('fake_organization')
        self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('#453')
    def test002_get_post_put_delete_apikey(self):

        """
            #Test 002_get_post_put_delete_apikey
            - Register a new apikey (1), should succeed with 201
            - Register a new apikey (2), should succeed with 201
            - Get organization\'s apikeys, should succeed with 200
            - Get apikey (2) by label, should succeed with 200
            - Get nonexisting apikey, should fail with 404
            - Register new apikey with label already exists (label of apikey (2)), should fail with 409
            - Update the apikey (2), should succeed with 201
            - Update the apikey (2) with label already exists (label of apikey (1)), should fail with 409
            - Delete apikey (1), should succeed with 204
            - Delete apikey (2), should succeed with 204
        """

        self.lg('%s STARTED' % self._testID)

        globalid = self.org_11_globalid

        self.lg('[POST] Register a new apikey (1), should succeed with 201')
        label = self.random_value()
        callbackURL = self.random_value()
        data = {'label' : label, 'callbackURL':callbackURL}
        response = self.client_1.api.CreateNewOrganizationAPIKey(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new apikey (2), should succeed with 201')
        new_label = self.random_value()
        new_callbackURL = self.random_value()
        new_data = {'label' : new_label, 'callbackURL':new_callbackURL}
        response = self.client_1.api.CreateNewOrganizationAPIKey(new_data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get organization\'s apikeys, should succeed with 200')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(label, response.json())
        self.assertIn(new_label, response.json())

        self.lg('[GET] Get apikey (2) by label, should succeed with 200')
        response = self.client_1.api.GetOrganizationAPIKey(new_label, globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_label, response.json()['label'])
        self.assertEqual(new_callbackURL, response.json()['callbackURL'])

        self.lg('[GET] - Get nonexisting apikey, should fail with 404')
        response = self.client_1.api.GetOrganizationAPIKey('fake_label', globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('[POST] Register new apikey with label already exists (label of apikey (2)), should fail with 409')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        new_label = response.json()[-1]
        new_callbackURL = self.random_value()
        new_data = {'label' : new_label, 'callbackURL':new_callbackURL}
        response = self.client_1.api.CreateNewOrganizationAPIKey(new_data, globalid)
        self.assertEqual(response.status_code, 409)

        #bug 453 bad request require secret
        self.lg('[PUT] Update the apikey (2), should succeed with 201')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]
        print label
        new_label = self.random_value()
        new_callbackURL = self.random_value()
        new_data = {'label' : new_label, 'callbackURL':new_callbackURL}
        response = self.client_1.api.UpdateOrganizationAPIKey(new_data, label, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[PUT] Update the apikey (2) with label already exists (label of apikey (1)), should fail with 409')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]
        new_label = response.json()[-2]
        new_callbackURL = self.random_value()
        new_data = {'label' : new_label, 'callbackURL':new_callbackURL}
        response = self.client_1.api.UpdateOrganizationAPIKey(new_data, label, globalid)
        self.assertEqual(response.status_code, 409)

        self.lg('[DELETE] Delete apikey (1), should succeed with 204')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]
        response = self.client_1.api.DeleteOrganizationAPIKey(label, globalid)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete apikey (2), should succeed with 204')
        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]
        response = self.client_1.api.DeleteOrganizationAPIKey(label, globalid)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetOrganizationAPIKeyLabels(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('bug: #443')
    def test003_get_post_put_delete_registry(self):

        """
            #Test 003_get_post_put_delete_registry
            - Register a new registry (1), should succeed with 201
            - Register a new registry (2), should succeed with 201.
            - Get user registries, should succeed with 200
            - Get registry (2) by key, should succeed with 200
            - Get nonexisting registry, should fail with 404
            - Register a new registry with key already exists (key of registry (2)), should succeed with 201
            - Register a new registry with invalid inputs, should fail with 400
            - Delete registry, should succeed with 204
            - Delete registry again, should succeed with 204
            - Delete nonexisting registry, should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        globalid = self.org_11_globalid

        self.lg('[POST] Register a new registry (1) - should succeed with 201')
        key = self.random_value()
        value = self.random_value()
        data = {"Key":key,"Value":value}
        print  data
        response = self.client_1.api.CreateOrganizationRegistry(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new registry (2) - should succeed with 201')
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

        self.lg('[GET] Get registry (2) by key - should succeed with 200')
        key = response.json()[-1]['Key']
        response = self.client_1.api.GetOrganizationRegistry(key, globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data, response.json())

        self.lg('[GET] Get nonexisting registry - should fail with 404')
        response = self.client_1.api.GetOrganizationRegistry('fake_key', globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('[POST] Register a new registry with key already exists (key of registry (2)), should succeed with 201')
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

        self.lg('[DELETE] Delete registry (2) - should succeed with 204')
        response = self.client_1.api.GetOrganizationRegistries(globalid)
        self.assertEqual(response.status_code, 200)
        key = response.json()[-1]['Key']
        response = self.client_1.api.DeleteOrganizaitonRegistry(key, globalid)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete registry (1) - should succeed with 204')
        response = self.client_1.api.GetOrganizationRegistries(globalid)
        self.assertEqual(response.status_code, 200)
        key = response.json()[-1]['Key']
        response = self.client_1.api.DeleteOrganizaitonRegistry(key, globalid)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete nonexisting registry - should fail with 404')
        response = self.client_1.api.DeleteOrganizaitonRegistry('fake_key', globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('bug: #441 #444')
    def test004_get_post_put_delete_dns(self):

        """
            #Test 004_get_post_put_delete_dns
            - Register a new dns name (1), should succeed with 201
            - Register a new dns name (2), should succeed with 201
            - Register a new dns name with name already exists (name of dns (1)), should fail with 409
            - Get organization dns names, should succeed with 200
            - Register a new dns name with invalid name, should fail with 400
            - Update organization dns name (2), should succeed with 201
            - Update organization dns name (2) with name already exists (name of dns (1)), should fail with 409
            - Update organization dns name with invalid name, should fail with 400
            - Update nonexisting organization dns name, should fail with 404
            - Delete dns name (2), should succeed with 204
            - Delete dns name (1), should succeed with 204
            - Delete invalid dns name, should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        globalid = self.org_11_globalid

        self.lg('[POST] Register a new dns name (1), should succeed with 201')
        name = "www.abc.com"
        data = {"name":name}
        print data
        response = self.client_1.api.CreateOrganizationDNS(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new dns name (2), should succeed with 201')
        name = "www.xyz.com"
        new_data = {"name": name}
        response = self.client_1.api.CreateOrganizationDNS(new_data, globalid)
        self.assertEqual(response.status_code, 201)

        #bug #441
        self.lg('[POST] Register a new dns name with name already exists (name of dns (1)) , should fail with 409')
        name = "www.abc.com"
        new_data = {"name": name}
        response = self.client_1.api.CreateOrganizationDNS(new_data, globalid)
        self.assertEqual(response.status_code, 409)

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

        self.lg('[PUT] Update organization dns name (2), should succeed with 201')
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

        #bug #441
        self.lg('[PUT] Update organization dns name (2) with name already exists (name of dns (1)), should fail with 409')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        dnsname = response.json()['dns'][-1]
        new_dnsname = response.json()['dns'][-2]
        new_data = {"name":new_dnsname}
        response = self.client_1.api.UpdateOrganizationDNS(new_data, dnsname, globalid)
        self.assertEqual(response.status_code, 409)

        self.lg('[PUT] Update organization dns name with invalid name, should fail with 400')
        response = self.client_1.api.GetOrganization(globalid)
        self.assertEqual(response.status_code, 200)
        dnsname = response.json()['dns'][-1]
        new_dnsname = self.random_value()
        new_data = {"name":new_dnsname}
        response = self.client_1.api.UpdateOrganizationDNS(new_data, dnsname, globalid)
        self.assertEqual(response.status_code, 400)

        # bug #444
        self.lg('[PUT] Update nonexisting organization dns name, should fail with 404')
        new_data = {"name":"www.qwe.com"}
        response = self.client_1.api.UpdateOrganizationDNS(new_data, 'fakse_dnsname', globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('[DELETE] Delete dns name(1), should succeed with 204')
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
            #Test 005_get_delete_invitation
            * Same steps for member and owner roles
            - User_1 invite user_2 to join org_11, should succeed with 201
            - Get org-11 pending invitations, should succeed with 200
            - Check user_2 invitations, should succeed with 200
            - Cancel org-11 pending invitation for user_2 to join org_11, should succeed with 201
            - Check org-11 pendings invitations, should succeed with 200
            - Check user_2 invitations, should succeed with 200
        """

        self.lg('%s STARTED' % self._testID)

        globalid = self.org_11_globalid

        for role in ['member', 'owner']:

            self.lg('User_1 invite user_2 to join org_11 role %s , should succeed with 201' % role)
            data = {'searchstring': self.user_2}
            if role =="member":
                response = self.client_1.api.AddOrganizationMember(data, globalid)
            elif role == "owner":
                response = self.client_1.api.AddOrganizationOwner(data, globalid)
            self.assertEqual(response.status_code, 201)

            self.lg('Get org-11 pending invitations, should succeed with 200')
            response = self.client_1.api.GetPendingOrganizationInvitations(globalid)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()[-1]['status'], 'pending')
            self.assertEqual(response.json()[-1]['organization'], globalid)
            self.assertEqual(response.json()[-1]['user'], self.user_2)
            self.assertEqual(response.json()[-1]['role'], role)

            self.lg('Check user_2 invitations, should succeed with 200')
            response = self.client_2.api.GetNotifications(self.user_2)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.org_11_globalid, response.json()['invitations'][-1]['organization'])
            self.assertEqual(role, response.json()['invitations'][-1]['role'])
            self.assertEqual('pending', response.json()['invitations'][-1]['status'])

            self.lg('Cancel org-11 pending invitation for user_2 to join org_11 role %s , should succeed with 201' % role)
            response = self.client_1.api.RemovePendingOrganizationInvitation(self.user_2, globalid)
            self.assertEqual(response.status_code, 204)

            self.lg('Check org-11 pendings invitations, should succeed with 200')
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
            #Test 006_get_post_put_delete_description
            - Add new description with langkey en, should succeed with 201
            - Get description by langkey, should succeed with 200
            - Add new description with random langkey, should succeed with 201
            - Update description, should succeed with 200
            - Delete description, should succeed with 204
            - Get description withfallback, should succeed with 200
        """
        self.lg('%s STARTED' % self._testID)

        globalid = self.org_11_globalid

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

    @unittest.skip('bug: #440 #452')
    def test007_get_post_twofa(self):
        """
            #Test 007_get_post_twofa
            - Update 2fa with owner user, should succeed with 200
            - Update 2fa with invalid value, should fail with 400
            - Update 2fa with member user, should fail with 403
            - Get 2fa, should succeed with 200
            - Get 2fa of nonexisting organization , should fail with 400
            - Update 2fa of nonexisting organization, should fail with 404
        """
        self.lg('%s STARTED' % self._testID)

        globalid = self.org_12_globalid

        self.lg('[POST] Update 2fa with owner user, should succeed with 200')
        secondsvalidity = 2000
        data = {"secondsvalidity":secondsvalidity}
        response = self.client_1.api.UpdateTwoFA(data, globalid)
        self.assertEqual(response.status_code, 200)

        self.lg('[POST] Update 2fa with owner user, should succeed with 200')
        secondsvalidity = self.random_value()
        data = {"secondsvalidity":secondsvalidity}
        response = self.client_1.api.UpdateTwoFA(data, globalid)
        self.assertEqual(response.status_code, 400)

        self.lg('[POST] Update 2fa with member user, should fail with 403')
        secondsvalidity = 2000
        data = {"secondsvalidity":secondsvalidity}
        response = self.client_2.api.UpdateTwoFA(data, globalid)
        self.assertEqual(response.status_code, 403)

        self.lg('[GET] Get 2fa, should succeed with 200')
        response = response = self.client_1.api.GetTwoFA(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['secondsvalidity'], secondsvalidity)

        #bug #440 (internal server error)
        self.lg('[GET] Get 2fa of nonexisting organization , should fail with 400')
        response = self.client_1.api.GetTwoFA('fake_globalid')
        self.assertEqual(response.status_code, 404)

        ##bug #452 (403 instead of 404 put not post)
        self.lg('[POST] Update 2fa of nonexisting organization, should fail with 404')
        secondsvalidity = 2000
        data = {"secondsvalidity":secondsvalidity}
        response = self.client_2.api.UpdateTwoFA(data, 'fake_globalid')
        self.assertEqual(response.status_code, 404)

    def test008_post_put_delete_orgmembers(self):

        """
            #Test 008_post_put_delete_orgmembers
            - Add org-12 to org-11 orgmembers, should succeed with 201
            - Add org-12 to org-11 orgmembers again, should fail with 409
            - Add org-22 org-11 orgmembers, should fail with 403
            - Add nonexisting to org-11 orgmembers, should fail with 404
            - Update org-12 from orgmember to orgowner of org-11, should succeed with 200
            - Update org-12 from orgowner to orgmember of org-11, should succeed with 200
            - Update org-22 organizations membership, should fail with 403
            - Update nonexisting organizations membership, should fail with 404
            - Remove org-12 as orgmember of org-11, should succeed with 204
            - Remove nonexisting organization as orgmember of org-11, should fail with 404
        """

        self.lg('[POST] Add org-12 to org-11 orgmembers, should succeed with 201')
        data = {"orgmember":self.org_12_globalid}
        response = self.client_1.api.SetOrgMember(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 201)

        response = self.client_1.api.GetOrganization(self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.org_12_globalid, response.json()['orgmembers'])

        self.lg('[POST] Add org-12 to org-11 orgmembers again, should fail with 409')
        data = {"orgmember":self.org_12_globalid}
        response = self.client_1.api.SetOrgMember(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 409)

        self.lg('[POST] Add org-22 org-11 orgmembers, should fail with 403')
        data = {"orgmember":self.org_22_globalid}
        response = self.client_1.api.SetOrgMember(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 403)

        self.lg('[POST] Add nonexisting to org-11 orgmembers, should fail with 404')
        data = {"orgmember":'fake_org'}
        response = self.client_1.api.SetOrgMember(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('[PUT] Update org-12 from orgmember to orgowner of org-11, should succeed with 200')
        data = {"org":self.org_12_globalid, "role":"owners"}
        response = self.client_1.api.UpdateOrganizationOrgMemberShip(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.org_12_globalid, response.json()['orgowners'])

        self.lg('[PUT] Update org-12 from orgowner to orgmember of org-11, should succeed with 200')
        data = {"org":self.org_12_globalid, "role":"members"}
        response = self.client_1.api.UpdateOrganizationOrgMemberShip(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.org_12_globalid, response.json()['orgmembers'])

        self.lg('[PUT] Update org-22 organizations membership, should fail with 403')
        data = {"org":self.org_22_globalid, "role":"members"}
        response = self.client_1.api.UpdateOrganizationOrgMemberShip(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 403)

        self.lg('[PUT] Update nonexisting organizations membership, should fail with 404')
        data = {"org":"fake_org", "role":"members"}
        response = self.client_1.api.UpdateOrganizationOrgMemberShip(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('[DEL] Remove org-12 as orgmember of org-11, should succeed with 204')
        response = self.client_1.api.DeleteOrgMember(self.org_12_globalid, self.org_11_globalid)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetOrganization(self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.org_12_globalid, response.json()['orgmembers'])

        self.lg('[DEL] Remove nonexisting organization as orgmember of org-11, should fail with 404')
        response = self.client_1.api.DeleteOrgMember('fake_org', self.org_11_globalid)
        self.assertEqual(response.status_code, 404)

    def test009_post_delete_orgowners(self):

        """
            #Test 009_post_delete_orgowners
            - Add org-12 to org-11 orgowners, should succeed with 201
            - Add org-12 to org-11 orgowners again, should fail with 409
            - Add org-22 org-11 orgmembers, should fail with 403
            - Add nonexisting to org-11 orgowners, should fail with 404
            - Remove org-12 as orgowners of org-11, should succeed with 204
            - Remove nonexisting organization as orgowners of org-11, should fail with 404
        """

        self.lg('[POST] Add org-12 to org-11 orgowner, should succeed with 201')
        data = {"orgowner":self.org_12_globalid}
        response = self.client_1.api.SetOrgOwner(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 201)

        response = self.client_1.api.GetOrganization(self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.org_12_globalid, response.json()['orgowners'])

        self.lg('[POST] Add org-12 to org-11 orgowner again, should fail with 409')
        data = {"orgowner":self.org_12_globalid}
        response = self.client_1.api.SetOrgOwner(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 409)

        self.lg('[POST] Add org-22 org-11 orgowner, should fail with 403')
        data = {"orgowner":self.org_22_globalid}
        response = self.client_1.api.SetOrgOwner(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 403)

        self.lg('[POST] Add nonexisting to org-11 orgowner, should fail with 404')
        data = {"orgowner":'fake_org'}
        response = self.client_1.api.SetOrgOwner(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('[DEL] Remove org-12 as orgowner of org-11, should succeed with 204')
        response = self.client_1.api.DeleteOrgOwner(self.org_12_globalid, self.org_11_globalid)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetOrganization(self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.org_12_globalid, response.json()['orgowners'])

        self.lg('[DEL] Remove nonexisting organization as orgowner of org-11, should fail with 404')
        response = self.client_1.api.DeleteOrgOwner('fake_org', self.org_11_globalid)
        self.assertEqual(response.status_code, 404)

    @unittest.skip('bug: #454')
    def test010_post_put_delete_members(self):

        """
            #Test 010_post_put_delete_members
            - User_1 invite user_2 to be a member of org-11, should succeed with 201
            - User_2 accept the invitations, should succeed with 201
            - User_1 invite user_2 to be a member of org-11 again, should fail with 409
            - User_1 update user_2 role to be an owner of org-11, should succeed with 200
            - User_1 update user_2 role to be a member, should succeed with 200
            - User_1 update nonexisting user\'s role , should fail with 404
            - User_1 Delete user_2 from org-11, should succeed with 204
            - User_1 Delete nonexisting user from org-11, should fail with 404
        """

        self.lg('[POST] User_1 invite user_2 to be a member of org-11, should succeed with 201')
        data = {"searchstring":self.user_2}
        response = self.client_1.api.AddOrganizationMember(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] User_2 accept the invitations, should succeed with 201')
        response = self.client_2.api.AcceptMembership(self.org_11_globalid, 'member', self.user_2)
        self.assertEqual(response.status_code, 201)

        response = self.client_2.api.GetOrganization(self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_2, response.json()['members'])

        self.lg('[POST] User_1 invite user_2 to be a member of org-11 again, should succeed with 201')
        data = {"searchstring":self.user_2}
        response = self.client_1.api.AddOrganizationMember(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 409)

        self.lg('[PUT] User_1 update user_2 role to be an owner of org-11, should succeed with 200')
        data = {"username":self.user_2, "role":"owners"}
        response = self.client_1.api.UpdateOrganizationMemberShip(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 200)

        response = self.client_1.api.GetOrganization(self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_2, response.json()['owners'])

        self.lg('[PUT] User_1 update user_2 role to be a member, should succeed with 200')
        data = {"username":self.user_2, "role":"members"}
        response = self.client_1.api.UpdateOrganizationMemberShip(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 200)

        response = self.client_1.api.GetOrganization(self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_2, response.json()['members'])

        #bug #454 internal server error
        self.lg('[PUT] User_1 update nonexisting user\'s role , should fail with 404')
        data = {"username":"fake_user", "role":"owners"}
        response = self.client_1.api.UpdateOrganizationMemberShip(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 404)

        self.lg('[DEL] User_1 Delete user_2 from org-11, should succeed with 204')
        response = self.client_1.api.RemoveOrganizationMember(self.user_2, self.org_11_globalid)
        self.assertEqual(response.status_code, 204)

        self.lg('[DEL] User_1 Delete nonexisting user from org-11, should fail with 404')
        response = self.client_1.api.RemoveOrganizationMember(self.user_1, self.org_11_globalid)
        self.assertEqual(response.status_code, 204)

    def test011_post_put_delete_owners(self):

        """
            #Test 011_post_put_delete_owners
            - User_1 invite user_2 to be an owner of org-11, should succeed with 201
            - User_2 accept the invitations, should succeed with 201
            - User_1 invite user_2 to be an owner of org-11 again, should fail with 409
            - User_1 Delete user_2 from org-11, should succeed with 204
            - User_1 Delete nonexisting user from org-11, should fail with 404
        """

        self.lg('[POST] User_1 invite user_2 to be an owner of org-11, should succeed with 201')
        data = {"searchstring":self.user_2}
        response = self.client_1.api.AddOrganizationOwner(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] User_2 accept the invitations, should succeed with 201')
        response = self.client_2.api.AcceptMembership(self.org_11_globalid, 'owner', self.user_2)
        self.assertEqual(response.status_code, 201)

        response = self.client_2.api.GetOrganization(self.org_11_globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_2, response.json()['owners'])

        self.lg('[POST] User_1 invite user_2 to be an owner of org-11 again, should succeed with 201')
        data = {"searchstring":self.user_2}
        response = self.client_1.api.AddOrganizationOwner(data, self.org_11_globalid)
        self.assertEqual(response.status_code, 409)

        self.lg('[DEL] User_1 Delete user_2 from org-11, should succeed with 204')
        response = self.client_1.api.RemoveOrganizationMember(self.user_2, self.org_11_globalid)
        self.assertEqual(response.status_code, 204)

        self.lg('[DEL] User_1 Delete nonexisting user from org-11, should fail with 404')
        response = self.client_1.api.RemoveOrganizationMember(self.user_1, self.org_11_globalid)
        self.assertEqual(response.status_code, 204)

    @unittest.skip('bug: #439')
    def test012_get_put_delete_logo(self):
        """
            #Test 012_get_put_delete_logo
            - Get organization logo, should succeed with 200
            - Update organization logo, should succeed with 200
            - Update organization logo with large file, should fail with 413
            - Remove organization logo, should succeed with 204
            - Remove nonexisting organization logo, should fail with 404
        """
        globalid = self.org_11_globalid

        self.lg('[GET] Get organization logo, should succeed with 200')
        response = self.client_1.api.GetOrganizationLogo(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['logo'], "")

        self.lg('[PUT] Update organization logo, should succeed with 200')
        logo = 'data:image/png;base64,' + self.random_value(1024)
        data = {"logo":logo}
        response = self.client_1.api.SetOrganizationLogo(data, globalid)
        self.assertEqual(response.status_code, 200)

        response = self.client_1.api.GetOrganizationLogo(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['logo'], logo)

        self.lg('[PUT] Update organization logo with large file, should fail with 413')
        large_logo = 'data:image/png;base64,' + self.random_value(1024*1024*6)
        data = {"logo":large_logo}
        response = self.client_1.api.SetOrganizationLogo(data, globalid)
        self.assertEqual(response.status_code, 413)

        self.lg('[DEL] Remove organization logo, should succeed with 204')
        response = self.client_1.api.DeleteOrganizationLogo(globalid)
        self.assertEqual(response.status_code, 204)

        #bug #439 (403 instead of 404)
        self.lg('[DEL] Remove nonexisting organization logo, should fail with 404')
        response = self.client_1.api.DeleteOrganizationLogo('fake_globalid')
        self.assertEqual(response.status_code, 404)

    @unittest.skip('bug: #445')
    def test013_get_post_contracts(self):
        """
            #Test 013_get_post_contracts
            - Create a new contract (1), should succeed with 201
            - Create a new contract (2), should succeed with 201
            - Create a new expired contract (3), should succeed with 201
            - Get organization\'s contracts, should succeed with 200
            - Get organization\'s contracts & include the expired contracts, should succeed with 200
            - Get organization\'s contracts with page size 1, should succeed with 200
            - Get organization\'s contracts with start page 2, should succeed with 200
        """

        globalid = self.org_11_globalid

        #bud #445
        self.lg('Create a new contract (1), should succeed with 201')
        contractid_1 = self.random_value()
        expire = '2019-10-02T22:00:00Z'
        data = {'content':'contract_1', 'contractId':contractid_1, 'contractType':'partnership','expires':expire, 'parties':[{'name':'', 'type':''}],
                'signatures':[{'date':'2018-10-02T22:00:00Z', 'publicKey':'asdasd', 'signature':'asdasd', 'signedBy':'asdasd'}]}
        response = self.client_1.api.CreateOrganizationContracts(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('Create a new contract (2), should succeed with 201')
        contractid_2 = self.random_value()
        expire = '2018-10-02T22:00:00Z'
        data = {'content':'contract_2', 'contractId':contractid_2, 'contractType':'partnership','expires':expire, 'parties':[{'name':'', 'type':''}],
                'signatures':[{'date':'2018-10-02T22:00:00Z', 'publicKey':'asdasd', 'signature':'asdasd', 'signedBy':'asdasd'}]}
        response = self.client_1.api.CreateOrganizationContracts(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('Create a new expired contract (3), should succeed with 201')
        contractid_3 = self.random_value()
        expire = '2015-10-02T22:00:00Z'
        data = {'content':'contract_2', 'contractId':contractid_3, 'contractType':'partnership','expires':expire, 'parties':[{'name':'', 'type':''}],
                'signatures':[{'date':'2018-10-02T22:00:00Z', 'publicKey':'asdasd', 'signature':'asdasd', 'signedBy':'asdasd'}]}
        response = self.client_1.api.CreateOrganizationContracts(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get organization\'s contracts, should succeed with 200')
        response = self.client_1.api.GetOrganizationContracts(globalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn(contractid_1, [x['contractId'] for x in response.json()])
        self.assertIn(contractid_2, [x['contractId'] for x in response.json()])
        self.assertNotIn(contractid_3, [x['contractId'] for x in response.json()])

        self.lg('[GET] Get organization\'s contracts & include the expired contracts, should succeed with 200')
        response = self.client_1.api.GetOrganizationContracts(globalid, query_params={"includeExpired":True})
        self.assertEqual(response.status_code, 200)
        self.assertIn(contractid_3, [x['contractId'] for x in response.json()])

        self.lg('[GET] Get organization\'s contracts with page size 1, should succeed with 200')
        response = self.client_1.api.GetOrganizationContracts(globalid, query_params={"max":1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(contractid_1, [x['contractId'] for x in response.json()])
        self.assertNotIn(contractid_2, [x['contractId'] for x in response.json()])

        self.lg('[GET] Get organization\'s contracts with start page 2, should succeed with 200')
        response = self.client_1.api.GetOrganizationContracts(globalid, query_params={"start":2})
        self.assertEqual(response.status_code, 200)
        self.assertIn(contractid_2, [x['contractId'] for x in response.json()])
        self.assertNotIn(contractid_1, [x['contractId'] for x in response.json()])

    def tearDown(self):

        response = self.client_1.api.DeleteOrganization(self.org_11_globalid)
        self.assertEqual(response.status_code, 204)
        response = self.client_1.api.DeleteOrganization(self.org_12_globalid)
        self.assertEqual(response.status_code, 204)

        response = self.client_2.api.DeleteOrganization(self.org_21_globalid)
        self.assertEqual(response.status_code, 204)
        response = self.client_2.api.DeleteOrganization(self.org_22_globalid)
        self.assertEqual(response.status_code, 204)

        super(OrganizationsTestsB, self).tearDown()
