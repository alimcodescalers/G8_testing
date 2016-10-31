from functional_testing.Itsyouonline.api_testing.utils import BaseTest
import types
import uuid

class UsersTestsB(BaseTest):

    def setUp(self):
        super(UsersTestsB, self).setUp()
        #should be removed if not needed later
        #self.response = self.client.api.GetUser(self.user)
        #self.lg('GetUser [%s] response [%s]' % (self.user, self.response.json()))

    def test001_post_username(self):
        """ ITSYOU-001
        *Test case for check post user /users/{username}/name *

        **Test Scenario:**

        #. Put the user's firstname and last name, should succeed
        #. Update same parameters with fake user, should fail with 404
        #. Update the user's password, should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('Put the user\'s firstname and last name, should succeed')
        import ipdb;ipdb.sset_trace()
        name= str(uuid.uuid4()).replace('-', '')[0:10]
        data = {"firstname": name, "lastname": name}
        response = self.client.api.UpdateUserName(data, self.user)
        self.lg('UpdateUserName [%s] response [%s]' % (self.user, response.json()))
        self.assertEqual(response.status_code, 204)
        response = self.client.api.GetUser(self.user)
        self.assertEqual(response.json()['firstname'], name)
        self.assertEqual(response.json()['lastname'], name)

        self.lg('Update same parameters with nonexisting user, should fail with 404')
        nonexisting_user = 'fake user'
        try:
            response = self.client.api.UpdateUserName(data, nonexisting_user)
        except:
            self.assertEqual(response.status_code, 404)

        # should be done in the manual testing to check that the pass has been changed
        newpassword=str(uuid.uuid4()).replace('-', '')[0:10]
        currentpass='self.pass'
        data = {'currentpassword':'', 'newpassword':newpassword}
        response = self.client.api.UpdatePassword(data, self.user)
        self.lg('UpdatePassword [%s] response [%s]' % (self.user, response.json()))
        self.assertEqual(response.status_code, 204)
        self.lg('%s ENDED' % self._testID)

    def test002_put_delete_emailaddress(self):
        """ ITSYOU-002
        *Test case for registering, updating and deleting  user's emailaddress.*

        **Test Scenario:**

        #. Register a new email address, should succeed with 201
        #. Validate the email address, should succeed with 204
        #. Update the user's email address, should succeed with 201
        #. Delete the user's email address, should succeed with 204
        #. Try to delete the last email address, shoulf fail with 409
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('Register a new email address, should succeed with 201')
        label = str(uuid.uuid4()).replace('-', '')[0:6]
        email = str(uuid.uuid4()).replace('-', '')[0:10]+'test.com'
        data = {'emailaddress':email, 'label':label}
        response = self.client.api.RegisterNewEmailAddress(data, self.user)
        self.lg('UpdateUserName [%s] response [%s]' % (self.user, response.json()))
        self.assertEqual(response.status_code, 201)
        response2 = self.client.api.GetEmailAddresses(self.user)
        self.assertEqual(response2[len(response2) - 1]['emailaddress'], email)
        self.assertEqual(response2[len(response2) - 1]['label'], label)

        self.lg('Validate the email address, should succeed with 204')
        self.client.api.ValidateEmailAddress(data,label,self.user)
        self.assertEqual(response.status_code, 204)

        self.lg('update the user\'s email address, should succeed with 201')
        email = str(uuid.uuid4()).replace('-', '')[0:10] + 'test.com'
        data = {'emailaddress': email}
        response = self.client.api.UpdateEmailAddress(data, label ,self.user)
        self.lg('UpdateEmailAddress [%s] response [%s]' % (self.user, response.json()))
        self.assertEqual(response.status_code, 201)
        response2 = self.client.api.GetEmailAddresses(self.user)
        self.assertEqual(response2[len(response2) - 1]['emailaddress'], email)

        self.lg('delete the user\'s email address, should succeed with 204')
        self.client.api.DeleteEmailAddress(label, self.user)
        self.assertEqual(response.status_code, 204)
        try:
            response2 = self.client.api.GetEmailAddresses(self.user)
            response2[len(response2) - 1]['emailaddress']
        except KeyError:
            self.lg('Emailaddress is not found, Expected error')

        self.lg('Try to delete the last email address, should fail with 409')
        while(True):
            response2 = self.client.api.GetEmailAddresses(self.user)
            if len(response2) == 1:
                label = response2[0]['label']
                try:
                    response2 = self.client.api.DeleteEmailAddress(label, self.user)
                except:
                    self.assertEqual(response.status_code, 409)
                    break
            label = response2[len(response2)-1]['label']
            self.client.api.DeleteEmailAddress(label, self.user)
        self.lg('%s ENDED' % self._testID)


    def test003_put_post_delete_apikeys(self):
        """ ITSYOU-003
        *Test case for adding, updating and deleting  user's apikey *

        **Test Scenario:**

        #. Add a new apikey for the user, should succeed with 201
        #. Add a new apikey with the same label of the previous apikey, should fail with 409
        #. List user's apikeys, should succeed with at least 2 apikeys
        #. Get existing specific apikey, should succeed
        #. Update the apikey's label, should succeed with 201
        #. Update the apikey's label with another existing label, should fail with 409
        #. Try to delete the created apikey with fake label, should fail with 404
        #. Delete the created apikey, should succeed with 204
        #. Get nonexisting apikey, should fail with 404
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('Add a new apikey for the user, should succeed with 201')
        label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'label' : label}
        response = self.client.api.AddApiKey(data, self.user)
        self.lg('AddApiKey [%s] response [%s]' % (self.user, response.json()))
        self.assertEqual(response.status_code, 201)

        self.lg('Add a new apikey with the same label of the previous apikey, should fail with 409')
        try:
            response = self.client.api.AddApiKey(data, self.user)
        except:
            self.assertEqual(response.status_code, 409)

        self.lg('List user\'s apikeys, should succeed with at least 2 apikeys')
        response = self.client.api.ListAPIKeys(self.user)
        self.assertGreaterEqual(len(response), 2)
        self.assertEqual(response[len(response)-1]['label'] , label)

        self.lg('Get existing specific apikey, should succeed')
        response = self.client.api.GetAPIkey(label, self.user)
        self.assertEqual(response.status_code, 200)

        self.lg('Update the apikey\'s label, should succeed with 201')
        new_label = str(uuid.uuid4()).replace('-', '')[0:10]
        data = {'label': new_label}
        response = self.client.api.UpdateAPIkey(data, label, self.user)
        self.assertEqual(response.status_code, 201)
        response = self.client.api.GetAPIkey(new_label, self.user)
        self.assertEqual(response[len(response)-1]['label'] , new_label)


        self.lg('Update the apikey\'s label with another existing label, should fail with 409')
        response = self.client.api.ListAPIKeys(self.user)
        existing_label = response[0]['label']
        data = {'label': existing_label}
        try:
            response = self.client.api.UpdateAPIkey(data, label, self.user)
        except:
            self.assertEqual(response.status_code, 409)

        self.lg('Try to delete the created apikey with fake label, should fail with 404')
        try:
            response = self.client.api.DeleteAPIkey('fake_label', self.user)
        except:
            self.assertEqual(response.status_code, 404)


        self.lg('Delete the created apikey, should succeed with 204')
        response = self.client.api.DeleteAPIkey(label, self.user)
        self.assertEqual(response.status_code, 204)

        self.lg('Get nonexisting apikey, should fail with 404')
        try:
            response = self.client.api.GetAPIkey(label, self.user)
        except:
            self.assertEqual(response.status_code, 404)
        self.lg('%s ENDED' % self._testID)

    def test004_put_post_delete_addresses(self):
        """ ITSYOU-004
        *Test case for adding, updating and deleting  user's addresses *

        **Test Scenario:**

        #. Register a new address, should succeed with 201
        #. Add a new address with the same label of the previous address, should fail with 409
        #. Get this specific address, should succeed with 200

        #. check any of the constrains of the parameters(not Done)

        #. Update the address, should succeed with 201
        #. Try to delete the address with fake label, should fail with 404
        #. Delete the created address, should succeed with 204
        #. Get nonexisting address, should fail with 404
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('Register a new address, should succeed with 201')
        label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'label': label, 'city':'Cairo', 'country':'Egypt',
                'nr':'2', 'postalcode':'11234', 'street':'Masr gdida'}
        response = self.client.api.RegisterNewUserAddress(data, self.user)
        self.lg('RegisterNewUserAddress [%s] response [%s]' % (self.user, response.json()))
        self.assertEqual(response.status_code, 201)

        self.lg('Add a new address with the same label of the previous address, should fail with 409')
        try:
            response = self.client.api.UpdateUserAddress(data, label, self.user)
        except:
            self.assertEqual(response.status_code, 409)

        self.lg('Get this specific address, should succeed with 200')
        response = self.client.api.GetUserAddressByLabel(label, self.user)
        self.assertEqual(response.status_code, 200)
        response = self.client.api.GetUserInformation(self.user)
        addresses = response['addresses']
        self.assertEqual(addresses[len(addresses)-1]['label'], label)

        self.lg('Update the address, should succeed with 201')
        new_label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'postalcode':'99999', 'label': new_label}
        response = self.client.api.UpdateUserAddress(data, label, self.user)
        self.assertEqual(response.status_code, 201)
        response = self.client.api.GetUserAddressByLabel(new_label, self.user)
        self.assertEqual(response[len(response)-1]['label'], new_label)
        self.assertEqual(response[len(response)-1]['postalcode'], '99999')

        self.lg('Try to delete the address with fake label, should fail with 404')
        try:
            response = self.client.api.DeleteUserAddress('fake_label', self.user)
        except:
            self.assertEqual(response.status_code, 404)

        self.lg(' Delete the created address, should succeed with 204')
        response = self.client.api.DeleteUserAddress(label, self.user)
        self.assertEqual(response.status_code, 204)

        self.lg('Get nonexisting address, should fail with 404')
        try:
            response = self.client.api.GetUserAddressByLabel(label, self.user)
        except:
            self.assertEqual(response.status_code, 404)
        self.lg('%s ENDED' % self._testID)

    # the put_post_delete functions of digital wallet is not implemented
    def test005_put_post_delete_digitalwallet(self):
        """ ITSYOU-005
        *Test case for adding, updating and deleting  user's digital wallet *

        **Test Scenario:**

        #. Register a new digital wallet, should succeed with 201
        #. Add a new digital wallet with the same label of the previous digital wallet, should fail with 409
        #. Get this specific digital wallet, should succeed with 200
        #. Update the digital wallet, should succeed with 201
        #. Update the digital wallet with outdated expiry date, should fail
        #. Try to delete the digital wallet with fake label, should fail with 404
        #. Delete the created digital wallet, should succeed with 204
        #. Get nonexisting digital wallet, should fail with 404
        """


        self.lg('%s STARTED' % self._testID)


        self.lg('Register a new digital wallet, should succeed with 201')
        expire = '2018-10-02T22:00:00Z'
        label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'label': label, 'address': '12345 NYC',
                'currencysymbol': 'USD', 'expire': expire}
        response = self.client.api.RegisterDigitalWallet(data, self.user)
        self.lg('RegisterDigitalWallet [%s] response [%s]' % (self.user, response.json()))
        self.assertEqual(response.status_code, 201)

        self.lg('Add a new digital wallet with the same label of the previous digital wallet, should fail with 409')
        try:
            response = self.client.api.UpdateDigitalWallet(data, label, self.user)
        except:
            self.assertEqual(response.status_code, 409)

        self.lg('Get this specific digital wallet, should succeed with 200')
        response = self.client.api.GetUserDigitalWalletByLabel(label, self.user)
        self.assertEqual(response.status_code, 200)
        response = self.client.api.GetUser(self.user)
        self.assertEqual(response['digitalwallet']['label'], label)

        self.lg('Update the digital wallet, should succeed with 201')
        datetime_new = '2019-10-02T22:00:00Z'
        new_label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'expire': datetime_new, 'label': new_label}
        response = self.client.api.UpdateUserDigitalWallet(data, label, self.user)
        self.assertEqual(response.status_code, 201)
        response = self.client.api.GetUserDigitalWalletByLabel(new_label, self.user)
        self.assertEqual(response[len(response)-1]['label'], new_label)
        self.assertEqual(response[len(response)-1]['expire'], datetime_new)

        self.lg('Update the digital wallet with outdated expiry date')
        #scenario


        self.lg('Try to delete the digital wallet with fake label, should fail with 404')
        try:
            response = self.client.api.DeleteUserDigitalWallet('fake_label', self.user)
        except:
            self.assertEqual(response.status_code, 404)


        self.lg(' Delete the created digital wallet, should succeed with 204')
        response = self.client.api.DeleteUserDigitalWallet(label, self.user)
        self.assertEqual(response.status_code, 204)


        self.lg('Get nonexisting digital wallet, should fail with 404')
        try:
            response = self.client.api.GetUserDigitalWalletByLabel(label, self.user)
        except:
            self.assertEqual(response.status_code, 404)
        self.lg('%s ENDED' % self._testID)

    def test006_put_post_delete_phonenumbers(self):
        """ ITSYOU-006
        *Test case for adding, updating and deleting  user's phonenumbers *

        **Test Scenario:**

        #. Register a new phonenumber, should succeed with 201
        #. Add a new phonenumber with the same label of the previous phonenumber, should fail with 409
        #. Get this specific phonenumber, should succeed with 200
        #. Update the phonenumber, should succeed with 201
        #. Try to delete the phonenumber with fake label, should fail with 404
        #. Delete the created phonenumber, should succeed with 204
        #. Get nonexisting phonenumber, should fail with 404
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('Register a new phonenumber, should succeed with 201')
        label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'label':label, 'phonenumber':'+01288184444'}
        response = self.client.api.RegisterNewUserPhonenumber(data, self.user)
        self.lg('RegisterNewUserPhonenumber [%s] response [%s]' % (self.user, response.json()))
        self.assertEqual(response.status_code, 201)

        self.lg('Add a new address with the same label of the previous address, should fail with 409')
        try:
            response = self.client.api.UpdateUserPhonenumber(data, label, self.user)
        except:
            self.assertEqual(response.status_code, 409)

        self.lg('Get this specific address, should succeed with 200')
        response = self.client.api.GetUserPhonenumberByLabel(label, self.user)
        self.assertEqual(response.status_code, 200)
        response = self.client.api.GetUserInformation(self.user)
        phonenumbers = response['phonenumbers']
        self.assertEqual(phonenumbers[len(phonenumbers)-1]['label'], label)

        self.lg('Update the phonenumber, should succeed with 201')
        new_label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'phonenumber': '+201288185555', 'label': new_label}
        response = self.client.api.UpdateUserPhonenumber(data, label, self.user)
        self.assertEqual(response.status_code, 201)
        response = self.client.api.GetUserPhonenumberByLabel(new_label, self.user)
        self.assertEqual(response[len(response)-1]['label'], new_label)
        self.assertEqual(response[len(response)-1]['phonenumber'], '201288185555')

        self.lg('Try to delete the phonenumber with fake label, should fail with 404')
        try:
            response = self.client.api.DeleteUserPhonenumber('fake_label', self.user)
        except:
            self.assertEqual(response.status_code, 404)

        self.lg(' Delete the created phonenumber, should succeed with 204')
        response = self.client.api.DeleteUserPhonenumber(label, self.user)
        self.assertEqual(response.status_code, 204)

        self.lg('Get nonexisting address, should fail with 404')
        try:
            response = self.client.api.GetUserPhonenumberByLabel(label, self.user)
        except:
            self.assertEqual(response.status_code, 404)
        self.lg('%s ENDED' % self._testID)

    def test007_put_post_delete_bankaccount(self):
        """ ITSYOU-007
        *Test case for adding, updating and deleting  user's bank account *

        **Test Scenario:**

        #. Register a new bank account, should succeed with 201
        #. Add a new bank account with the same label of the previous bank account, should fail with 409
        #. Get this specific bank account, should succeed with 200
        #. Update the bank account, should succeed with 201
        #. Update the bank account's BIC with wrong BIC, should fail
        #. Try to delete the bank account with fake label, should fail with 404
        #. Delete the created bank account, should succeed with 204
        #. Get nonexisting bank account, should fail with 404
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('Register a new bank account, should succeed with 201')
        label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'label': label, 'bic': '21232333', 'country':'Egypt', 'iban':'123123123123'}
        response = self.client.api.CreateUserBankAccount(data, self.user)
        self.lg('CreateUserBankAccount [%s] response [%s]' % (self.user, response.json()))
        self.assertEqual(response.status_code, 201)

        self.lg('Add a new bank account with the same label of the previous bank account, should fail with 409')
        try:
            response = self.client.api.CreateUserBankAccount(data, label, self.user)
        except:
            self.assertEqual(response.status_code, 409)

        self.lg('Get this specific bank account, should succeed with 200')
        response = self.client.api.GetUserBankAccountByLabel(label, self.user)
        self.assertEqual(response.status_code, 200)
        response = self.client.api.GetUser(self.user)
        bankaccounts = response['bankaccounts']
        self.assertEqual(bankaccounts[len(bankaccounts)-1]['label'], label)

        self.lg('Update the bank account, should succeed with 201')

        new_label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'label': new_label, 'bic': '21sds234', 'country': 'Egypt', 'iban': '1231231'}
        response = self.client.api.UpdateUserBankAccount(data, self.user, label)
        self.assertEqual(response.status_code, 201)
        response = self.client.api.GetUserBankAccountByLabel(new_label, self.user)
        self.assertEqual(response[len(response)-1]['label'], new_label)
        self.assertEqual(response[len(response)-1]['bic'], '21sds234')

        self.lg("Update the bank account's BIC with wrong BIC, should fail")
        data = {'label': label, 'bic': '212', 'country': 'Egypt', 'iban': '123123123123'}
        try:
            self.client.api.UpdateUserBankAccount(data, self.user, label)
        except:
            raise

        self.lg('Try to delete the bank account with fake label, should fail with 404')
        try:
            response = self.client.api.DeleteUserBankAccount('fake_label', self.user)
        except:
            self.assertEqual(response.status_code, 404)

        self.lg('Delete the created bank account, should succeed with 204')
        response = self.client.api.DeleteUserBankAccount(label, self.user)
        self.assertEqual(response.status_code, 204)

        self.lg('Get nonexisting bank account, should fail with 404')
        try:
            response = self.client.api.GetUserBankAccountByLabel(label, self.user)
        except:
            self.assertEqual(response.status_code, 404)
        self.lg('%s ENDED' % self._testID)

    def test008_delete_facebook_account(self):
        """ ITSYOU-008
        *Test case for deleting facebook account.*

        **Test Scenario:**

        #. Check if facebook account exists, should succeed
        #. Delete facebook account, should succeed
        #. Check if the facebook account is deleted, should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('Check if facebook account exists, should succeed')
        response = self.client.api.GetUser(self.user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('facebook', response.json().keys())
        self.assertEqual(type(response.json()['facebook']), types.DictType)
        empty_account = {'id':'', 'link':'', 'name':'', 'picture':''}
        self.assertNotEqual(response.json()['facebook'], empty_account)
        self.lg('Delete facebook account, should succeed')
        response = self.client.api.DeleteFacebookAccount(self.user)
        self.assertEqual(response.status_code, 204)
        self.lg('Check if the facebook account is deleted, should succeed')
        response = self.client.api.GetUser(self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['facebook'], empty_account)
        self.lg('%s ENDED' % self._testID)

    def test009_delete_github_account(self):
        """ ITSYOU-009
        *Test case for deleting github account*

        **Test Scenario:**

        #. Check if github account exists, should succeed
        #. Delete github account, should succeed
        #. Check if the github account is deleted, should succeed
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('Check if github account exists, should succeed')
        response = self.client.api.GetUser(self.user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('github', response.json().keys())
        self.assertEqual(type(response.json()['github']), types.DictType)
        empty_account = {u'avatar_url': u'', u'html_url': u'', u'id': 0, u'login': u'', u'name': u''}
        self.assertNotEqual(response.json()['github'], empty_account)
        self.lg('Delete github account, should succeed')
        response = self.client.api.DeleteGithubAccount(username=self.user)
        self.assertEqual(response.status_code, 204)
        self.lg('Check if the github account is deleted, should succeed')
        response = self.client.api.GetUser(self.user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('github', response.json().keys())
        self.assertEqual(type(response.json()['github']), types.DictType)
        self.assertEqual(response.json()['github'], empty_account)
        self.lg('%s ENDED' % self._testID)

    def test010_put_delete_organization_auth(self):
        """ ITSYOU-010
        *Test case for leaving, accepting, rejecting  user's invitation or organization
        and updating, deleting user's authorization as well*

        **Test Scenario:**

        #. Create a new organization with user1, should succeed
        #. Send invitation to user2 to join an organization, should succeed (organization api)
        #. Accept membership in organization, should succeed with 201

        #. Modify certain information to be granted to specific organization, should succeed
        #. Remove the authorization for the organization, should succeed

        #. Leave an organization with unknown user, should fail with 404
        #. Leave an organization, get list of organization
        #. send another invitation, should succeed
        #. Reject the invitation, should succeed with 204
        """
        self.lg('Create a new organization with user1, should succeed')
        globalid = str(uuid.uuid4()).replace('-', '')[0:10]
        data = {'dns':[], globalid:globalid, 'includes':[],
                'members':[], 'owners':[self.user], 'publicKeys':[]}
        response = self.client.api.CreateNewOrganization(data)
        self.assertEqual(response.status_code, 201)

        self.lg('Send invitation to someone to join an organization, should succeed')
        role = 'member'; user2 = 'anotheruser'
        data = {'username': user2}
        response = self.client.api.AddOrganizationMember(data, globalid)
        self.assertEqual(response.status_code, 201)
        response = self.client.api.GetNotifications(user2)
        invitations = response['invitations']
        self.assertEqual(invitations[len(invitations)-1]['organization'], globalid)
        self.assertEqual(invitations[len(invitations)-1]['status'], 'pending')

        self.lg('Accept membership in organization, should succeed with 201')
        data={'created':'datatime..don\'t know what is that',
              'organization':globalid, 'role':role, 'user': user2}
        response = self.client.api.AcceptMembership(data, globalid, role, user2)
        self.assertEqual(response.status_code, 201)
        response = self.client.api.GetUserOrganizations(user2)
        self.assertIn(globalid, response[role])
        response = self.client.api.GetNotifications(user2)
        invitations = response['invitations']
        self.assertEqual(invitations[len(invitations)-1]['status'], 'accepted')


        self.lg('Modify certain information to be granted to specific organization, should succeed')
        # not sure if this data is right
        data = {"emailaddresses": [{"requestedlabel": "main", "reallabel": "main"}],
                "phonenumbers": [{"requestedlabel": "main", "reallabel": "main"}]}
        grantedto = globalid
        response = self.client.api.UpdateAuthorization(data, grantedto, user2)
        self.assertEqual(response.status_code, 201)
        response = self.client.api.GetAuthorization(grantedto, user2)
        self.assertIn('emailaddresses', response)

        self.lg('Remove the authorization for the organization, should succeed')
        response = self.client.api.DeleteAuthorization(grantedto, user2)
        self.assertEqual(response.status_code, 204)
        response = self.client.api.GetAuthorization(grantedto, user2)
        self.assertNotIn('emailaddresses', response)
        self.assertNotIn('phonenumbers', response)


        self.lg('Leave an organization with unkown user, should fail with 404')
        try:
            response = self.client.api.LeaveOrganization(globalid, 'unknow_user')
        except:
            self.assertEqual(response.status_code, 404)

        self.lg('Leave an organization, should succeed with 204')
        self.client.api.LeaveOrganization(globalid, user2)
        self.assertEqual(response.status_code, 204)
        response = self.client.api.GetUserOrganizations(user2)
        self.assertNotIn(globalid, response[role])

        self.lg('Send the invitation once more, should succeed')
        data = {'role': role, 'username': user2}
        response = self.client.api.AddOrganizationMember(data, globalid)
        self.assertEqual(response.status_code, 201)

        self.lg('Reject the invitation, should succeed with 204')
        self.client.api.RejectMembership(globalid, role, user2)
        self.assertEqual(response.status_code, 204)
        response = self.client.api.GetUserOrganizations(user2)
        self.assertNotIn(globalid, response[role])
        response = self.client.api.GetNotifications(user2)
        invitations = response['invitations']
        self.assertEqual(invitations[len(invitations)-1]['status'], 'rejected')

    def test011_create_contract(self):
        """ ITSYOU-011
        *Test case for creating  user's contract*

        **Test Scenario:**

        #. Create a new contract, should succeed
        #. Create an new contract with unauthorized user, should fail with 404 (not implemented yet)
        """
        self.lg('Create a new contract, should succeed')
        contractid = str(uuid.uuid4()).replace('-', '')[0:6]
        expire = '2019-10-02T22:00:00Z'
        data = {'content':'test', 'contractId':contractid, 'contractType':'partnership',
                'expires':expire, 'parties':[{'name':'', 'type':''}],
                'signatures':[{'date':'', 'publicKey':'', 'signature':'', 'signedBy':''}]}
        response = self.client.api.CreateUserContract(data, self.user)
        self.assertEqual(response.status_code, 201)

    def test012_post_delete_registry(self):
        pass
















