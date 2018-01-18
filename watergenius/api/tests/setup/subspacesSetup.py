from api.tests.setup.spacesSetup import SpaceTestSetup


class SubSpaceTestSetup(SpaceTestSetup):
    SUBSPACES_PER_SPACE = 2

    spaceSubpaces = None  # Map<SpaceID, [SubpaceID]>
    subspaceIDs = None  # Map<SubspaceID, SpaceID>

    @classmethod
    def setUpTestData(cls):
        super(SubSpaceTestSetup, cls).setUpTestData()

        cls.spaceSubpaces = dict()
        cls.subspaceIDs = dict()

        cls.registerSubspaces()

    @classmethod
    def registerSubspaces(cls):
        for spaceID in cls.spaceIDs.keys():
            cls.spaceSubpaces[spaceID] = list()
            for i in range(0, cls.SUBSPACES_PER_SPACE):
                response = cls.postSubspace("Name " + str(i),
                                            "Description " + str(i),
                                            spaceID)
                subspaceID = response.data['sub_id']
                cls.spaceSubpaces[spaceID].append(subspaceID)
                cls.subspaceIDs[subspaceID] = spaceID

    @classmethod
    def postSubspace(cls, name, description, spaceID):
        subspace = {
            "sub_name": name,
            "sub_description": description,
            "sub_space_id": spaceID
        }
        client = cls.getSpaceOwnerAPIClient(spaceID)
        return client.post('/subspaces/', subspace, format='json')

    @classmethod
    def getSubSpaceOwnerAPIClient(cls, subspaceID):
        spaceID = cls.subspaceIDs.get(subspaceID)
        return cls.getSpaceOwnerAPIClient(spaceID)
