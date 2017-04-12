import g8core

class Client:
    def __init__(self, ip):
        self.client = g8core.Client(ip)

    def stdout(self, resource):
        return resource.get().stdout.replace('\n', '').lower()

    def get_node_cpus(self):
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

    def get_node_nics(self):
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

    def get_node_bridges(self):
        bridgesInfo = []
        nics = self.client.bash('ls /sys/class/net').get().stdout.splitlines()
        for nic in nics:
            status = self.client.bash('cat /sys/class/net/{}/operstate'.format(nic)).get().stdout.strip()
            bridge = {"name":nic, "status":status, "config":""}
            bridgesInfo.append(bridge)

        return bridgesInfo

    def get_node_mem(self):
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

    def get_node_info(self):
        hostname = self.client.system('uname -n').get().stdout.strip()
        krn_name = self.client.system('uname -s').get().stdout.strip().lower()
        return {"hostname":hostname, "kernel":krn_name}

    def get_node_disks(self):
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
