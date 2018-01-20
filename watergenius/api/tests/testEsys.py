from rest_framework import status

from api.tests.globalSetup import APITestGlobalSetup


class EsysTest(APITestGlobalSetup):

    fixtures = ['v1/users', 'v1/properties', 'v1/spaces', 'v1/subspaces', 'v1/esys']

    def test_get_embeddedsystems_per_subspace(self):
        subspaces = self.rua.get('/embeddedsys/?subspaceid=1')
        self.assertEqual(len(subspaces.data), 2)

    def test_post_embeddedsystem(self):
        esys = {
            "esys_local_lat": 40.736946,
            "esys_local_long": -10.142685,
            "esys_local_alt": 10.5,
            "esys_sub": 1,
            "esys_state": 0,
            "esys_name": "Embedded System 4"
        }
        post_response = self.rua.post('/embeddedsys/', esys, format='json')
        self.assertTrue(status.is_success(post_response.status_code))
        esystems = self.rua.get('/embeddedsys/?subspaceid=1')
        self.assertEqual(len(esystems.data), 3)