from api.tests.globalSetup import APITestGlobalSetup


class SensorTest(APITestGlobalSetup):

    fixtures = ['v1/users', 'v1/properties', 'v1/spaces', 'v1/subspaces', 'v1/esys', 'v1/sensors']

    def test_get_sensors_per_esys(self):
        sensors = self.rua.get('/sensors/?embeddedsysid=1')
        self.assertEqual(len(sensors.data), 2)
