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
        label = 'backup'
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
        label = 'secondary'
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
        new_label = 'secondary_updated'
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
















