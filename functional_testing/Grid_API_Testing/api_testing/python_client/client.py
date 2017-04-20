import g8core

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
                cpuInfo[-1]['mhz'] = int(float(value))
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
            addrs = [ x for x in addrs]
            if addrs == [] :
                addrs= None
            tmp = {"name": nic, "hardwareaddr": hardwareaddr, "mtu": mtu, "addrs": addrs}
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
        memInfo = {'available': 0, 'buffers': 0, 'cached': 0,
                    'inactive': 0, 'total': 0}
        for line in lines:
            line = line.replace('\t', '').strip()
            key = line[:line.find(':')].lower()
            value = line[line.find(':')+2:line.find('kB')].strip()
            if 'mem' == key[:3]:
                key = key[3:]
            if key in memInfo.keys():

                memInfo[key] = int(value)*1024
        return memInfo

    def get_nodes_info(self):
        hostname = self.client.system('uname -n').get().stdout.strip()
        krn_name = self.client.system('uname -s').get().stdout.strip().lower()
        return {"hostname":hostname, "os":krn_name}

    def get_nodes_disks(self):
        diskInfo = []
        diskInfo_format = {'mountpoint': [], 'fstype': [], 'device': [], 'opts': []}
        response = self.client.bash('mount').get().stdout
        lines = response.splitlines()
        for line in lines:
            line = line.split()
            item = dict(diskInfo_format)
            item['mountpoint'] = line[2]
            item['fstype'] = line[4]
            item['device'] = line[0]
            item['opts'] = line[5][1:-1]
            diskInfo.append(item)
        return diskInfo

    def get_processes_list(self):
        processes = self.client.process.list()
        return processes

    def get_jobs_list(self):
        jobs = self.client.job.list()
        gridjobs = []
        temp = {}
        for job in jobs:
            temp['id'] = job['cmd']['id']
            if job['cmd']['arguments']:
                if ('name' in job['cmd']['arguments'].keys()):
                    temp['name'] = job['cmd']['arguments']['name']
            temp['starttime'] = job['starttime']
            gridjobs.append(temp)
        return gridjobs

    def get_node_state(self):
        state = self.client.json('core.state', {})
        del state['cpu']
        return state
