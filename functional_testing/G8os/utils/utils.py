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

    def getCpuInfo(self):
        lines = self.client.bash('cat /proc/cpuinfo').get().stdout.splitlines()
        cpuInfo = { 'vendorId':[], 'family':[], 'stepping': [], 'cpu': [],
            'coreId': [],'model': [], 'cacheSize': [], 'mhz': [], 'cores': [],
            'flags': [], 'modelName':[], 'physicalId':[]}   

        mapping = { "vendor_id":"vendorId", "cpu family":"family", "processor":"cpu", "core id":"coreId", "cache size":"cacheSize",
                    "cpu MHz":"mhz", "cpu cores":"cores", "model name":"modelName", "physical id":"physicalId", "stepping":"stepping",
                    "flags":"flags", "model": "model"}

        keys = mapping.keys()
        for line in lines:
                line = line.replace('\t', '')
                for key in keys:
                	if key == line[:line.find(':')]:
                                item = line[line.index(':')+1:].strip()
                                if key in ['processor', 'stepping', 'cpu cores']:
                                        item = int(item)
                                if key == "cpu MHz":
                                        item = float(item)
                                if key == 'cache size':
                                        item = int(item[:item.index(' KB')])
                                if key == 'flags':
                                        item = item.split(' ')
                                cpuInfo[mapping[key]].append(item)

        return cpuInfo

    def getDiskInfo(self):
        diskInfo = {'mountpoint':[] , 'fstype':[], 'device':[] , 'opts':[]}
        response = self.client.bash('mount').get().stdout
        lines = response.splitlines()
        for line in lines:
                 line = line.split()
                 diskInfo['mountpoint'].append(line[2])
                 diskInfo['fstype'].append(line[4])
                 diskInfo['device'].append(line[0])
                 diskInfo['opts'].append(line[5][1:-1])

        return diskInfo
 
    def getNicInfo(self):
         r = self.client.bash('ip -br a').get().stdout
         nics = [x.split()[0] for x in r.splitlines()]
         nicInfo = []
         for nic in nics:
                 if '@' in nic:
                       nic = nic[:nic.index('@')]
                 addrs = self.client.bash('ip -br a | grep -E "{}"'.format(nic)).get().stdout.splitlines()[0].split()[2:]
                 mtu = int(self.stdout(self.client.bash('cat /sys/class/net/{}/mtu'.format(nic))))
                 hardwareaddr = self.stdout(self.client.bash('cat /sys/class/net/{}/address'.format(nic)))
                 if hardwareaddr == '00:00:00:00:00:00':
                        hardwareaddr = ''
                 tmp = {"name":nic, "hardwareaddr":hardwareaddr, "mtu":mtu, "addrs":[{"addr":x} for x in addrs]}
                 nicInfo.append(tmp)
         return nicInfo

 
   



