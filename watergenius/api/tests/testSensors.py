from api.tests.globalSetup import APITestGlobalSetup


class SensorTest(APITestGlobalSetup):

    fixtures = ['v2/users', 'v2/properties', 'v2/spaces', 'v2/subspaces', 'v2/esys', 'v2/sensors']

    def test_length_of_get_sensors_per_esys(self):
        sensors = self.rua.get('/sensors/?embeddedsysid=1')
        self.assertEqual(len(sensors.data), 2)
