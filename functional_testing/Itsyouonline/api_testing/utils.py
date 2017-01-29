import logging
import unittest
import time
import os
import pyotp
import uuid
import email
import imaplib
import mailbox
from bs4 import BeautifulSoup
import requests

from testconfig import config
from testframework import base
# from testframework.email_verification import email_verification

class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.env_url = config['main']['env_url']
        self.applicationid_1 = config['main']['applicationid_1']
        self.applicationid_2 = config['main']['applicationid_2']
        self.secret_1 = config['main']['secret_1']
        self.secret_2 = config['main']['secret_2']
        self.user_1   = config['main']['user_1']
        self.user_2   = config['main']['user_2']
        self.organization_1 = config['main']['organization_1']
        self.validation_email = config['main']['validation_email']
        self.validation_email_password = config['main']['validation_email_password']

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('itsyouonline_testsuite'),{'testid': self.shortDescription() or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.client_1 = base.Client(self.env_url)
        self.client_2 = base.Client(self.env_url)
        self.client_1.oauth.login_via_client_credentials(client_id=self.applicationid_1,client_secret=self.secret_1)
        self.client_2.oauth.login_via_client_credentials(client_id=self.applicationid_2,client_secret=self.secret_2)

    def random_value(self, size=10):
        return str(str(uuid.uuid4())+str(uuid.uuid4())).replace('-', '')[0:size]

    def get_totp_code(self, secret):
        totp = pyotp.TOTP(secret)
        GAuth_code = totp.now()
        return GAuth_code

    def get_valid_phonenumber(self):
        html = requests.get('http://receive-sms-now.com/').content
        html = BeautifulSoup(html, "html.parser")
        html = html.find_all('a')
        numbers =  [x.string for x in html if '+' in x.string]
        links =  [x['href'] for x in html if '+' in x.string]
        for i, number in enumerate(numbers):
            if number[1] == 3:
                self.validation_number = number
                self.validation_number_link = links[i]
                break
        else:
            self.validation_number = numbers[0]
            self.validation_number_link = links[0]

        return self.validation_number


    def get_mobile_verification_code(self):
        html = requests.get('http://receive-sms-now.com/'+self.validation_number_link).content
        html = BeautifulSoup(html, "html.parser")
        rows = html.find_all('table')[1].find_all('tr')[1:]
        for row in rows:
            sms_info =  [x.string for x in row.find_all('td')]
            sms_date = sms_info[1]
            sms_message = sms_info[2]
            if 'To verify your phonenumber on itsyou.online enter the code' in sms_message:
                code = sms_message[sms_message.find('code')+5: sms_message.find('code')+11]
                return code

    def UserValidateEmail(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.validation_email, self.validation_email_password)
        mail.select('itsyouonline')
        result, data = mail.search(None, 'ALL')
        latest_email_id = data[0].split()[-1]
        result, email_data = mail.fetch(latest_email_id, '(UID BODY[TEXT])')
        raw_email = email_data[0][1]
        soup = BeautifulSoup(raw_email, "html.parser")
        validation_link = [x.string for x in soup.find_all('a', href=True)][-1]
        validation_link = validation_link.replace('=3D', '=').replace('=\r\n', '')
        r = requests.get(validation_link)
        return r

    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s ExecutionTime is %s sec.' % (self._testID, executionTime))

    def lg(self, msg):
        self._logger.info(msg)
