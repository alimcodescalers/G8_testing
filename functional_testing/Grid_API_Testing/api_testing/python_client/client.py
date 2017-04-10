import g8core

class Client:
    def __init__(self, ip):
        self.client = g8core.Client(ip)

    def stdout(self, resource):
        return resource.get().stdout.replace('\n', '').lower()

    def get_nic_info(self):
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

    def get_cpu_info(self):

        lines = self.client.bash('cat /proc/cpuinfo').get().stdout.splitlines()
        cpuInfo = {'vendorId': [], 'family': [], 'stepping': [], 'cpu': [], 'coreId': [], 'model': [],
                    'cacheSize': [], 'mhz': [], 'cores': [], 'flags': [], 'modelName': [], 'physicalId':[]}

        mapping = { "vendor_id": "vendorId", "cpu family": "family", "processor": "cpu", "core id": "coreId",
                    "cache size": "cacheSize", "cpu MHz": "mhz", "cpu cores": "cores", "model name": "modelName",
                    "physical id": "physicalId", "stepping": "stepping", "flags": "flags", "model": "model"}

        keys = mapping.keys()
        for line in lines:
            line = line.replace('\t', '')
            for key in keys:
                if key == line[:line.find(':')]:
                    item = line[line.index(':') + 1:].strip()
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

    def get_mem_info(self):
        lines = self.client.bash('cat /proc/meminfo').get().stdout.splitlines()
        memInfo = { 'active': 0, 'available': 0, 'buffers': 0, 'cached': 0,
                    'free': 0,'inactive': 0, 'total': 0}

        mapping = { 'Active': 'active', 'MemAvailable': 'available', 'Buffers':'buffers',
                    'Cached': 'cached', 'MemFree': 'free', 'Inactive':'inactive', 'MemTotal':'total'}

        keys = mapping.keys()
        for line in lines:
            line = line.replace('\t', '')
            for key in keys:
                if key == line[:line.find(':')]:
                    item = int(line[line.index(':') + 1:line.index(' kB')].strip())
                    item = item * 1024
                    memInfo[mapping[key]] = item

        return memInfo

    def get_os_info(self):
        hostname = self.client.system('uname -n').get().stdout.strip()
        krn_name = self.client.system('uname -s').get().stdout.strip().lower()
        return {"hostname":hostname, "kernel":krn_name}

    def get_disks_info(self):
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
