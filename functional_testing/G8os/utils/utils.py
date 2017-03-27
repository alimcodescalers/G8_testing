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

    def get_process_id(self, cmd, match):
        """
        Get the id of certain process
        :param cmd: command used by the client (same as the command in process.list) ex: 'core.system'
        :param match: string to match intended command. ex: 'sleep 300'
        """
        time.sleep(3)
        processes = self.client.process.list()
        for p in processes:
           if p['cmd']['command'] == cmd:
              if cmd == 'core.system':
                 if p['cmd']['arguments']['name'] == match:
                    return p['cmd']['id']
              if cmd == 'bash':
                 if p['cmd']['arguments']['script'] == match:
                    return p['cmd']['id']
        return

    def stdout(self, resource):
        return resource.get().stdout.replace('\n', '').lower()

