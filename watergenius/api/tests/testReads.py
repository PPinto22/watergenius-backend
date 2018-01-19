from api.tests.globalSetup import APITestGlobalSetup


class ReadTest(APITestGlobalSetup):

    fixtures = ['v2/users', 'v2/properties', 'v2/spaces', 'v2/subspaces', 'v2/esys', 'v2/sensors',
                'v2/reads']

    def test_length_of_get_reads_per_sensor(self):
        reads = self.rua.get('/reads/?sensorid=1')
        self.assertEqual(len(reads.data), 3)
