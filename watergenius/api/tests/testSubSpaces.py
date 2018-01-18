from api.tests.testSubSpacesSetup import SubSpaceTestSetup


class SubSpaceTest(SubSpaceTestSetup):

    def test_quantity_of_subspaces_per_space(self):
        subspaceID = next(iter(self.subspaceIDs.keys()))
        spaceID = self.subspaceIDs[subspaceID]
        apiClient = self.getSubSpaceOwnerAPIClient(subspaceID)
        subspaces = apiClient.get('/subspaces/?spaceid='+str(spaceID))
        self.assertEqual(len(subspaces.data), self.SUBSPACES_PER_SPACE)