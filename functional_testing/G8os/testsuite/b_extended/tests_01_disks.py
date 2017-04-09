from utils.utils import BaseTest
import unittest


class DisksTests(BaseTest):

    def setUp(self):
        super(DisksTests, self).setUp()
        self.check_g8os_connection(DisksTests)

    def create_btrfs(self):
        self.lg('Create Btrfs file system (Bfs1), should succeed')
        self.label = self.rand_str()
        self.loop_dev_list = self.setup_loop_devices(['bd0', 'bd1'], '500M', deattach=True)
        self.lg('Mount the btrfs filesystem (Bfs1)')
        self.client.btrfs.create(self.label, self.loop_dev_list)
        self.mount_point = '/mnt/{}'.format(self.rand_str())
        self.client.bash('mkdir -p {}'.format(self.mount_point))
        self.client.disk.mount(self.loop_dev_list[0], self.mount_point, [""])

    def destroy_btrfs(self):
        self.lg('Remove all loop devices')
        for dev in self.loop_dev_list:
            self.client.btrfs.device_remove(self.mount_point, dev)
        self.deattach_all_loop_devices()

    def bash_disk_info(self, keys, diskname):
        diskinf = {}
        info = self.client.bash('lsblk -d dev/{} -O -P -b'.format(diskname)).get().stdout
        info = info.lower()
        lines = info.split()
        for key in keys:
            for line in lines:
                if key == line[:line.find('=')]:
                    value = line[line.find('=')+2:-1]
                    if value == '':
                        value = None
                    if key == 'vendor':
                        value = line[line.find('=')+2:].ca
                    diskinf[key] = value
                    break
        diskinf['blocksize'] = self.client.bash(' blockdev --getbsz dev/{} '.format(diskname)).get().stdout
        remaininfo = self.client.bash('parted dev/{} print '.format(diskname)).get().stdout
        remaininfo_lines = remaininfo.splitlines()
        for i, line in enumerate(remaininfo_lines):
            if 'Partition Table' in line:
                diskinf['table'] = str(line[line.find(':')+2:])
            if i == 6:
                lines = line.split()
                sizes = [lines[1], lines[2]]
                for n, size in enumerate(sizes):
                    if 'TB' in size:
                        sizes[n] = int(float((size[:size.find('TB')]))*1024*1024*1024*1024)
                    elif 'GB' in size:
                        sizes[n] = int(float((size[:size.find('GB')]))*1024*1024*1024)
                    elif 'MB' in size:
                        sizes[n] = int(float(size[:size.find('MB')])*1024*1024)
                    elif 'KB' in size:
                        sizes[n] = int(float(size[:size.find('KB')])*1024)
                    else:
                        sizes[n] = int(float(size[:size.find('B')]))

                diskinf['start'] = sizes[0]
                diskinf['end'] = sizes[1]
        return diskinf

    def test001_create_list_delete_btrfs(self):
        """ g8os-008
        *Test case for creating, listing and monitoring btrfs*

        **Test Scenario:**
        #. Setup two loop devices to be used by btrfs
        #. Create Btrfs file system (Bfs1), should succeed
        #. Mount the btrfs filesystem (Bfs1)
        #. List Btrfs file system, should find the file system (Bfs1)
        #. Get Info for the btrfs file system (Bfs1)
        #. Add new loop (LD1) device, should succeed
        #. Remove the loop device (LD1), should succeed
        #. Remove all loop devices
        #. List the btrfs filesystem, Bfs1 shouldn't be there
        """

        self.lg('{} STARTED'.format(self._testID))

        self.create_btrfs()

        self.lg('List Btrfs file system, should find the file system (Bfs1)')
        btr_list = self.client.btrfs.list()
        btr = [i for i in btr_list if i['label'] == self.label]
        self.assertNotEqual(btr, [])

        self.lg('Get Info for the btrfs file system (Bfs1)')
        rs = self.client.btrfs.info(self.mount_point)
        self.assertEqual(rs['label'], self.label)
        self.assertEqual(rs['total_devices'], btr[0]['total_devices'])

        self.lg('Add new loop (LD1) device')
        loop_dev_list2 = self.setup_loop_devices(['bd2'], '500M')
        self.client.btrfs.device_add(self.mount_point, loop_dev_list2[0])
        rs = self.client.btrfs.info(self.mount_point)
        self.assertEqual(rs['total_devices'], 3)

        self.lg('Remove the loop device (LD1)')
        self.client.btrfs.device_remove(self.mount_point, loop_dev_list2[0])
        rs = self.client.btrfs.info(self.mount_point)
        self.assertEqual(rs['total_devices'], 2)

        self.destroy_btrfs()

        self.lg("List the btrfs filesystems , Bfs1 shouldn't be there")
        btr_list = self.client.btrfs.list()
        btr = [i for i in btr_list if i['label'] == self.label]
        self.assertEqual(btr, [])
        self.client.bash('rm -rf {}'.format(self.mount_point))

        self.lg('{} ENDED'.format(self._testID))

    def test002_subvolumes_btrfs(self):
        """ g8os-016
        *Test case for creating, listing and deleting btrfs subvolumes*

        **Test Scenario:**
        #. Create Btrfs file system, should succeed
        #. Create btrfs subvolume (SV1), should succeed
        #. List btrfs subvolumes giving any btrfs path, SV1 should be found
        #. List btrfs subvolumes giving non btrfs path, should fail
        #. Create btrfs subvolume (SV2) inside (SV1), should succeed
        #. Delete SV1, should fail as it has SV1 inside it
        #. Delete SV2 then SV1, should succeed
        #. List btrfs subvolumes, should return nothing
        #. Delete SV1, should Fail
        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('Create Btrfs file system, should succeed')
        self.create_btrfs()

        self.lg('Create btrfs subvolume (SV1), should succeed')
        sv1 = self.rand_str()
        sv1_path = '{}/{}'.format(self.mount_point, sv1)
        self.client.btrfs.subvol_create(sv1_path)

        self.lg('List btrfs subvolumes, SV1 should be found')
        sub_list = self.client.btrfs.subvol_list(self.mount_point)
        self.assertEqual(sub_list[0]['Path'], sv1)
        self.assertEqual(len(sub_list), 1)

        self.lg('List btrfs subvolumes giving non btrfs path, should fail')
        with self.assertRaises(RuntimeError):
            self.client.btrfs.subvol_list('/mnt')

        self.lg('Create btrfs subvolume (SV2) inside (SV1), should succeed')
        sv2 = self.rand_str()
        sv2_path = '{}/{}'.format(sv1_path, sv2)
        self.client.btrfs.subvol_create(sv2_path)

        self.lg('Delete SV1, should fail as it has SV1 inside it')
        with self.assertRaises(RuntimeError):
            self.client.btrfs.subvol_delete(sv1_path)

        self.lg('Delete SV2 then SV1, should succeed')
        self.client.btrfs.subvol_delete(sv2_path)
        self.client.btrfs.subvol_delete(sv1_path)

        self.lg('List btrfs subvolumes, should return nothing')
        sub_list = self.client.btrfs.subvol_list(self.mount_point)
        self.assertIsNone(sub_list)

        self.lg('Delete SV1, should Fail')
        with self.assertRaises(RuntimeError):
            self.client.btrfs.subvol_delete(sv1_path)
        self.destroy_btrfs()

        self.lg('{} ENDED'.format(self._testID))

    def test003_snapshots_btrfs(self):
        """ g8os-0017
        *Test case for creating, listing and deleting btrfs snapshots*

        **Test Scenario:**
        #. Create Btrfs file system, should succeed
        #. Create btrfs snapshot (SN1), should succeed
        #. List btrfs subvolumes giving any btrfs path, SN1 should be found
        #. Create btrfs snapshot (SN2) inside (SN1) with read only, should succeed
        #. Create btrfs snapshot (SN3) inside (SN2), should fail
        #. Delete btrfs subvolume SN2 then SN1, should succeed
        #. List btrfs subvolumes, should return nothing
        """

        self.lg('{} STARTED'.format(self._testID))

        self.lg('Create Btrfs file system, should succeed')
        self.create_btrfs()

        self.lg('Create btrfs snapshot (SN1), should succeed')
        sn1 = self.rand_str()
        sn1_path = '{}/{}'.format(self.mount_point, sn1)
        self.client.btrfs.subvol_snapshot(self.mount_point, sn1_path)

        self.lg('List btrfs subvolumes giving any btrfs path, SN1 should be found')
        sub_list = self.client.btrfs.subvol_list(self.mount_point)
        self.assertEqual(sub_list[0]['Path'], sn1)
        self.assertEqual(len(sub_list), 1)

        self.lg('Create btrfs snapshot (SN2) inside (SN1) with read only, should succeed')
        sn2 = self.rand_str()
        sn2_path = '{}/{}'.format(sn1_path, sn2)
        self.client.btrfs.subvol_snapshot(sn1_path, sn2_path, read_only=True)

        self.lg('Create btrfs snapshot (SN3) inside (SN2), should fail')
        sn3 = self.rand_str()
        sn3_path = '{}/{}'.format(sn2_path, sn3)
        with self.assertRaises(RuntimeError):
            self.client.btrfs.subvol_snapshot(sn2_path, sn3_path)

        self.lg('Delete btrfs subvolume SN2 then SN1, should succeed')
        self.client.btrfs.subvol_delete(sn2_path)
        self.client.btrfs.subvol_delete(sn1_path)

        self.lg('List btrfs subvolumes, should return nothing')
        sub_list = self.client.btrfs.subvol_list(self.mount_point)
        self.assertIsNone(sub_list)

        self.destroy_btrfs()

        self.lg('{} ENDED'.format(self._testID))

    @unittest.skip('bug# https://github.com/g8os/core0/issues/134')
    def test004_disk_get_info(self):
        """ g8os-020

        *Test case for checking on the disks information*

        **Test Scenario:**

        #. Get the disks name  using disk list
        #. Get disk info using bash
        #. Get disk info using g8os disk info
        #. Compare g8os results to that of the bash results, should be the same

        """
        self.lg('{} STARTED'.format(self._testID))

        self.lg('Get the disks name  using disk list')
        disk_names = []
        disks = self.client.disk.list()
        for disk in disks['blockdevices']:
            disk_names.append(disk['name'])

        for disk in disks_names:
            self.lg('Get disk {} info  using bash '.format(disk))
            g8os_disk_info = self.client.disk.getinfo(disk)
            keys = g8os_disk_info.keys()

            self.lg('Get disk {} info  using gos disk info  '.format(disk))
            bash_disk_info = self.bash_disk_info(keys, disk)

            self.lg('compare g8os results to disk{} of the bash results, should be the same '.format(disk))
            for key in bash_disk_info.keys:
                self.assertEqual(g8os_disk_info[key], bash_disk_info)

        self.lg('{} ENDED'.format(self._testID))

    def test005_disk_mount_and_unmount(self):
        """ g8os-021

        *Test case for test mount disk and unmount *

        **Test Scenario:**

        #. Make device to be mounted.
        #. Mount disk using g8os disk mount.
        #. Get disk info , should mounted disk be here.
        #. Try mount it again , should fail.
        #. Remount disk ,should deattach from disk list.

        """
        self.lg('{} STARTED'.format(self._testID))
        filename = [self.rand_str()]
        label = self.rand_str()
        mount_point = '/mnt/{}'.format(self.rand_str())
        self.lg('Make device to be mounted')
        self.loop_dev_list = self.setup_loop_devices(filename, '500M', deattach=True)
        self.client.btrfs.create(label, self.loop_dev_list)

        self.lg('Mount disk using g8os disk mount')
        self.client.bash('mkdir -p {}'.format(mount_point))
        self.client.disk.mount(self.loop_dev_list[0], mount_point, [""])

        self.lg('Get disk info , should mounted disk be here')
        disks = self.client.bash(' lsblk -n -io NAME ').get().stdout
        disks = disks.splitlines()
        result = [disk in self.loop_dev_list[0] for disk in disks]
        self.assertTrue(True in result)

        self.lg('Try mount it again , should fail')
        with self.assertRaises(RuntimeError):
            self.client.disk.mount(self.loop_dev_list[0], mount_point, [""])

        self.lg('Remount disk ,should deattach from disk list')

        self.client.disk.umount(self.loop_dev_list[0])
        disks = self.client.bash(' lsblk -n -io NAME ').get().stdout
        disks = disks.splitlines()
        result = [disk in self.loop_dev_list[0] for disk in disks]
        self.assertFalse(True in result)

        self.lg('{} ENDED'.format(self._testID))

    def test006_disk_partions(self):

        """ g8os-022

        *Test case for test creating Partitions in disk *

        **Test Scenario:**

        #. make new disk.
        #. Make partion for disk before make table for it , should fail.
        #. Make a partion table for this disk, should succeed.
        #. Make 2 partion for disk with 50% space of disk , should succeed.
        #. check disk  exist in disk list with 2 partions .
        #. Make partion for this disk again  , should fail.
        #. Remove partion for this disk ,should succeed.

        """
        self.lg('{} STARTED'.format(self._testID))
        filename = [self.rand_str()]
        label = self.rand_str()
        mount_point = '/mnt/{}'.format(self.rand_str())

        self.lg('Make device to be mounted')
        self.loop_dev_list = self.setup_loop_devices(filename, '500M', deattach=True)
        device_name = self.loop_dev_list[0]
        device_name = device_name[device_name.index('/')+5:]

        self.lg('Make partion for disk before make table for it , should fail.')
        with self.assertRaises(RuntimeError):
            self.client.disk.mkpart(device_name, '0', '50%')

        self.lg('Make a partion table for this disk, should succeed.')
        self.client.disk.mktable(device_name)

        self.lg('Make 2 partion for disk with 50% space of disk , should succeed.')
        self.client.disk.mkpart(device_name, '0', '50%')
        self.client.disk.mkpart(device_name, '50%', '100%')

        self.lg('check disk  exist in disk list with 2 partions ')
        disks = self.client.disk.list()
        for disk in disks['blockdevices']:
            if disk['name'] == device_name:
                self.assertEqual(len(disk['children']), 2)

        self.lg('Make partion for this disk again  , should fail.')
        with self.assertRaises(RuntimeError):
            self.client.disk.mkpart(device_name, '0', '50%')

        self.lg('Remove partion for this disk ,should succeed.')
        self.client.disk.rmpart(device_name, 1)
        self.client.disk.rmpart(device_name, 2)

        self.lg('check that  partions for this disk removed ,should succeed.')
        disks = self.client.disk.list()
        for disk in disks['blockdevices']:
            if disk['name'] == device_name:
                self.assertTrue('children' not in disk.keys())

        self.lg('{} ENDED'.format(self._testID))
