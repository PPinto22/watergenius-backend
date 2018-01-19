from api.tests.globalSetup import APITestGlobalSetup


class ReadTest(APITestGlobalSetup):

    fixtures = ['v1/users', 'v1/properties', 'v1/spaces', 'v1/subspaces', 'v1/esys', 'v1/sensors', 'v1/reads']

    def test_length_of_get_reads_per_sensor(self):
        reads = self.rua.get('/reads/?sensorid=1')
        self.assertEqual(len(reads.data), 3)
