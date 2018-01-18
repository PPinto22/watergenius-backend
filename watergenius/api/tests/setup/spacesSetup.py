from api.models import PlantType
from api.tests.setup.propertiesSetup import PropertyTestSetup
import datetime


class SpaceTestSetup(PropertyTestSetup):
    SPACES_PER_PROP = 2
    RESTRICTIONS_PER_SPACE = 2
    RESTRICTION_DURATION_HOURS = 2
    HOURS_BETWEEN_RESTRICTIONS = 12

    plantIDs = None  # Plant IDs
    propertySpaces = None  # Map<PropID, [SpaceID]>
    spaceIDs = None  # Map<SpaceID, PropID>

    @classmethod
    def setUpTestData(cls):
        super(SpaceTestSetup, cls).setUpTestData()

        cls.plantIDs = list()
        cls.propertySpaces = dict()
        cls.spaceIDs = dict()

        cls.registerPlants()
        cls.registerSpacesAndRestrictions()

    @classmethod
    def registerSpacesAndRestrictions(cls):
        for prop in cls.propertyIDs.keys():
            cls.propertySpaces[prop] = list()
            ownerClient = cls.getPropOwnerAPIClient(prop)
            for i in range(0, cls.SPACES_PER_PROP):
                response = cls.postSpace("Name " + str(i + 1),
                                         "Description " + str(i + 1),
                                         (20 + i) % 24,
                                         prop,
                                         cls.plantIDs[0]
                                         )
                spaceID = response.data['space_id']
                cls.propertySpaces.get(prop).append(spaceID)
                cls.spaceIDs[spaceID] = prop
                cls.addTimeRestrictions(spaceID)

    @classmethod
    def addTimeRestrictions(cls, spaceID):
        ownerClient = cls.getSpaceOwnerAPIClient(spaceID)
        date_begin = datetime.datetime.now()
        for i in range(0, cls.RESTRICTIONS_PER_SPACE):
            date_begin = datetime.datetime.now() + \
                         i * (datetime.timedelta(hours=cls.RESTRICTION_DURATION_HOURS) +
                              datetime.timedelta(hours=cls.HOURS_BETWEEN_RESTRICTIONS))
            date_end = date_begin + datetime.timedelta(hours=cls.RESTRICTION_DURATION_HOURS)
            cls.postTimeRestriction(spaceID, str(date_begin), str(date_end))

    @classmethod
    def postTimeRestriction(cls, spaceID, date_begin, date_end):
        restriction = {
            "time_restriction_begin": date_begin,
            "time_restriction_end": date_end,
            "time_restriction_space": spaceID
        }
        ownerClient = cls.getSpaceOwnerAPIClient(spaceID)
        return ownerClient.post('/spaces/'+str(spaceID)+'/restrictions/', restriction, format='json')

    @classmethod
    def postSpace(cls, name, description, irrigation_hour, propID, plantType):
        space = {
            "space_name": name,
            "space_description": description,
            "space_irrigation_hour": irrigation_hour,
            "space_property": propID,
            "space_plant_type": plantType
        }
        ownerClient = cls.getPropOwnerAPIClient(propID)
        return ownerClient.post('/spaces/', space, format='json')

    @classmethod
    def registerPlants(cls):
        plant = PlantType()
        plant.plant_type_name = "Grass"
        plant.save()
        cls.plantIDs.append(plant.plant_type_id)

    @classmethod
    def getSpaceOwnerAPIClient(cls, spaceID):
        propID = cls.spaceIDs.get(spaceID)
        return cls.getPropOwnerAPIClient(propID)
