# from api.tests.setup.subspacesSetup import SubSpaceTestSetup
#
#
# class EsysTestSetup(SubSpaceTestSetup):
#     ESYS_PER_SUBSPACE = 4
#
#     subspaceEsys = None  # Map<SubspaceID, [EsysID]>
#     esysIDs = None  # Map<EsysID, SubspaceID>
#
#     @classmethod
#     def setUpTestData(cls):
#         super(EsysTestSetup, cls).setUpTestData()
#
#         cls.subspaceEsys = dict()
#         cls.esysIDs = dict()
#
#         cls.registerEmbeddedSystems()
#
#     @classmethod
#     def registerEmbeddedSystems(cls):
#         for subspaceID in cls.subspaceIDs.keys():
#             cls.subspaceEsys[subspaceID] = list()
#             for i in range(0, cls.ESYS_PER_SUBSPACE):
#                 response = cls.postEmbeddedSystem(subspaceID, -9.142685, 38.736946, 5, 1,
#                                                   "Embedded System " + str(i),
#                                                   "password")
#                 esysID = response.data['esys_id']
#                 cls.subspaceEsys[subspaceID].append(esysID)
#                 cls.esysIDs[esysID] = subspaceID
#
#     @classmethod
#     def postEmbeddedSystem(cls, subspaceID, longitude, latitude, altitude, state, name, network_pass):
#         esys = {
#             "esys_sub": subspaceID,
#             "esys_local_long": longitude,
#             "esys_local_lat": latitude,
#             "esys_local_alt": altitude,
#             "esys_state": state,
#             "esys_name": name,
#             "esys_network_pass": network_pass
#         }
#         client = cls.getSubSpaceOwnerAPIClient(subspaceID)
#         return client.post('/embeddedsys/', esys, format='json')
#
#
#
#     @classmethod
#     def getEsysOwnerAPIClient(cls, esysID):
#         subspaceID = cls.esysIDs.get(esysID)
#         return cls.getSubSpaceOwnerAPIClient(subspaceID)
