from api.tests.globalSetup import APITestGlobalSetup


class EsysTest(APITestGlobalSetup):

    fixtures = ['v1/users', 'v1/properties', 'v1/spaces', 'v1/subspaces', 'v1/esys']

    def test_get_embeddedsystems_per_subspace(self):
        subspaces = self.rua.get('/embeddedsys/?subspaceid=1')
        self.assertEqual(len(subspaces.data), 2)
