from utils.utils import BaseTest
import time
import unittest


class BasicTests(BaseTest):

    def setUp(self):
        super(BasicTests, self).setUp()
        self.check_g8os_connection(BasicTests)

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
            tmp = {"name": nic, "hardwareaddr": hardwareaddr, "mtu": mtu, "addrs": [{"addr": x} for x in addrs]}
            nicInfo.append(tmp)

        return nicInfo

    def getCpuInfo(self):
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

    def getDiskInfo(self):
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

    def getMemInfo(self):

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

    def test001_execute_commands(self):

        """ g8os-001
        *Test case for testing basic commands using  bash and system*

        **Test Scenario:**
        #. Check if you can ping the remote host, should succeed
        #. Create folder using system
        #. Check that the folder is created
        #. Remove the created folder
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Check if you can ping the remote host, should succeed')
        rs = self.client.ping()
        self.assertEqual(rs[:4], 'PONG')

        self.lg('Create folder using system')
        folder = self.rand_str()
        self.client.system('mkdir {}'.format(folder))

        self.lg('Check that the folder is created')
        rs1 = self.client.bash('ls | grep {}'.format(folder))
        rs_ob = rs1.get()
        self.assertEqual(rs_ob.stdout, '{}\n'.format(folder))
        self.assertEqual(rs_ob.state, 'SUCCESS')

        self.lg('Remove the created folder')
        self.client.bash('rm -rf {}'.format(folder))
        time.sleep(0.5)
        rs2 = self.client.bash('ls | grep {}'.format(folder))
        self.assertEqual(self.stdout(rs2), '')

        self.lg('{} ENDED'.format(self._testID))

    @unittest.skip('bug# https://github.com/g8os/core0/issues/95')
    def test002_kill_list_processes(self):

        """ g8os-002
        *Test case for testing killing and listing processes*

        **Test Scenario:**
        #. Create process that runs for long time using both system and bash
        #. List the process, should be found
        #. Kill the process
        #. List the process, shouldn't be found
        """

        self.lg('{} STARTED'.format(self._testID))

        for i in range(2):
            if i == 0:
               cmd = 'core.system'
               match = 'sleep'
               self.client.system('sleep 40')
            else:
               cmd = 'bash'
               match = 'sleep 40'
               self.client.bash('sleep 40')
            self.lg('Created process that runs for long time using {}'.format(cmd))

            self.lg('List the process, should be found')
            id = self.get_process_id(cmd, match)
            self.assertIsNotNone(id)

            self.lg('Kill the process')
            self.client.process.kill(id)

            self.lg('List the process, shouldn\'t be found')
            id = self.get_process_id(cmd, match)
            self.assertIsNone(id)

            self.lg('{} ENDED'.format(self._testID))

    def test003_os_info(self):

        """ g8os-003
        *Test case for checking on the system os information*

        **Test Scenario:**
        #. Get the os information using g8os client
        #. Get the hostname and compare it with the g8os os insformation
        #. Get the kernal's name and compare it with the g8os os insformation
        #. compare the rest of the info ...
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Get the os information using g8os client')
        os_info = self.client.info.os()

        self.lg('Get the hostname and compare it with the g8os os insformation')
        hostname = self.client.system('uname -n').get().stdout.strip()
        self.assertEqual(os_info['hostname'], hostname)

        self.lg('Get the kernal\'s name and compare it with the g8os os insformation')
        krn_name = self.client.system('uname -s').get().stdout.strip()
        self.assertEqual(os_info['os'], krn_name.lower())

        self.lg('{} ENDED'.format(self._testID))

    def test004_mem_info(self):

        """ g8os-004
        *Test case for checking on the system memory information*

        **Test Scenario:**
        #. Get the memory information using g8os client
        #. Get the memory information using bash
        #. Compare memory g8os results to that of the bash results, should be the same
        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('get memory info using bash')
        expected_mem_info = self.getMemInfo()

        self.lg('get memory info using g8os')
        g8os_mem_info = self.client.info.mem()

        self.lg('compare g8os results to bash results')
        self.assertEqual(expected_mem_info['total'], g8os_mem_info['total'])
        params_to_check = ['active', 'available', 'buffers', 'cached', 'free', 'inactive']
        for key in params_to_check:
            threshold = 1024 * 200  # acceptable threshold (200 MB)
            g8os_value = g8os_mem_info[key]
            expected_value = expected_mem_info[key]
            self.assertTrue(expected_value - threshold <= g8os_value <= expected_value + threshold, key)

        self.lg('{} ENDED'.format(self._testID))

    @unittest.skip('bug# https://github.com/g8os/core0/issues/109')
    def test005_cpu_info(self):

        """ g8os-005
        *Test case for checking on the system CPU information*

        **Test Scenario:**
        #. Get the CPU information using g8os client
        #. Get the CPU information using bash
        #. Compare CPU g8os results to that of the bash results, should be the same
        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('get cpu info using bash')
        expected_cpu_info = self.getCpuInfo()

        self.lg('get cpu info using g8os')
        g8os_cpu_info = self.client.info.cpu()

        self.lg('compare g8os results to bash results')
        for key in expected_cpu_info.keys():
            g8os_param_list = [x[key] for x in g8os_cpu_info]
            self.assertEqual(expected_cpu_info[key], g8os_param_list)

        self.lg('{} ENDED'.format(self._testID))

    def test006_disk_info(self):

        """ g8os-006
        *Test case for checking on the disks information*

        **Test Scenario:**
        #. Get the disks information using g8os client
        #. Get the disks information using bas
        #. Compare disks g8os results to that of the bash results, should be the same
        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('get disks info using linux bash command (mount)')
        expected_disk_info = self.getDiskInfo()

        self.lg('get cpu info using g8os')
        g8os_disk_info = self.client.info.disk()

        self.lg('compare g8os results to bash results')
        for key in expected_disk_info.keys():
            g8os_param_list = [x[key] for x in g8os_disk_info]
            self.assertEqual(expected_disk_info[key], g8os_param_list)

        self.lg('{} ENDED'.format(self._testID))

    def test007_nic_info(self):

        """ g8os-007
        *Test case for checking on the system nic information*

        **Test Scenario:**
        #. Get the nic information using g8os client
        #. Get the information using bash
        #. Compare nic g8os results to that of the bash results, should be the same
        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('get nic info using linux bash command (ip a)')
        expected_nic_info = self.getNicInfo()

        self.lg('get nic info using g8os client')
        g8os_nic_info = self.client.info.nic()

        self.lg('compare g8os results to bash results')
        params_to_check = ['name', 'addrs', 'mtu', 'hardwareaddr']
        for i in range(len(expected_nic_info)-1):
            for param in params_to_check:
                self.assertEqual(expected_nic_info[i][param], g8os_nic_info[i][param])

        self.lg('{} ENDED'.format(self._testID))

    # def test008_create_destroy_list_kvm(self):
    #     """ g8os-008
    #     *Test case for testing creating, listing and destroying VMs*
    #
    #     **Test Scenario:**
    #     #. Create virtual machine (VM1), should succeed
    #     #. List all virtual machines and check that VM1 is there
    #     #. Create another virtual machine with the same kvm domain, should fail
    #     #. Destroy VM1, should succeed
    #     #. List the virtual machines, VM1 should be gone
    #     #. Destroy VM1 again, should fail
    #     """
    #
    # def test009_create_list_delete_containers(self):
    #     """ g8os-009
    #     *Test case for testing creating, listing and deleting containers*
    #
    #     **Test Scenario:**
    #     #. Create a new container (C1), should succeed
    #     #. List all containers and check that C1 is there
    #     #. Get client, execute command and check on the result (write more details)
    #     #. Destroy C1, should succeed
    #     #. List the containers, C1 should be gone
    #     #. Destroy C1 again, should fail
    #     """
    #
    # def test010_join_leave_list_zerotier(self):
    #     """ g8os-010
    #     *Test case for testing joining, listing, leaving zerotier networks*
    #
    #     **Test Scenario:**
    #     #. Join zerotier network (N1), should succeed
    #     #. List zerotier network
    #     #. Leave zerotier network (N1),should succeed
    #     #. List zerotier networks, N1 should be gone
    #     #. Leave zerotier network (N1), should fail
    #     #. ref: https://www.zerotier.com/manual.shtml .. please all possible missing steps .. also add extended scenario to test zerotier functionality
    #     """
    #
    # def test011_create_delete_list_bridges(self):
    #     """ g8os-011
    #     *Test case for testing creating, listing, deleting bridges*
    #
    #     **Test Scenario:**
    #     #. Create bridge (B1), should succeed
    #     #. List  bridges, B1 should be listed
    #     #. Delete bridge B1, should succeed
    #     #. List bridges, B1 should be gone
    #     #. Delete bridge B1, should fail
    #     .... please add extended scenario to test bridges functionality
    #     """
    #

    def test012_create_list_delete_btrfs(self):
        """ g8os-012
        *Test case for creating, listing and monitoring btrfs*

        **Test Scenario:**
        #. Setup two loop devices to be used by btrfs
        #. Create Btrfs file system, should succeed
        #. List Btrfs file system, should find the file system (Bfs1)
        #. Mount the btrfs filesystem (Bfs1)
        #. Get Info for the btrfs file system (Bfs1)
        #. Add new loop (LD1) device, should succeed
        #. Remove the loop device (LD1), should succeed
        #. Remove all loop devices
        #. List the btrfs filesystem, Bfs1 shouldn't be there
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Setup two loop devices to be used by btrfs')
        loop_dev_list = self.setup_loop_devices(['bd0', 'bd1'], '500M', deattach=True)

        self.lg('Create Btrfs file system (Bfs1), should succeed')
        label = self.rand_str()
        self.client.btrfs.create(label, loop_dev_list)

        self.lg('List Btrfs file system, should find the file system (Bfs1)')
        btr_list = self.client.btrfs.list()
        btr = [i for i in btr_list if i['label'] == label]
        self.assertNotEqual(btr, [])

        self.lg('Mount the btrfs filesystem (Bfs1)')
        dirc = self.rand_str()
        mount_point = '/mnt/{}'.format(dirc)
        self.client.bash('mkdir -p {}'.format(mount_point))
        rs = self.client.disk.mount(loop_dev_list[0], mount_point, [""])
        self.assertEqual(rs.get().state(), 'SUCCESS')

        self.lg('Get Info for the btrfs file system (Bfs1)')
        rs = self.client.btrfs.info(mount_point)
        self.assertEqual(rs['label'], label)
        self.assertEqual(rs['total_devices'], btr[0]['total_devices'])

        self.lg('Add new loop (LD1) device')
        loop_dev_list2 = self.setup_loop_devices(['bd2'], '500M')
        self.client.btrfs.device_add(mount_point, loop_dev_list2[0])
        rs = self.client.info(mount_point)
        self.assertEqual(rs['total_devices'], 3)

        self.lg('Remove the loop device (LD1)')
        self.client.btrfs.device_remove(mount_point, loop_dev_list2[0])
        rs = self.client.info(mount_point)
        self.assertEqual(rs['total_devices'], 2)

        self.lg('Remove all loop devices')
        for dev in loop_dev_list:
            rs = self.client.btrfs.device_remove(mount_point, dev)
            self.assertEqual(rs.get().state(), 'SUCCESS')
        self.deattach_all_loop_devices()
        self.client.btrfs.list()

        self.lg("List the btrfs filesystems , Bfs1 shouldn't be there")
        btr_list = self.client.btrfs.list()
        btr = [i for i in btr_list if i['label'] == label]
        self.assertEqual(btr, [])
        self.client.bash('rm -rf {}'.format(mount_point))

        self.lg('{} ENDED'.format(self._testID))
