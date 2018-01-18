from api.models import Property
from api.tests.setup.spacesSetup import SpaceTestSetup


class SpaceTest(SpaceTestSetup):

    def test_quantity_of_spaces_per_property_equals_SPACES_PER_PROP(self):
        spaceID = next(iter(self.spaceIDs.keys()))
        propID = self.spaceIDs[spaceID]
        apiClient = self.getSpaceOwnerAPIClient(spaceID)
        spaces = apiClient.get('/spaces/?propertyid='+str(propID))
        self.assertEqual(len(spaces.data), self.SPACES_PER_PROP)

    def test_quantity_of_time_restrictions_per_space_equals_RESCTRICTIONS_PER_SPACE(self):
        spaceID = next(iter(self.spaceIDs))
        apiClient = self.getSpaceOwnerAPIClient(spaceID)
        restrictions = apiClient.get('/spaces/'+str(spaceID)+'/restrictions/')
        self.assertEqual(len(restrictions.data), self.RESTRICTIONS_PER_SPACE)
