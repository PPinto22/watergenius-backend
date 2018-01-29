from rest_framework import status

from api.tests.globalSetup import APITestGlobalSetup


class SensorTest(APITestGlobalSetup):

    fixtures = ['tests/users', 'tests/properties', 'tests/spaces', 'tests/subspaces', 'tests/esys', 'tests/sensors']

    def test_get_sensors_per_esys(self):
        sensors = self.rua.get('/sensors/?embeddedsysid=1')
        self.assertEqual(len(sensors.data), 2)

    def test_post_sensor(self):
        sensor = {
            "sensor_name": "Humidity sensor 4",
            "sensor_state": 0,
            "sensor_esys": 1,
            "sensor_timerate": 10,
            "sensor_depth": 20,
            "sensor_type": "humidity"
        }
        post_response = self.rua.post('/sensors/', sensor, format='json')
        self.assertTrue(status.is_success(post_response.status_code))
        sensors = self.rua.get('/sensors/?embeddedsysid=1')
        self.assertEqual(len(sensors.data), 3)