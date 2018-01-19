from api.tests.globalSetup import APITestGlobalSetup


class PropertyTest(APITestGlobalSetup):

    fixtures = ['v2/users','v2/properties']

    def test_length_of_get_properties(self):
        properties = self.rua.get('/properties/?ownerid=rua@gmail.com')
        self.assertEqual(len(properties.data), 2)

    def test_length_of_get_property_managers(self):
        managersResponse = self.rua.get('/properties/1/managers/')
        self.assertEqual(len(managersResponse.data), 2)
