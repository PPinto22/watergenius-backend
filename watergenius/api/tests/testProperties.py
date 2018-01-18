from api.tests.setup.propertiesSetup import PropertyTestSetup


class PropertyTest(PropertyTestSetup):

    def test_number_of_owned_properties_equals_PROPS_PER_USER(self):
        properties = self.regularClient.get('/properties/?ownerid='+self.regularEmail)
        self.assertEqual(len(properties.data), self.PROPS_PER_USER)

    def test_number_of_managers_equals_MANAGERS_PER_PROP_plus_one(self):
        propID = self.userProperties.get(self.regularEmail)[0]
        managersResponse = self.regularClient.get('/properties/'+str(propID)+'/managers/')
        self.assertEqual(len(managersResponse.data), self.MANAGERS_PER_PROP+1)
