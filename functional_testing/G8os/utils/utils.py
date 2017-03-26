import g8core
import unittest
import time
import uuid
import logging 
from testconfig import config
import configparser 


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.target_ip = config['main']['target_ip']
        self.client  = g8core.Client(self.target_ip)
        super(BaseTest, self).__init__(*args, **kwargs)

    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('g8os_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})

    def teardown(self):
        pass

    def lg(self, msg):
        self._logger.info(msg)

    def rand_str(self):
        return str(uuid.uuid4()).replace('-','')[1:10]
