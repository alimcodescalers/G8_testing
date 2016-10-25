from functional_testing.Itsyouonline.api_testing.utils import BaseTest
import unittest
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

        label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'label': label, 'address': '12345 NYC',
                'currencysymbol': 'USD', 'expire': datetime_type}
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
        new_label = str(uuid.uuid4()).replace('-', '')[0:6]
        data = {'expire': datetimenew, 'label': new_label}
        response = self.client.api.UpdateUserDigitalWallet(data, label, self.user)
        self.assertEqual(response.status_code, 201)
        response = self.client.api.GetUserDigitalWalletByLabel(new_label, self.user)
        self.assertEqual(response[len(response)-1]['label'], new_label)
        self.assertEqual(response[len(response)-1]['expire'], datetimenew)

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
        *Test case for adding, updating and deleting  user's phonenumbers *

        **Test Scenario:**

        #. Register a new bank account, should succeed with 201
        #. Add a new bank account with the same label of the previous bank account, should fail with 409
        #. Get this specific bank account, should succeed with 200
        #. Update the bank account, should succeed with 201
        #. Try to delete the bank account with fake label, should fail with 404
        #. Delete the created bank account, should succeed with 204
        #. Get nonexisting bank account, should fail with 404
        """














