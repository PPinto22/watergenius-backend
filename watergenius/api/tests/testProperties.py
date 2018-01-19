from rest_framework import status

from api.tests.globalSetup import APITestGlobalSetup


class PropertyTest(APITestGlobalSetup):

    fixtures = ['v1/users','v1/properties']

    def test_get_properties(self):
        properties = self.rua.get('/properties/?ownerid=rua@gmail.com')
        self.assertEqual(len(properties.data), 2)

    def test_get_property_managers(self):
        managers = self.rua.get('/properties/1/managers/')
        self.assertEqual(len(managers.data), 2)

    def test_get_non_existent_node(self):
        node = self.rua.get('/properties/2/node/')
        self.assertEqual(node.data, "That property doesn't have a central node")

    def test_get_existent_node(self):
        node = self.rua.get('/properties/1/node/')
        self.assertEqual(node.data['node_ip'], "100.100.30.2")
        self.assertEqual(node.data['node_local_lat'], 38.736945)
        self.assertEqual(node.data['node_local_long'], -9.142684)
        self.assertEqual(node.data['node_local_alt'], 4.5)
        self.assertEqual(node.data["node_property"], 1)

    def test_post_property(self):
        property = {
            "prop_name": "Name 4",
            "prop_description": "Description 4",
            "prop_address": "Address 4",
            "prop_owner": "freitas@gmail.com"
        }
        post_response = self.freitas.post('/properties/', property, format='json')
        self.assertTrue(status.is_success(post_response.status_code))
        properties = self.freitas.get('/properties/?ownerid=freitas@gmail.com')
        self.assertEqual(len(properties.data), 1)