import random
from api_testing.testcases.testcases_base import TestcasesBase
from api_testing.grid_apis.apis.volumes_apis import VolumesAPIs
from api_testing.python_client.client import Client
import unittest


class TestVolumes(TestcasesBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.volumes_api = VolumesAPIs()
        self.base_test = TestcasesBase()

    def setUp(self):
        self.lg.info('Create new volume.')
        self.volume_size = 1
        block_size = 4096
        self.volumn_id = self.base_test.rand_str()
        volume_type=random.choice('boot','db','cache','tmp')
        self.body = {"siz": self.volume_size, "blocksize": block_size,
                "volumetype": volume_type,"id": self.volumn_id,
                "readOnly": False }

        body = json.dumps(self.body)
        response = self.volumes_api.post_volumes(body=body)
        self.assertEqual(response.status_code, 201)

    def tearDown(self):

        self.lg.info('Delete created volume.')
        response = self.volumes_api.delete_volumes_volumeid(self.volumn_id)
        self.assertEqual(response.status_code, 204)

        self.lg.info('Check that it removed from volumes list. .')
        response = self.volumes_api.get_volumes()
        self.assertEqual(response.status_code, 200)
        volumes_list = response.json()
        self.assertNotIn(self.volumn_id, volumes_list)

    def test001_create_volume(self):
        """ GAT-001
        *GET:/node/ Expected: create new volume*

        **Test Scenario:**

        #. Send post volumes api request.
        #. check that created volume exist in volume list.
        """
        self.lg.info('check that created volume exist in volume list.')
        response = self.volumes_api.get_volumes()
        self.assertEqual(response.status_code, 200)
        volumes_list = response.json()
        self.assertIn(self.volumn_id, volumes_list)

    def test002_get_volume_details(self):
        """ GAT-002
        *GET:/node/ Expected: create new volume*

        **Test Scenario:**

        #. Create new volume.
        #. Get volume details check that same as details you create with.

        """
        self.lg.info('Get volume details check that same as details you create with.')

        response = self.volumes_api.get_volumes_volumeid(self.volumn_id)
        self.assertEqual(response.status_code, 200)
        volume_details = response.json()
        for key in body.keys():
            self.assertEqual(volume_details[key], body[key])


    def test003_resize_volume(self):
        """ GAT-003
        *GET:/node/ Expected: create new volume*

        **Test Scenario:**

        #. Create new volume, should succeed.
        #. Resize created volume, should succeed.
        #. Check that size of volume changed from get volume details,should succeed.
        #. Resize with size vlue less than current volume size, should fail.
        #. Check that size of volume doesn't change from get volume details,should succeed.

        """
        self.lg.info(' Resize  created volume.')
        new_size = self.volume_size+1
        body = {"newSize": new_size}
        response = self.volumes_api.post_volumes_volumeid_resize(self.volumn_id, body)
        self.assertEqual(response.status_code, 202)

        self.lg.info(' check that size of volume changed from get volume details.')
        response = self.volumes_api.get_volumes_volumeid(self.volumn_id)
        self.assertEqual(response.status_code, 200)
        volume_details = response.json()
        self.assertEqual(volume_details['size'], new_size)

        self.lg.info(' Resize with size vlue less than current volume size, should fail.')
        new_size = self.volume_size-1
        body = {"newSize": new_size}
        response = self.volumes_api.post_volumes_volumeid_resize(self.volumn_id, body)
        self.assertEqual(response.status_code, 404)

        self.lg.info(' check that size of volume doesn\'t change from get volume details.')
        response = self.volumes_api.get_volumes_volumeid(self.volumn_id)
        self.assertEqual(response.status_code, 200)
        volume_details = response.json()
        self.assertNotEqual(volume_details['size'], new_size)

    @unittest.skip('Not Emplemented yet ')
    def test004_Rollback_volume(self):
        """ GAT-004
        *GET:/node/ Expected: Rollback volume*

        **Test Scenario:**

        #. Create new volume, should succeed.
        #. Resize created volume, should succeed.
        #. Rollback to first volume,should succeed
        #. Check that size of volume change from get volume details,should succeed.

        """
        self.lg.info(' Resize  created volume.')
        new_size = self.volume_size+1
        body = {"newSize": new_size}
        response = self.volumes_api.post_volumes_volumeid_resize(self.volume_id, body)
        self.assertEqual(response.status_code, 202)

        self.lg.info(' check that size of volume changed from get volume details.')
        response = self.volumes_api.get_volumes_volumeid(self.volumn_id)
        self.assertEqual(response.status_code, 200)
        volume_details = response.json()
        self.assertNotEqual(volume_details['size'], new_size)

        self.lg.info('Rollback to first volume,should succeed,should succeed.')
        body = {"epoch": }
        response = self.volumes_api.post_volumes_volumeid_rollback(self.volume_id, body)
        self.assertEqual(response.status_code, 202)
        self.lg.info(' check that size of volume changed from get volume details.')
