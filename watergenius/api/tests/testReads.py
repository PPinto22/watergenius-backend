from rest_framework import status

from api.tests.globalSetup import APITestGlobalSetup


class ReadTest(APITestGlobalSetup):

    fixtures = ['tests/users', 'tests/properties', 'tests/spaces', 'tests/subspaces', 'tests/esys', 'tests/sensors', 'tests/reads']

    def test_length_of_get_reads_per_sensor(self):
        reads = self.rua.get('/reads/?sensorid=1')
        self.assertEqual(len(reads.data), 3)

    def test_post_read(self):
        read = {
            "read_timestamp": "2018-01-20T08:36:23.860205Z",
            "read_sensor": 1,
            "read_value": 55.5,
            "read_type": 1
        }
        post_response = self.rua.post('/reads/', read, format='json')
        self.assertTrue(status.is_success(post_response.status_code))
        reads = self.rua.get('/reads/?sensorid=1')
        self.assertEqual(len(reads.data), 4)