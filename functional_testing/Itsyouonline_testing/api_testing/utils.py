import logging
import unittest
import time
import os

from testconfig import config

from testframework import base

class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.env_url = config['main']['env_url']
        self.applicationid = config['main']['applicationid']
        self.secret = config['main']['secret']
        self.user = config['main']['user']

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('itsyouonline_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.client = base.Client(self.env_url)
        self.client.oauth.login_via_client_credentials(client_id=self.applicationid,
                                                       client_secret=self.secret)


    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s ExecutionTime is %s sec.' % (self._testID, executionTime))

    def lg(self, msg):
        self._logger.info(msg)