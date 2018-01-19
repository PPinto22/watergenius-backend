from api.tests.globalSetup import APITestGlobalSetup


class SubSpaceTest(APITestGlobalSetup):

    fixtures = ['v2/users', 'v2/properties', 'v2/spaces', 'v2/subspaces']

    def test_length_of_get_subspaces_per_space(self):
        subspaces = self.rua.get('/subspaces/?spaceid=1')
        self.assertEqual(len(subspaces.data), 2)