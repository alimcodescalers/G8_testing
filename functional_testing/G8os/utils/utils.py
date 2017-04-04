import g8core
import unittest
import time
import uuid
import logging
import configparser


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.target_ip = config['main']['target_ip']
        self.client = g8core.Client(self.target_ip)
        self.client.timeout = 60
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

    def deattach_all_loop_devices(self):
        self.client.bash('modprobe loop')  # to make /dev/loop* available
        self.client.bash('umount --force /dev/loop*')  # Make sure to free all loop devices first
        for i in range(8):
            self.client.bash('losetup -d /dev/loop{}'.format(i))  # deattach all devices

    def setup_loop_devices(self, files_names, file_size, files_loc='/', deattach=False):
        """
        :param files_names: list of files names to be truncated
        :param file_size: the file size (ex: 1G)
        :param files_loc: abs path for the files (ex: /)
        :param deattach: if True, deattach all loop devices
        """
        if deattach:
            self.deattach_all_loop_devices()
        loop_devs = []
        for f in files_names:
            self.client.bash('cd {}; truncate -s {} {}'.format(files_loc, file_size, f))
            output = self.client.bash('losetup -f')
            free_l_dev = self.stdout(output)
            self.client.bash('losetup {} {}{}'.format(free_l_dev, files_loc, f))
            loop_devs.append(free_l_dev)
            self.client.bash('rm -rf {}{}'.format(files_loc, f))
        return loop_devs
