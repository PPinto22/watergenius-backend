from rest_framework import status

from api.tests.globalSetup import APITestGlobalSetup


class DayplanTest(APITestGlobalSetup):

    fixtures = ['tests/users', 'tests/properties', 'tests/spaces', 'tests/subspaces', 'tests/dayplans']

    def test_get_plans_per_subspace(self):
        plans = self.rua.get('/plans/?subspaceid=1')
        self.assertEqual(len(plans.data), 3)

    def test_post_day_play(self):
        plan = {
            "dayplan_gen_time": "2018-01-17T10:30:30.500000Z",
            "dayplan_time": "2018-01-20T20:00:00.000000Z",
            "dayplan_water_qty": 3.1,
            "dayplan_sub": 1
        }
        post_response = self.rua.post('/plans/', plan, format='json')
        self.assertTrue(status.is_success(post_response.status_code))
        plans = self.rua.get('/plans/?subspaceid=1')
        self.assertEqual(len(plans.data), 4)
