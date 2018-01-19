from api.tests.globalSetup import APITestGlobalSetup


class SubSpaceTest(APITestGlobalSetup):

    fixtures = ['v1/users', 'v1/properties', 'v1/spaces', 'v1/subspaces']

    def test_length_of_get_subspaces_per_space(self):
        subspaces = self.rua.get('/subspaces/?spaceid=1')
        self.assertEqual(len(subspaces.data), 2)