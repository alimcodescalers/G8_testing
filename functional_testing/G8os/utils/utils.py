import g8core
import unittest
import time
import uuid
import logging
import configparser
import requests


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.target_ip = config['main']['target_ip']
        self.zt_access_token = config['main']['zt_access_token']
        self.client = g8core.Client(self.target_ip)
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'Bearer {}'.format(self.zt_access_token)
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

    def check_g8os_connection(self, classname):
        try:
            self.client.ping()
        except Exception as e:
            self.lg("can't reach g8os remote machine")
            print("Can't reach g8os remote machine")
            self.skipTest(classname)


    def rand_str(self):
        return str(uuid.uuid4()).replace('-', '')[1:10]

    def get_process_id(self, cmd, match):
        """
        Get the id of certain process
        :param cmd: command used by the client (same as the command in process.list) ex: 'core.system'
        :param match: string to match intended command. ex: 'sleep 300'
        """
        time.sleep(2)
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

    def getZtNetworkID(self):
        url = 'https://my.zerotier.com/api/network'
        r = self.session.get(url)
        if r.status_code == 200:
            for item in r.json():
                if item['type'] == 'Network':
                    return item['id']
            else:
                self.lg('can\'t find network id')
                return False
        else:
            self.lg('can\'t connect to zerotier, {}:{}'.format(r.status_code, r.content))
            return False

    def getZtNetworkOnlineMembers(self, networkId):
        url = 'https://my.zerotier.com/api/network/{}'.format(networkId)
        r = self.session.get(url)
        if r.status_code == 200:
            return r.json()['onlineMemberCount']
        else:
            self.lg('can\'t connect to zerotier, {}:{}'.format(r.status_code, r.content))
            return False
