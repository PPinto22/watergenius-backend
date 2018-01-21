from rest_framework import status

from api.tests.globalSetup import APITestGlobalSetup


class SubSpaceTest(APITestGlobalSetup):

    fixtures = ['tests/users', 'tests/properties', 'tests/spaces', 'tests/subspaces']

    def test_get_subspaces_per_space(self):
        subspaces = self.rua.get('/subspaces/?spaceid=1')
        self.assertEqual(len(subspaces.data), 2)

    def test_post_subspace(self):
        subspace = {
            "sub_name": "Name 4",
            "sub_description": "Description 4",
            "sub_space_id": 1
        }
        post_response = self.rua.post('/subspaces/', subspace, format='json')
        self.assertTrue(status.is_success(post_response.status_code))
        subspaces = self.rua.get('/subspaces/?spaceid=1')
        self.assertEqual(len(subspaces.data), 3)

    def test_update_subspace(self):
        subspace = {
            "sub_name": "New name",
            "sub_description": "New description",
            "sub_space_id": 2
        }
        put_response = self.rua.put('/subspaces/1/', subspace, format='json')
        self.assertTrue(status.is_success(put_response.status_code))
        for attr in subspace:
            self.assertEqual(subspace[attr], put_response.data[attr])
        subspaces1 = self.rua.get('/subspaces/?spaceid=1')
        self.assertTrue(len(subspaces1.data), 1)
        subspaces2 = self.rua.get('/subspaces/?spaceid=2')
        self.assertTrue(len(subspaces2.data), 1)

    def test_delete_empty_subspace(self):
        response = self.rua.delete('/subspaces/2/')
        self.assertTrue(status.is_success(response.status_code))
        subspaces = self.rua.get('/subspaces/?spaceid=1')
        self.assertEqual(len(subspaces.data), 1)

    def test_delete_cascade_subspace(self):
        response = self.rua.delete('/subspaces/1/')
        self.assertTrue(status.is_success(response.status_code))
        subspaces = self.rua.get('/subspaces/?spaceid=1')
        self.assertEqual(len(subspaces.data), 1)
        embeddedsys = self.rua.get('/embeddedsys/?subspaceid=1')
        self.assertEqual(len(embeddedsys.data), 0)