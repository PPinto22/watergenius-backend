from api.tests.globalSetup import APITestGlobalSetup


class IrrigationTest(APITestGlobalSetup):

    fixtures = ['v1/users', 'v1/properties', 'v1/spaces', 'v1/subspaces', 'v1/irrigations']

    def test_length_of_get_irrigations_per_subspace(self):
        irrigations = self.rua.get('/irrigations/?subspaceid=1')
        self.assertEqual(len(irrigations.data), 3)
