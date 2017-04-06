from utils.utils import BaseTest


class ExtendedSystem(BaseTest):

    def setUp(self):
        super(ExtendedSystem, self).setUp()
        self.check_g8os_connection(ExtendedSystem)


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
        """ g8os-009
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
        """ g8os-0010
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
