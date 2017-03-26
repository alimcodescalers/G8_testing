import g8core
import unittest


#cl = g8core.Client('172.17.0.2')


class Client:
    def __init__(self, ip):
        self.client = g8core.Client(ip)


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        ip = '172.17.0.2'
        self.client = Client(ip)
        import ipdb; ipdb.set_trace()
        super(BaseTest, self).__init__(*args, **kwargs)

    def setup(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('openvcloud_testsuite'),
                                             {'testid': self.shortDescription() or self._testID})

    def teardown(self):
        pass
