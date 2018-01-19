from api.tests.globalSetup import APITestGlobalSetup


class DayplanTest(APITestGlobalSetup):

    # TODO - remove irrigations
    fixtures = ['v1/users', 'v1/properties', 'v1/spaces', 'v1/subspaces', 'v1/irrigations', 'v1/dayplans']

    def test_length_of_get_plans_per_subspace(self):
        plans = self.rua.get('/plans/?subspaceid=1')
        self.assertEqual(len(plans.data), 3)
