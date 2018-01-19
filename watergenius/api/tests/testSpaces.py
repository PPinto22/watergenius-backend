from api.models import Property
from api.tests.globalSetup import APITestGlobalSetup


class SpaceTest(APITestGlobalSetup):

    fixtures = ['v2/users', 'v2/properties', 'v2/spaces']

    def test_length_of_get_spaces_by_property(self):
        spaces = self.rua.get('/spaces/?propertyid=1')
        self.assertEqual(len(spaces.data), 2)

    def test_length_of_get_time_restrictions(self):
        restrictions = self.nine.get('/spaces/3/restrictions/')
        self.assertEqual(len(restrictions.data), 2)
