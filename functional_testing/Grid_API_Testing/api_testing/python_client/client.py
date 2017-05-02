import g8core
import time

class Client:
    def __init__(self, ip):
        self.client = g8core.Client(ip)

    def stdout(self, resource):
        return resource.get().stdout.replace('\n', '').lower()

    def get_nodes_cpus(self):
        lines = self.client.bash('cat /proc/cpuinfo').get().stdout.splitlines()
        cpuInfo = []
        cpuInfo_format = {'family': "", 'cacheSize': "", 'mhz': "", 'cores': "", 'flags': ""}
        for line in lines:
            line = line.replace('\t', '').strip()
            key = line[:line.find(':')]
            value = line[line.find(':')+2:]
            if key == 'processor':
                cpuInfo.append(dict(cpuInfo_format))
            if key == 'cpu family':
                cpuInfo[-1]['family'] = value
            elif key == 'cache size':
                cpuInfo[-1]['cacheSize'] = int(value[:value.index(' KB')])
            elif key == 'cpu MHz':
                cpuInfo[-1]['mhz'] = value
            elif key == 'cpu cores':
                cpuInfo[-1]['cores'] = int(value)
            elif key == 'flags':
                cpuInfo[-1]['flags'] = value.split(' ')
        return cpuInfo

    def get_nodes_nics(self):
        r = self.client.bash('ip -br a').get().stdout
        nics = [x.split()[0] for x in r.splitlines()]
        nicInfo = []
        for nic in nics:
            if '@' in nic:
                nic = nic[:nic.index('@')]
            addrs = self.client.bash('ip -br a show "{}"'.format(nic)).get()
            addrs = addrs.stdout.splitlines()[0].split()[2:]
            mtu = int(self.stdout(self.client.bash('cat /sys/class/net/{}/mtu'.format(nic))))
            hardwareaddr = self.stdout(self.client.bash('cat /sys/class/net/{}/address'.format(nic)))
            if hardwareaddr == '00:00:00:00:00:00':
                    hardwareaddr = ''
            tmp = {"name": nic, "hardwareaddr": hardwareaddr, "mtu": mtu, "addrs": [{"addr": x} for x in addrs]}
            nicInfo.append(tmp)

        return nicInfo

    def get_nodes_bridges(self):
        bridgesInfo = []
        nics = self.client.bash('ls /sys/class/net').get().stdout.splitlines()
        for nic in nics:
            status = self.client.bash('cat /sys/class/net/{}/operstate'.format(nic)).get().stdout.strip()
            bridge = {"name":nic, "status":status, "config":""}
            bridgesInfo.append(bridge)

        return bridgesInfo

    def get_nodes_mem(self):
        lines = self.client.bash('cat /proc/meminfo').get().stdout.splitlines()
        memInfo = { 'active': 0, 'available': 0, 'buffers': 0, 'cached': 0,
                    'free': 0,'inactive': 0, 'total': 0}
        for line in lines:
            line = line.replace('\t', '').strip()
            key = line[:line.find(':')].lower()
            value = line[line.find(':')+2:line.find('kB')].strip()
            if 'mem' == key[:3]:
                key = key[3:]
            if key in memInfo.keys():
                memInfo[key] = int(value)
        return memInfo

    def get_nodes_info(self):
        hostname = self.client.system('uname -n').get().stdout.strip()
        krn_name = self.client.system('uname -s').get().stdout.strip().lower()
        return {"hostname":hostname, "kernel":krn_name}

    def get_nodes_disks(self):
        diskInfo = {'mountpoint': [], 'fstype': [], 'device': [], 'opts': []}
        response = self.client.bash('mount').get().stdout
        lines = response.splitlines()
        for line in lines:
            line = line.split()
            diskInfo['mountpoint'].append(line[2])
            diskInfo['fstype'].append(line[4])
            diskInfo['device'].append(line[0])
            diskInfo['opts'].append(line[5][1:-1])

        return diskInfo

    def get_container_info(self, container_id):
        container_id = list(self.client.container.find(container_id).keys())[0]
        container_info = {}
        golden_data = self.client.container.list().get(str(container_id), None)
        if not golden_data:
            return False
        golden_value = golden_data['container']
        container_info['nics'] = ([{i: nic[i] for i in nic if i != 'hwaddr'} for nic in golden_value['arguments']['nics']])
        container_info['ports'] = (['%s:%s' % (key, value) for key, value in golden_value['arguments']['port'].items()])
        container_info['hostNetworking'] = golden_value['arguments']['host_network']
        container_info['hostname'] = golden_value['arguments']['hostname']
        container_info['flist'] = golden_value['arguments']['root']
        container_info['storage'] = golden_value['arguments']['storage']
        return container_info

    def get_container_job_list(self, container_name):
        container_id = list(self.client.container.find(container_name).keys())[0]
        golden_values = []
        container = self.client.container.client(int(container_id))
        container_data = container.job.list()
        # cannot compare directly as the job.list is considered a job and has a different id everytime is is called
        for i, golden_value in enumerate(container_data[:]):
            if golden_value.get('command', "") == 'job.list':
                container_data.pop(i)
                continue
            golden_values.append((golden_value['cmd']['id'], golden_value['starttime']))
        return set(golden_values)

    def wait_on_container_update(self, container_name, timeout, removed):
        for _ in range(timeout):
            if removed:
                if not self.client.container.find(container_name):
                    return True
            else:
                if self.client.container.find(container_name):
                    return True
            time.sleep(1)
        return False

    def wait_on_container_job_update(self, container_name, job_id, timeout, removed):
        container_id = int(list(self.client.container.find(container_name).keys())[0])
        container = self.client.container.client(container_id)
        for _ in range(timeout):
            if removed:
                if job_id not in [item['cmd']['id']for item in container.job.list()]:
                    return True
            else:
                if job_id in [item['cmd']['id']for item in container.job.list()]:
                    return True
            time.sleep(1)
        return False
