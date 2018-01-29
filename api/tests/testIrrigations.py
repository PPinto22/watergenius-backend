from rest_framework import status

from api.tests.globalSetup import APITestGlobalSetup


class IrrigationTest(APITestGlobalSetup):

    fixtures = ['tests/users', 'tests/properties', 'tests/spaces', 'tests/subspaces', 'tests/irrigations']

    def test_get_irrigations_per_subspace(self):
        irrigations = self.rua.get('/irrigations/?subspaceid=1')
        self.assertEqual(len(irrigations.data), 3)

    def test_post_irrigation(self):
        irrigation = {
            "irrigation_time_date": "2018-01-20T20:00:00.500000Z",
            "irrigation_time_qty": 3.2,
            "irrigation_time_sub": 1
        }
        post_response = self.rua.post('/irrigations/', irrigation, format='json')
        self.assertTrue(status.is_success(post_response.status_code))
        irrigations = self.rua.get('/irrigations/?subspaceid=1')
        self.assertEqual(len(irrigations.data), 4)