from api.tests.globalSetup import APITestGlobalSetup


class EsysTest(APITestGlobalSetup):

    fixtures = ['v2/users', 'v2/properties', 'v2/spaces', 'v2/subspaces', 'v2/esys']

    def test_length_of_get_embeddedsystems_per_subspace(self):
        subspaces = self.rua.get('/embeddedsys/?subspaceid=1')
        self.assertEqual(len(subspaces.data), 2)
