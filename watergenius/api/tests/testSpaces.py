from api.tests.testSpacesSetup import SpaceTestSetup


class SpaceTest(SpaceTestSetup):

    def test_quantity_of_spaces_per_property(self):
        spaceID = next(iter(self.spaceIDs))
        propID = self.spaceIDs[spaceID]
        apiClient = self.getSpaceOwnerAPIClient(spaceID)
        spaces = apiClient.get('/spaces/?propertyid='+str(propID))
        self.assertEqual(len(spaces.data), self.SPACES_PER_PROP)

    def test_quantity_of_time_restrictions_per_space(self):
        spaceID = next(iter(self.spaceIDs))
        apiClient = self.getSpaceOwnerAPIClient(spaceID)
        restrictions = apiClient.get('/spaces/'+str(spaceID)+'/restrictions/')
        self.assertEqual(len(restrictions.data), self.RESTRICTIONS_PER_SPACE)
