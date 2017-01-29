from functional_testing.Itsyouonline.api_testing.utils import BaseTest
import types
import unittest
from random import randint
import json
import time

class UsersTestsB(BaseTest):

    def setUp(self):
        super(UsersTestsB, self).setUp()
        self.password = '123456'

    def test000_get_user(self):

        """
            #Test 000 [USER]
            - [GET] Get username info - should succeed with 200
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('[GET] Get username info - should succeed with 200')
        response = self.client_1.api.GetUser(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.lg('%s ENDED' % self._testID)

    def test001_put_name(self):

        """
            #Test 001 [NAME]
            - [PUT] Change firstname & lastname to a valid user - should succeed with 204
            - [PUT] Change firstname & lastname to a invalid user - should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('[PUT] Change firstname & lastname to a valid user - should succeed with 204')
        firstname = self.random_value()
        lastname  = self.random_value()
        data = {"firstname": firstname, "lastname": lastname}
        response = self.client_1.api.UpdateUserName(data, self.user_1)
        self.assertEqual(response.status_code, 204)
        response = self.client_1.api.GetUser(self.user_1)
        self.assertEqual(response.json()['firstname'], firstname)
        self.assertEqual(response.json()['lastname'], lastname)
        self.lg('[PUT] Change firstname & lastname to a invalid user - should fail with 404')
        response = self.client_1.api.UpdateUserName(data, 'fake user')
        self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    def test002_put_password(self):

        """
            #Test 002 [PASSWORD]
            - [PUT] Change password with valid current password - should succeed with 204
            - [PUT] Change password with valid current password again - should succeed with 204
            - [PUT] Change password with wrong current password - should fail with 422
            - [PUT] Change password with invalid new password - should fail with 422
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('[PUT] Change password with valid current password - should succeed with 204')
        current_password = self.password
        new_password = 'TheNewPassword123456'
        data = {'currentpassword':current_password, 'newpassword':new_password}
        response = self.client_1.api.UpdatePassword(data, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[PUT] Change password with valid current password again - should succeed with 204')
        current_password = new_password
        new_password = self.password
        data = {'currentpassword':current_password, 'newpassword':new_password}
        response = self.client_1.api.UpdatePassword(data, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[PUT] Change password with wrong current password - should fail with 422')
        current_password = self.random_value()
        new_password = self.random_value()
        data = {'currentpassword':current_password, 'newpassword':new_password}
        response = self.client_1.api.UpdatePassword(data, self.user_1)
        self.lg('UpdatePassword [%s] response [%s]' % (self.user_1, response.json()))
        self.assertEqual(response.status_code, 422)

        self.lg('Change password with invalid new password - should fail with 422')
        current_password = self.password
        new_password = self.random_value()[0:3]
        data = {'currentpassword':current_password, 'newpassword':new_password}
        response = self.client_1.api.UpdatePassword(data, self.user_1)
        self.lg('UpdatePassword [%s] response [%s]' % (self.user_1, response.json()))
        self.assertEqual(response.status_code, 422)

        self.lg('%s ENDED' % self._testID)

    def test003_get_post_put_delete_email_address(self):

        """
            #Test 003 [EMAIL ADDRESS]
            - [GET ] Get email addresses - should succeed with 200
            - [POST] Create new email address - should succeed with 201
            - [POST] Create new email address with label already exists - should fail with 409
            - [PUT]  Edit email address & label - should succeed with 201
            - [PUT]  Edit email label with label already exists - should fail with 409
            - [POST] Sends validation email to email address - should succeed with 204
            - [POST] Sends validation email to invalid email address - should fail with 404
            - [DEL]  Delete email address - should succeed with 204
            - [DEL]  Delete invalid email address - should fail with 404
            - [DEL]  Delete last email address - should fail with 409
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('[GET] Get email addresses - should succeed with 200')
        response = self.client_1.api.GetEmailAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)

        self.lg('[POST] Create new email address - should succeed with 201')
        label = self.random_value()
        new_email_address = self.random_value() + "@gig.com"
        data = {"emailaddress":new_email_address, "label":label}
        response = self.client_1.api.RegisterNewEmailAddress(data, self.user_1)
        self.assertEqual(response.status_code, 201)
        response = self.client_1.api.GetEmailAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_email_address, response.json()[-1]['emailaddress'])
        self.assertEqual(label, response.json()[-1]['label'])

        self.lg('[POST] Create new email address with label already exist - should fail with 409')
        response = self.client_1.api.GetEmailAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_email_address = self.random_value() + "@gig.com"
        data = {'emailaddress':new_email_address, 'label':label}
        response = self.client_1.api.RegisterNewEmailAddress(data, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[PUT] Edit email address & label - should succeed with 201')
        response = self.client_1.api.GetEmailAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = self.random_value()
        new_email_address = self.random_value() + "@gig.com"
        data = {'emailaddress':new_email_address, 'label':new_label}
        response = self.client_1.api.UpdateEmailAddress(data,label, self.user_1)
        self.assertEqual(response.status_code, 201)
        response = self.client_1.api.GetEmailAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_email_address, response.json()[-1]['emailaddress'])
        self.assertEqual(new_label, response.json()[-1]['label'])

        self.lg('[PUT] Edit email label with label already exists - should fail with 409')
        response = self.client_1.api.GetEmailAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = response.json()[-2]['label']
        new_email_address = self.random_value() + "@gig.com"
        data = {'emailaddress':new_email_address, 'label':new_label}
        response = self.client_1.api.UpdateEmailAddress(data, label, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[POST] Create new email address & validate it - should succeed with 201')
        label = "validation email"
        new_email_address = self.validation_email
        data = {"emailaddress":new_email_address, "label":label}
        response = self.client_1.api.RegisterNewEmailAddress(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        time.sleep(10)

        response = self.client_1.api.ValidateEmailAddress(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        time.sleep(10)

        self.lg('Check the validation message & validate - should succeed with 200')
        response = self.UserValidateEmail()
        self.assertEqual(response.status_code, 200)

        response = self.client_1.api.GetEmailAddresses(self.user_1, query_params={'validated':True})
        self.assertEqual(response.status_code, 200)
        self.assertIn(label, [x['label'] for x in response.json()])

        self.lg('[POST] Sends validation email to invalid email address - should fail with 404')
        response = self.client_1.api.ValidateEmailAddress('fake_label', self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('[DELETE] Delete email address - should succeed with 204')
        response = self.client_1.api.GetEmailAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteEmailAddress(label, self.user_1)
        self.assertEqual(response.status_code, 204)
        response = self.client_1.api.GetEmailAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(label, response.json()[-1]['label'])

        self.lg('[DELETE] Delete invalid email address - should fail with 404')
        response = self.client_1.api.DeleteEmailAddress("fake_label", self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('[DELETE] Delete last email address - should fail with 409')
        response = self.client_1.api.GetEmailAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        labels = [x['label'] for x in response.json()]
        for i in range(0, len(labels)-1):
            response = self.client_1.api.DeleteEmailAddress(labels[i], self.user_1)
            self.assertEqual(response.status_code, 204)
        else:
            response = self.client_1.api.DeleteEmailAddress(labels[len(labels)-1], self.user_1)
            self.assertEqual(response.status_code, 409)

        self.lg('%s ENDED' % self._testID)

    def test004_get_post_put_delete_phonenumber(self):
        """
            #Test 004 [PHONE NUMBER]
            - [POST] Register a new phonenumber - should succeed with 201
            - [POST] Register a new phonenumber again - should succeed with 201
            - [GET]  Get user phonenumbers - should succeed with 200
            - [GET]  Get phonenumber by label - should succeed with 200
            - [POST] Register a new phonenumber with invalid number - should fail with 400
            - [POST] Register a new phonenumber with existing label - should fail with 409
            - [GET]  Get phonenumber by nonexisting label - should fail with 404
            - [PUT]  Update phonenumber - should succeed with 201
            - [PUT]  Update phonenumber with invalid number - should fail with 400
            - [PUT]  Update phonenumber label with label already exist - should fail with 409
            - [POST] [POST] Register a new phonenumber & send validation sms - should succeed with 201 & 200
            - [DEL]  Delete verified phonenumber - should fail with 409
            - [DEL]  Force Delete verified phonenumber - should succeed with 204
            - [POST] Validate & activate invalid phonenumber - should fail with 404
            - [DEL]  Delete phonenumber - should succeed with 204
            - [DEL]  Delete phonenumber again - should succeed with 204
            - [DEL]  Delete invalid phone number - should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('[POST] Register a new phonenumber - should succeed with 201')
        label = self.random_value()
        phonenumber = "+0123456789"
        data = {"label":label, "phonenumber":phonenumber}
        response = self.client_1.api.RegisterNewUserPhonenumber(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new phonenumber again - should succeed with 201')
        new_label = self.random_value()
        new_phonenumber = "+01987654321"
        new_data = {"label":new_label, "phonenumber":new_phonenumber}
        response = self.client_1.api.RegisterNewUserPhonenumber(new_data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get user phonenumbers - should succeed with 200')
        response = self.client_1.api.GetUserPhoneNumbers(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data, response.json())
        self.assertIn(new_data, response.json())

        self.lg('[GET] Get phonenumber by label - should succeed with 200')
        label = response.json()[-1]['label']
        response = self.client_1.api.GetUserPhonenumberByLabel(label, self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data, response.json())

        self.lg('[POST] Register a new phonenumber with invalid number - should fail with 400')
        new_label = self.random_value()
        new_phonenumber = self.random_value()
        new_data = {"label":new_label, "phonenumber":new_phonenumber}
        response = self.client_1.api.RegisterNewUserPhonenumber(new_data, self.user_1)
        self.assertEqual(response.status_code, 400)

        self.lg('[POST] Register a new phonenumber with existing label - should fail with 409')
        response = self.client_1.api.GetUserPhoneNumbers(self.user_1)
        self.assertEqual(response.status_code, 200)
        new_label = response.json()[-1]['label']
        new_phonenumber = "+123456789"
        new_data = {"label":new_label, "phonenumber":new_phonenumber}
        response = self.client_1.api.RegisterNewUserPhonenumber(new_data, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[GET] Get phonenumber by nonexisting label - should fail with 404')
        response = self.client_1.api.GetUserPhonenumberByLabel('fake_label', self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('[PUT] Update phonenumber - should succeed with 201')
        response = self.client_1.api.GetUserPhoneNumbers(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = self.random_value()
        new_phonenumber = "+987654321"
        new_data = {"label":new_label, "phonenumber":new_phonenumber}
        response = self.client_1.api.UpdateUserPhonenumber(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[PUT] Update phonenumber with invalid number - should fail with 400')
        response = self.client_1.api.GetUserPhoneNumbers(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = self.random_value()
        new_phonenumber = self.random_value()
        new_data = {"label":new_label, "phonenumber":new_phonenumber}
        response = self.client_1.api.UpdateUserPhonenumber(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 400)

        self.lg('[PUT] Update phonenumber label with label already exist - should fail with 409')
        response = self.client_1.api.GetUserPhoneNumbers(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = response.json()[-2]['label']
        new_phonenumber = "+123456789"
        new_data = {"label":new_label, "phonenumber":new_phonenumber}
        response = self.client_1.api.UpdateUserPhonenumber(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[POST] Register a new phonenumber & send validation sms - should succeed with 201 & 200')
        label = 'validation number'
        phonenumber = self.get_valid_phonenumber()
        print phonenumber
        data = {"label":label, "phonenumber":phonenumber}
        response = self.client_1.api.RegisterNewUserPhonenumber(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        response = self.client_1.api.ValidatePhonenumber(label, self.user_1)
        self.assertEqual(response.status_code, 200)
        validationkey = response.json()['validationkey']

        time.sleep(25)

        smscode = self.get_mobile_verification_code()
        data = {"smscode":smscode, "validationkey":validationkey}
        response = self.client_1.api.VerifyPhoneNumber(data, label, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetUserPhoneNumbers(self.user_1, query_params={'validated':True})
        self.assertEqual(response.status_code, 200)
        self.assertIn(label, [x['label'] for x in response.json()])

        self.lg('[DELETE] Delete verified phonenumber - should fail with 409')
        response = self.client_1.api.DeleteUserPhonenumber(label, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[DELETE] Force Delete verified phonenumber - should succeed with 204')
        response = self.client_1.api.DeleteUserPhonenumber(label, self.user_1, query_params={'force':'true'})
        self.assertEqual(response.status_code, 204)

        self.lg('[POST] Validate & activate invalid phonenumber label - should succeed with 200')
        response = self.client_1.api.ValidatePhonenumber('fake_label', self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('[DELETE] Delete phonenumber - should succeed with 204')
        response = self.client_1.api.GetUserPhoneNumbers(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserPhonenumber(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete phonenumber again - should succeed with 204')
        response = self.client_1.api.GetUserPhoneNumbers(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserPhonenumber(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete invalid phone number - should fail with 404')
        response = self.client_1.api.DeleteUserPhonenumber(label, self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    def test005_get_post_put_delete_address(self):
        """
        #Test 005 [ADDRESSES]
        - [POST] Register a new address - should succeed with 201
        - [POST] Register a new address again - should succeed with 201
        - [GET] Get Addresse by label - should succeed with 200
        - [GET] Get Addresses - should succeed with 200
        - [POST] Register a new address with existing label - should fail with 409
        - [POST] Register a new address with invalid inputs - should fail with 400
        - [PUT] Edit address - should succeed with 201
        - [PUT] Edit address with exisiting label- should fail with 409
        - [PUT] Edit address with invalid inputs - should fail with 400
        - [DEL] Delete address - should succeed with 204
        - [DEL] Delete address again - should succeed with 204
        - [DEL] Delete invalid address - should fail with 404
        """

        elements = {"city":30, "country":40 ,"nr":10, "postalcode":20, "street":50, "other":30}

        self.lg('%s STARTED' % self._testID)

        self.lg('[POST] Register a new address - should succeed with 201')
        label = self.random_value()
        data = {"city": self.random_value(),
                "country": self.random_value(),
                "nr": self.random_value(),
                "other": self.random_value(),
                "postalcode": self.random_value(),
                "street": self.random_value(),
                "label": label}

        response = self.client_1.api.RegisterNewUserAddress(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new address again - should succeed with 201')
        label = self.random_value()
        new_data = {"city": self.random_value(),
                "country": self.random_value(),
                "nr": self.random_value(),
                "other": self.random_value(),
                "postalcode": self.random_value(),
                "street": self.random_value(),
                "label": label}

        response = self.client_1.api.RegisterNewUserAddress(new_data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get Addresses - should succeed with 200')
        response = self.client_1.api.GetUserAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data, response.json())
        self.assertIn(new_data, response.json())

        self.lg('[GET] Get Addresse by label - should succeed with 200')
        response = self.client_1.api.GetUserAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.GetUserAddressByLabel(label, self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data, response.json())


        self.lg('[POST] Register a new address with existing label - should fail with 409')
        new_data['label'] = label
        response = self.client_1.api.RegisterNewUserAddress(data, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[POST] Register a new address with invalid inputs - should fail with 400')
        new_data = dict(data)
        for key, value in elements.items():
            new_data['label'] = self.random_value()
            new_data[key] = self.random_value(value+1)
            response = self.client_1.api.RegisterNewUserAddress(new_data, self.user_1)
            self.assertEqual(response.status_code, 400)
            new_data = dict(data)

        self.lg('[PUT] Edit address - should succeed with 201')
        response = self.client_1.api.GetUserAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_data = {"city": self.random_value(),
                "country": self.random_value(),
                "nr": self.random_value(),
                "other": self.random_value(),
                "postalcode": self.random_value(),
                "street": self.random_value(),
                "label": self.random_value()}

        response = self.client_1.api.UpdateUserAddress(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[PUT] Edit address with exisiting label- should fail with 409')
        response = self.client_1.api.GetUserAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = response.json()[-2]['label']
        new_data = {"city": self.random_value(),
                    "country": self.random_value(),
                    "nr": self.random_value(),
                    "other": self.random_value(),
                    "postalcode": self.random_value(),
                    "street": self.random_value(),
                    "label": new_label}

        response = self.client_1.api.UpdateUserAddress(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[PUT] Edit address with invalid inputs - should fail with 400')

        new_data = dict(data)
        new_data['label'] = self.random_value()
        for key, value in elements.items():
            new_data[key] = self.random_value(value+1)
            response = self.client_1.api.UpdateUserAddress(new_data, label, self.user_1)
            self.assertEqual(response.status_code, 400)
            new_data = dict(data)

        self.lg('[DELETE] Delete address - should succeed with 204')
        response = self.client_1.api.GetUserAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserAddress(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete address again - should succeed with 204')
        response = self.client_1.api.GetUserAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserAddress(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetUserAddresses(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        self.lg('[DELETE] Delete invalid address - should fail with 404')
        response = self.client_1.api.DeleteUserAddress('fake_address', self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('bug #415')
    def test006_get_post_put_delete_banks(self):
        """
            #Test 006 [BANKS]
            - [POST] Register a new bank account - should succeed with 201
            - [POST] Register a new bank account again - should succeed with 201
            - [GET] Get bank accounts - should succeed with 200
            - [GET] Get bank account by label - should succeed with 200
            - [POST] Register a new bank account with existing label - should fail with 409
            - [POST] Register a new bank account with invalid inputs - should fail with 400
            - [PUT] Edit bank account - should succeed with 201
            - [PUT] Edit bank account with exisiting label- should fail with 409
            - [PUT] Edit bank account with invalid inputs - should fail with 400
            - [DEL] Delete bank account - should succeed with 204
            - [DEL] Delete bank account again - should succeed with 204
            - [DEL] Delete invalid bank account - should fail with 404
        """

        elements = {"bic":11,"country":40,"iban":30}

        self.lg('%s STARTED' % self._testID)

        self.lg('[POST] Register a new bank account - should succeed with 201')
        label = self.random_value()
        data = {"bic": self.random_value(8),
                "country": self.random_value(),
                "iban": self.random_value(),
                "label": label}
        response = self.client_1.api.CreateUserBankAccount(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new bank account again - should succeed with 201')
        new_label = self.random_value()
        new_data = {"bic": self.random_value(11),
                    "country": self.random_value(),
                    "iban": self.random_value(),
                    "label": new_label}
        response = self.client_1.api.CreateUserBankAccount(new_data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get bank accounts - should succeed with 200')
        response = self.client_1.api.GetUserBankAccounts(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data, response.json())
        self.assertIn(new_data, response.json())

        self.lg('[GET] Get bank account by label - should succeed with 200')
        label = response.json()[-1]['label']
        response = self.client_1.api.GetUserBankAccountByLabel(label, self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data, response.json())


        self.lg('[POST] Register a new bank account with existing label - should fail with 409')
        response = self.client_1.api.GetUserBankAccounts(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_data = {"bic": self.random_value(8),
                    "country": self.random_value(),
                    "iban": self.random_value(),
                    "label": label}

        response = self.client_1.api.CreateUserBankAccount(new_data, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[POST] Register a new bank account with invalid inputs - should fail with 400')
        new_data = dict(data)
        for key, value in elements.items():
            new_data['label'] = self.random_value()
            new_data[key] = self.random_value(value+1)
            response = self.client_1.api.CreateUserBankAccount(new_data, self.user_1)
            self.assertEqual(response.status_code, 400)
            new_data = dict(data)

        self.lg('[PUT] Edit bank account - should succeed with 201')
        response = self.client_1.api.GetUserBankAccounts(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_data = {"bic": self.random_value(8),
                    "country": self.random_value(),
                    "iban": self.random_value(),
                    "label": self.random_value()}
        response = self.client_1.api.UpdateUserBankAccount(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 200) ### response section is empty

        self.lg('[PUT] Edit bank account with exisiting label- should fail with 409')
        response = self.client_1.api.GetUserBankAccounts(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = response.json()[-2]['label']
        new_data = {"bic": self.random_value(8),
                    "country": self.random_value(),
                    "iban": self.random_value(),
                    "label": new_label}
        response = self.client_1.api.UpdateUserBankAccount(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[PUT] Edit bank account with invalid inputs - should fail with 400')
        new_data = dict(data)
        for key, value in elements.items():
            new_data[key] = self.random_value(value+1)
            response = self.client_1.api.UpdateUserBankAccount(new_data, label, self.user_1)
            self.assertEqual(response.status_code, 400)
            new_data = dict(data)

        self.lg('[DELETE] Delete bank account - should succeed with 204')
        response = self.client_1.api.GetUserBankAccounts(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserBankAccount(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete bank account again - should succeed with 204')
        response = self.client_1.api.GetUserBankAccounts(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserBankAccount(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetUserBankAccounts(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        self.lg('[DELETE] Delete invalid bank account - should fail with 404')
        response = self.client_1.api.DeleteUserBankAccount('fake_bank_account', self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    def test007_get_notifications(self):
        """
            #Test 007 [NOTIFICATIONS]
        """
        self.lg('%s STARTED' % self._testID)
        self.lg('[GET] Get Notifications - should succeed with 200')
        response = self.client_1.api.GetNotifications(self.user_1)
        self.assertEqual(response.status_code, 200)

    def test008_get_post_put_delete_publickey(self):
        """
            #Test 008 [PUBLICKEYS]
            - [POST] Register a new publickey - should succeed with 201
            - [POST] Register a new publickey again - should succeed with 201
            - [GET] Get publickeys - should succeed with 200
            - [GET] Get publickey by label - should succeed with 200
            - [POST] Register a new publickey with existing label - should fail with 409
            - [POST] Register a new publickey with invalid inputs - should fail with 400
            - [PUT] Edit publickey - should succeed with 201
            - [PUT] Edit publickey with exisiting label- should fail with 409
            - [PUT] Edit publickey with invalid inputs - should fail with 400
            - [DEL] Delete publickey - should succeed with 204
            - [DEL] Delete publickey again - should succeed with 204
            - [DEL] Delete invalid publickey - should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('[POST] Register a new publickey - should succeed with 201')
        label = self.random_value()
        publickey = 'ssh-rsa AAAAB3NzaC1yc2E'+self.random_value(30)
        data = {"label": label,"publickey": publickey}
        response = self.client_1.api.RegisterUserPublicKey(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new publickey again - should succeed with 201')
        new_label = self.random_value()
        publickey = 'ssh-rsa AAAAB3NzaC1yc2E'+self.random_value(30)
        new_data = {"label": new_label,"publickey": publickey}
        response = self.client_1.api.RegisterUserPublicKey(new_data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get publickeys - should succeed with 200')
        response = self.client_1.api.GetUserPublicKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data, response.json())
        self.assertIn(new_data, response.json())

        self.lg('[GET] Get publickey by label - should succeed with 200')
        label = response.json()[-1]['label']
        response = self.client_1.api.GetUserPublicKeyByLabel(label, self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data, response.json())

        self.lg('[POST] Register a new publickey with existing label - should fail with 409')
        response = self.client_1.api.GetUserPublicKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        new_label = response.json()[-1]['label']
        new_publickey = 'ssh-rsa AAAAB3NzaC1yc2E'+self.random_value(30)
        new_data = {"label": new_label,"publickey": new_publickey}
        response = self.client_1.api.RegisterUserPublicKey(new_data, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[POST] Register a new publickey with invalid inputs - should fail with 400')
        new_label = self.random_value()
        new_publickey = self.random_value(30)
        new_data = {"label": new_label,"publickey": new_publickey}
        response = self.client_1.api.RegisterUserPublicKey(new_data, self.user_1)
        self.assertEqual(response.status_code, 400)

        self.lg('[PUT] Edit publickey - should succeed with 201')
        response = self.client_1.api.GetUserPublicKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = self.random_value()
        new_publickey = 'ssh-rsa AAAAB3NzaC1yc2E'+self.random_value(30)
        new_data = {"label": new_label,"publickey": new_publickey}
        response = self.client_1.api.UpdateUserPublicKey(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[PUT] Edit publickey with exisiting label- should fail with 409')
        response = self.client_1.api.GetUserPublicKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = response.json()[-2]['label']
        new_publickey = 'ssh-rsa AAAAB3NzaC1yc2E'+self.random_value(30)
        new_data = {"label": new_label,"publickey": new_publickey}
        response = self.client_1.api.UpdateUserPublicKey(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[PUT] Edit publickey with invalid inputs - should fail with 400')
        response = self.client_1.api.GetUserPublicKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = self.random_value()
        new_publickey = self.random_value(30)
        new_data = {"label": new_label,"publickey": new_publickey}
        response = self.client_1.api.UpdateUserPublicKey(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 400)

        self.lg('[DELETE] Delete publickey - should succeed with 204')
        response = self.client_1.api.GetUserPublicKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserPublicKey(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete publickey again - should succeed with 204')
        response = self.client_1.api.GetUserPublicKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserPublicKey(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetUserPublicKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        self.lg('[DELETE] Delete invalid publickey - should fail with 404')
        response = self.client_1.api.DeleteUserPublicKey('fake_publickey', self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('bugs : #402 #403 #404 #405')
    def test009_get_post_put_delete_apikeys(self):

        """
        #Test 009 [APIKEYS]
        - [POST] Add a new apikey for the user - should succeed with 201
        - [POST] Add a new apikey for the user again - should succeed with 201
        - [POST] Add a new apikey with existing label - should fail with 409
        - [GET] List user\'s apikeys - should succeed with 200
        - [GET] Get apikey by label - should succeed with 200
        - [POST] Add a new apikey with the same label of the previous apikey - should fail with 409
        - [PUT] Update the apikey\'s label - should succeed with 201
        - [PUT] Update the apikey\'s label with existing label - should fail with 409
        - [DEL] Delete valid apikey - should succeed with 204
        - [DEL] Delete valid apikey again - should succeed with 204
        - [DEL] Delete apikey with fake label, should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('[POST] Add a new apikey - should succeed with 201')
        label = self.random_value()
        data = {'label' : label}
        response = self.client_1.api.AddApiKey(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Add a new apikey again - should succeed with 201')
        new_label = self.random_value()
        new_data = {'label' : new_label}
        response = self.client_1.api.AddApiKey(new_data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] List user\'s apikeys, should succeed with 200')
        response = self.client_1.api.ListAPIKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data, response.json())
        self.assertIn(new_data, response.json())

        self.lg('[GET] Get apikey by label - should succeed with 200')
        label = response.json()[-1]['label']
        response = self.client_1.api.GetAPIkey(label, self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data, response.json())

        #bug #402
        self.lg('[POST] Add a new apikey with the same label of the previous apikey, should fail with 409')
        new_label = response.json()[-1]['label']
        new_data = {'label' : new_label}
        response = self.client_1.api.AddApiKey(new_data, self.user_1)
        self.assertEqual(response.status_code, 409)

        #bug #404
        self.lg('[PUT] Update the apikey\'s label, should succeed with 201')
        response = self.client_1.api.ListAPIKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = self.random_value()
        new_data = {'label': new_label}
        response = self.client_1.api.UpdateAPIkey(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 201)

        #bug #403
        self.lg('[PUT] Update the apikey\'s label with existing label, should fail with 409')
        response = self.client_1.api.ListAPIKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        new_label = response.json()[-2]['label']
        data = {'label': new_label}
        response = self.client_1.api.UpdateAPIkey(data, label, self.user_1)
        self.assertEqual(response.status_code, 409)

        #bug #405
        self.lg('[DELETE] Delete valid apikey - should succeed with 204')
        response = self.client_1.api.ListAPIKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteAPIkey(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete valid apikey again - should succeed with 204')
        response = self.client_1.api.ListAPIKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteAPIkey(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.ListAPIKeys(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        self.lg('[DELETE] Delete apikey with fake label, should fail with 404')
        response = self.client_1.api.DeleteAPIkey('fake_label', self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('bug: #407')
    def test010_get_post_put_delete_digitalwallet(self):
        """
            #Test 010 [DIGITALWALLET]
            - [POST] Register a new digital wallet - should succeed with 201
            - [POST] Register a new digital wallet again - should succeed with 201
            - [GET] Get digital wallet by label - should succeed with 200
            - [GET] Get digital wallet - should succeed with 200
            - [POST] Register a new digital wallet with existing label - should fail with 409
            - [POST] Register a new digital wallet with invalid inputs - should fail with 400
            - [PUT] Edit digital wallet - should succeed with 201
            - [PUT] Edit digital wallet with exisiting label- should fail with 409
            - [PUT] Edit digital wallet with invalid inputs - should fail with 400
            - [DEL] Delete digital wallet - should succeed with 204
            - [DEL] Delete digital wallet again - should succeed with 204
            - [DEL] Delete invalid digital wallet - should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('[POST] Register a new digital wallet - should succeed with 201')
        label = self.random_value()
        data = {"currencysymbol": self.random_value(),
                "address": self.random_value(),
                "label": label,
                "expire": "2018-01-16T15:35:14.507Z",
                "noexpiration": False}
        response = self.client_1.api.RegisterDigitalWallet(data, self.user_1)
        self.assertEqual(response.status_code, 201)


        self.lg('[POST] Register a new digital wallet again - should succeed with 201')
        new_label = self.random_value()
        new_data =  {"currencysymbol": self.random_value(),
                    "address": self.random_value(),
                    "label": new_label,
                    "noexpiration": True}
        response = self.client_1.api.RegisterDigitalWallet(new_data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get digital wallet by label - should succeed with 200')
        response = self.client_1.api.GetUserDigitalWalletByLabel(label, self.user_1)
        self.assertEqual(response.status_code, 200)

        self.lg('[GET] Get digital wallet - should succeed with 200')
        response = self.client_1.api.GetUserDigitalWallets(self.user_1)
        self.assertEqual(response.status_code, 200)

        self.lg('[POST] Register a new digital wallet with existing label - should fail with 409')
        label = response.json()[randint(0, len(response.json())-1)]['label']
        data['label'] = label
        response = self.client_1.api.RegisterDigitalWallet(data, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[POST] Register a new digital wallet with invalid inputs - should fail with 400')
        label = self.random_value()
        data['label'] = label
        data['expire'] = self.random_value()
        response = self.client_1.api.RegisterDigitalWallet(data, self.user_1)
        self.assertEqual(response.status_code, 400)

        self.lg('[PUT] Edit digital wallet - should succeed with 201')
        response = self.client_1.api.GetUserDigitalWallets(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[randint(0, len(response.json())-1)]['label']
        new_label = self.random_value()
        new_data = {"currencysymbol": self.random_value(),
                    "address": self.random_value(),
                    "label": new_label,
                    "expire": "2018-01-16T15:35:14.507Z",
                    "noexpiration": False}
        response = self.client_1.api.UpdateUserDigitalWallet(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 201)

        # bug #407
        self.lg('[PUT] Edit digital wallet with exisiting label- should fail with 409')
        response = self.client_1.api.GetUserDigitalWallets(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[0]['label']
        new_label = response.json()[1]['label']
        new_data = {"currencysymbol": self.random_value(),
                    "address": self.random_value(),
                    "label": new_label,
                    "expire": "2018-01-16T15:35:14.507Z",
                    "noexpiration": False}
        response = self.client_1.api.UpdateUserDigitalWallet(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[PUT] Edit digital wallet with invalid inputs - should fail with 400')
        response = self.client_1.api.GetUserDigitalWallets(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[randint(0, len(response.json())-1)]['label']
        new_label = self.random_value()
        new_data = {"currencysymbol": self.random_value(),
                    "address": self.random_value(),
                    "label": new_label,
                    "expire": self.random_value(),
                    "noexpiration": False}
        response = self.client_1.api.UpdateUserDigitalWallet(new_data, label, self.user_1)
        self.assertEqual(response.status_code, 400)

        self.lg('[DELETE] Delete digital wallet - should succeed with 204')
        response = self.client_1.api.GetUserDigitalWallets(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserDigitalWallet(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete digital wallet again - should succeed with 204')
        response = self.client_1.api.GetUserDigitalWallets(self.user_1)
        self.assertEqual(response.status_code, 200)
        label = response.json()[-1]['label']
        response = self.client_1.api.DeleteUserDigitalWallet(label, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetUserDigitalWallets(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        self.lg('[DELETE] Delete invalid digital wallet - should fail with 404')
        response = self.client_1.api.DeleteUserDigitalWallet('fake_digital_wallet', self.user_1)
        self.assertEqual(response.status_code, 404)

    @unittest.skip('bug #411 #414')
    def test011_get_post_delete_organizations_auth(self):

        """
            #Test 011 [ORGANIZATION & AUTH]

        """
        self.lg('%s STARTED' % self._testID)

        response = self.client_1.api.GetUserOrganizations(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.organization_1, response.json()['owner'])

        for role in ['member', 'owner']:

            self.lg('[POST] Send invitation to user_2 to join org_1 role %s, should succeed with 201' % role)
            data = {'searchstring': self.user_2}
            if role =="member":
                response = self.client_1.api.AddOrganizationMember(data, self.organization_1)
            elif role == "owner":
                response = self.client_1.api.AddOrganizationOwner(data, self.organization_1)
            self.assertEqual(response.status_code, 201)

            response = self.client_2.api.GetNotifications(self.user_2)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.organization_1, response.json()['invitations'][-1]['organization'])
            self.assertEqual(role, response.json()['invitations'][-1]['role'])
            self.assertEqual('pending', response.json()['invitations'][-1]['status'])

            self.lg('[DELETE] Reject the invitation, should succeed with 204')
            response = self.client_2.api.RejectMembership(self.organization_1, role, self.user_2)
            self.assertEqual(response.status_code, 204)
            response = self.client_2.api.GetUserOrganizations(self.user_2)
            self.assertNotIn(self.organization_1, response.json()[role])

            self.lg('[POST] Send invitation to user_2 to join org_1 role %s again, should succeed with 201' % role)
            data = {'searchstring': self.user_2}
            if role =="member":
                response = self.client_1.api.AddOrganizationMember(data, self.organization_1)
            elif role == "owner":
                response = self.client_1.api.AddOrganizationOwner(data, self.organization_1)
            self.assertEqual(response.status_code, 201)

            response = self.client_2.api.GetNotifications(self.user_2)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.organization_1, response.json()['invitations'][-1]['organization'])
            self.assertEqual(role, response.json()['invitations'][-1]['role'])
            self.assertEqual('pending', response.json()['invitations'][-1]['status'])

            self.lg('[POST] Accept the invitation, should succeed with 201')
            response = self.client_2.api.AcceptMembership(data, self.organization_1, role, self.user_2)
            self.assertEqual(response.status_code, 201)
            response = self.client_2.api.GetUserOrganizations(self.user_2)
            self.assertIn(self.organization_1, response.json()[role])

            self.lg('[PUT] Modify certain information for user_2 to be granted to  organization_1 - should succeed')

            response = self.client_2.api.GetEmailAddresses(self.user_1)
            self.assertEqual(response.status_code, 200)
            label = response.json()[0]['label']

            grantedto = self.organization_1
            data = {"username":self.user_2,
                    "grantedTo":grantedto,
                    "emailaddresses":[{"requestedlabel": self.random_value(), "reallabel": "main"}]}

            response = self.client_2.api.UpdateAuthorization(data, grantedto, self.user_2)
            self.assertEqual(response.status_code, 201)

            self.lg('[GET] Get all Authorizations of user - should succeed with 200')
            response = self.client_2.api.GetAllAuthorizations(self.user_2)
            self.assertEqual(response.status_code, 200)

            self.lg('[GET] Get the Authorizations of user for specific organization - should succeed with 200')
            response = self.client_2.api.GetAuthorization(grantedto, self.user_2)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(grantedto, response.json()['grantedTo'])
            self.assertIn('emailaddresses', response.json())

            self.lg('[DELETE] Remove the authorization for the organization_1 - should succeed with 204')
            response = self.client_2.api.DeleteAuthorization(grantedto, self.user_2)
            self.assertEqual(response.status_code, 204)

            response = self.client_2.api.GetAuthorization(grantedto, self.user_2)
            self.assertEqual(response.status_code, 404)

            response = self.client_2.api.GetAllAuthorizations(self.user_2)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), [])

            self.lg('[DELETE] Leave an organization, should succeed with 204')
            response = self.client_2.api.LeaveOrganization(self.organization_1, self.user_2)
            self.assertEqual(response.status_code, 204)
            response = self.client_2.api.GetUserOrganizations(self.user_2)
            self.assertNotIn(self.organization_1, response.json()[role])

            #bug 411
            self.lg('[DELETE] Leave an organization, with unothorized user should fail with 401')
            response = self.client_1.api.LeaveOrganization(self.organization_2, self.user_2)
            self.assertEqual(response.status_code, 401)

            self.lg('[DELETE] Leave an fake organization, should fail with 404')
            response = self.client_2.api.LeaveOrganization('fake_organization', self.user_2)
            self.assertEqual(response.status_code, 404)

            #bug 414
            self.lg('[DELETE] Leave an fake user, should fail with 404')
            response = self.client_2.api.LeaveOrganization(self.organization_1, 'fake_user')
            self.assertEqual(response.status_code, 404)

    def test012_get_post_delete_totp_twofamethods(self):
        """
            #Test 012 [TOTP]
            - [GET]  totp secret - should succeed with 200
            - [POST] Set totp code with invalid secret - should fail with 422
            - [POST] Set totp code with valid code - should succeed with 204
            - [DEL]  Delete - should fail with 409
            - [POST] Register a new phonenumber & send validation sms - should succeed with 201 & 200
            - [DEL]  Delete totp - should succeed with 204
            - [POST] Set totp code with valid code again - should succeed with 204
            - [POST] Set totp code with valid secret and invalid code - should fail with 422'
            - [POST] Register a new phonenumber & send validation sms - should succeed with 201 & 200
            - [POST] Set totp code with valid code again - should succeed with 204 (to be able to access the account again)
        """

        self.lg('[GET] totp secret - should succeed with 200')
        response = self.client_1.api.GetTotp(self.user_1)
        self.assertEqual(response.status_code, 200)

        self.lg('[POST] Set totp code with invalid secret - should fail with 422')
        new_secret = self.random_value()
        totpcode = self.random_value()
        data = {"totpcode":totpcode, "totpsecret":new_secret}
        response = self.client_1.api.EditTotp(data, self.user_1)
        self.assertEqual(response.status_code, 422)

        self.lg('[POST] Set totp code with valid secret and invalid code - should fail with 422')
        response = self.client_1.api.GetTotp(self.user_1)
        self.assertEqual(response.status_code, 200)
        new_secret = response.json()['totpsecret']
        totpcode = self.random_value()
        data = {"totpcode":totpcode, "totpsecret":new_secret}
        response = self.client_1.api.EditTotp(data, self.user_1)
        self.assertEqual(response.status_code, 422)

        self.lg('[POST] Set totp code with valid code - should succeed with 204')
        response = self.client_1.api.GetTotp(self.user_1)
        self.assertEqual(response.status_code, 200)
        new_secret = response.json()['totpsecret']
        totpcode = self.get_totp_code(new_secret)
        data = {"totpcode":totpcode, "totpsecret":new_secret}
        response = self.client_1.api.EditTotp(data, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetTwofamethods(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['totp'])

        self.lg('[DEL] Delete - should fail with 409')
        response = self.client_1.api.DeleteTotp(self.user_1)
        self.assertEqual(response.status_code, 409)

        self.lg('[POST] Register a new phonenumber & send validation sms - should succeed with 201 & 200')
        label = 'validation number'
        phonenumber = self.get_valid_phonenumber()
        data = {"label":label, "phonenumber":phonenumber}
        response = self.client_1.api.RegisterNewUserPhonenumber(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        response = self.client_1.api.ValidatePhonenumber(label, self.user_1)
        self.assertEqual(response.status_code, 200)
        validationkey = response.json()['validationkey']
        time.sleep(25)
        smscode = self.get_mobile_verification_code()
        data = {"smscode":smscode, "validationkey":validationkey}
        response = self.client_1.api.VerifyPhoneNumber(data, label, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetUserPhoneNumbers(self.user_1, query_params={'validated':True})
        self.assertEqual(response.status_code, 200)
        self.assertIn(label, [x['label'] for x in response.json()])

        self.lg('[DEL] Delete totp - should succeed with 204')
        response = self.client_1.api.DeleteTotp(self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetTwofamethods(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['sms'])

        self.lg('[POST] Set totp code with valid code again - should succeed with 204')
        new_secret = '3OK7Y5WNBS3NO5TZN2SY3BFMRH42YL52'
        totpcode = self.get_totp_code(new_secret)
        data = {"totpcode":totpcode, "totpsecret":new_secret}
        response = self.client_1.api.EditTotp(data, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetTwofamethods(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['totp'])

        self.lg('[DELETE] Force Delete verified phonenumber - should succeed with 204')
        response = self.client_1.api.DeleteUserPhonenumber(label, self.user_1, query_params={'force':'true'})
        self.assertEqual(response.status_code, 204)

    def test014_delete_facebook_account(self):

        """
            #Test 014 [FACEBOK]
            - [GET] Check if facebook account exists or not, should succeed with 200
            - [Del] Delete facebook account if exists , should succeed with 204
            - [GET] Check if the facebook account is deleted, should succeed with 200
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('Check if facebook account exists or not , should succeed')
        response = self.client_1.api.GetUser(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('facebook', response.json().keys())
        self.assertEqual(type(response.json()['facebook']), types.DictType)
        empty_account = {'id':'', 'link':'', 'name':'', 'picture':''}

        if response.json()['facebook'] != empty_account:
            self.lg('Delete facebook account, should succeed')
            response = self.client_1.api.DeleteFacebookAccount(self.user_1)
            self.assertEqual(response.status_code, 204)
            self.lg('Check if the facebook account is deleted, should succeed')
            response = self.client_1.api.GetUser(self.user_1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['facebook'], empty_account)
        else:
            self.lg('facebook account is already deleted')

        self.lg('%s ENDED' % self._testID)

    def test015_delete_github_account(self):
        """
            #Test 015 [GITHUB]
            - [GET] Check if github account exists or not, should succeed with 200
            - [Del] Delete github account if exists , should succeed with 204
            - [GET] Check if the github account is deleted, should succeed with 200
        """

        self.lg('%s STARTED' % self._testID)

        self.lg('Check if github account exists, should succeed')
        response = self.client_1.api.GetUser(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('github', response.json().keys())
        self.assertEqual(type(response.json()['github']), types.DictType)
        empty_account = {u'avatar_url': u'', u'html_url': u'', u'id': 0, u'login': u'', u'name': u''}

        if response.json()['github'] != empty_account:
            self.lg('Delete github account, should succeed')
            response = self.client_1.api.DeleteGithubAccount(username=self.user_1)
            self.assertEqual(response.status_code, 204)
            self.lg('Check if the github account is deleted, should succeed')
            response = self.client_1.api.GetUser(self.user_1)
            self.assertEqual(response.status_code, 200)
            self.assertIn('github', response.json().keys())
            self.assertEqual(type(response.json()['github']), types.DictType)
            self.assertEqual(response.json()['github'], empty_account)
        else:
            self.lg('github account is already deleted')

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('bug: #412')
    def test016_get_user_info(self):
        """
            #Test 016 [INFO]
            - [GET] Get user info - should succeed with 200
        """
        self.lg('%s STARTED' % self._testID)

        self.lg('[GET] Get user info - should succeed with 200')
        response = self.client_1.api.GetUserInformation(self.user_1)
        self.assertEqual(response.status_code, 200)

        self.lg('%s ENDED' % self._testID)

    @unittest.skip('bug 411')
    def test017_create_contract(self):
        """
        #Test 017 [CONTRACT]
        - [GET]
        - [POST] Create a new contract, should succeed
        - [POST] Create an new contract with unauthorized user, should fail with 404 (not implemented yet)
        """
        self.lg('[GET] user contracts - should succeed with 200')
        response = self.client_1.api.GetUserContracts(self.user_1)
        self.assertEqual(response.status_code, 200)

        self.lg('Create a new contract - should succeed with 201')
        contractid = self.random_value()
        expire = '2019-10-02T22:00:00Z'
        data = {'content':'test', 'contractId':contractid, 'contractType':'partnership',
                'expires':expire, 'parties':[{'name':'', 'type':''}],
                'signatures':[{'date':'2018-10-02T22:00:00Z', 'publicKey':'asdasd', 'signature':'asdasd', 'signedBy':'asdasd'}]}
        response = self.client_1.api.CreateUserContract(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('Create a new contract with unauthorized user - should fail with 401')
        contractid = self.random_value()
        expire = '2019-10-02T22:00:00Z'
        data = {'content':'test', 'contractId':contractid, 'contractType':'partnership',
                'expires':expire, 'parties':[{'name':'', 'type':''}],
                'signatures':[{'date':'2018-10-02T22:00:00Z', 'publicKey':'asdasd', 'signature':'asdasd', 'signedBy':'asdasd'}]}
        response = self.client_1.api.CreateUserContract(data, self.user_2)
        self.assertEqual(response.status_code, 401)

    @unittest.skip('bug: #413')
    def test018_get_post_delete_registry(self):

        """
            #Test 018 [REGISTRY]
            - [POST] Register a new registry - should succeed with 201
            - [POST] Register a new registry again - should succeed with 201.
            - [GET] Get user registries - should succeed with 200
            - [GET] Get registry by key - should succeed with 200
            - [GET] Get invalid registry - should fail with 404
            - [POST] Register a new registry with existing key - should fail with 409
            - [POST] Register a new registry with invalid inputs - should fail with 400
            - [DEL] Delete registry - should succeed with 204
            - [DEL] Delete registry again - should succeed with 204
            - [DEL] Delete invalid registry - should fail with 404
        """

        self.lg('%s STARTED' % self._testID)

        #bug #413
        self.lg('[POST] Register a new registry - should succeed with 201')
        key = self.random_value()
        value = self.random_value()
        data = {"Key": key,"Value": value}
        response = self.client_1.api.CreateNewRegistry(data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[POST] Register a new registry again - should succeed with 201')
        key = self.random_value()
        value = self.random_value()
        new_data = {"Key": key,"Value": value}
        response = self.client_1.api.CreateNewRegistry(new_data, self.user_1)
        self.assertEqual(response.status_code, 201)

        self.lg('[GET] Get user registries - should succeed with 200')
        response = self.client_1.api.GetRegistries(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data, response.json())
        self.assertIn(new_data, response.json())

        self.lg('[GET] Get registry by key - should succeed with 200')
        key = response.json()[-1]['Key']
        response = self.client_1.api.GetRegistry(key, self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data, response.json())

        self.lg('[GET] Get invalid registry - should fail with 404')
        response = self.client_1.api.GetRegistry('fake_key', self.user_1)
        self.assertEqual(response.status_code, 404)

        self.lg('[POST] Register a new registry with existing key - should fail with 409')
        response = self.client_1.api.GetRegistries(self.user_1)
        self.assertEqual(response.status_code, 200)
        key = response.json()[-1]['Key']
        value = self.random_value()
        new_data = {"Key": key,"Value": value}
        response = self.client_1.api.CreateNewRegistry(new_data, self.user_1)
        self.assertEqual(response.status_code, 409)


        self.lg('[POST] Register a new registry with invalid inputs - should fail with 400')
        key = ''
        value = ''
        new_data = {"Key": key,"Value": value}
        response = self.client_1.api.CreateNewRegistry(new_data, self.user_1)
        self.assertEqual(response.status_code, 400)

        self.lg('[DELETE] Delete registry - should succeed with 204')
        response = self.client_1.api.GetRegistries(self.user_1)
        self.assertEqual(response.status_code, 200)
        key = response.json()[-1]['Key']
        response = self.client_1.api.DeleteRegistry(key, self.user_1)
        self.assertEqual(response.status_code, 204)

        self.lg('[DELETE] Delete registry again - should succeed with 204')
        response = self.client_1.api.GetRegistries(self.user_1)
        self.assertEqual(response.status_code, 200)
        key = response.json()[-1]['Key']
        response = self.client_1.api.DeleteRegistry(key, self.user_1)
        self.assertEqual(response.status_code, 204)

        response = self.client_1.api.GetRegistries(self.user_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        self.lg('[DELETE] Delete invalid registry - should fail with 404')
        response = self.client_1.api.DeleteRegistry('fake_key', self.user_1)
        self.assertEqual(response.status_code, 404)
