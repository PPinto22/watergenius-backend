from api.tests.setup.usersSetup import UserTestSetup


class PropertyTestSetup(UserTestSetup):
    PROPS_PER_USER = 2
    MANAGERS_PER_PROP = 1  # Not counting the owner

    userProperties = None  # Map<OwnerEmail, [propIDs]>
    propertyIDs = None  # Map<PropID, OwnerEmail>

    @classmethod
    def setUpTestData(cls):
        super(PropertyTestSetup, cls).setUpTestData()
        cls.userProperties = dict()
        cls.propertyIDs = dict()

        if cls.MANAGERS_PER_PROP >= len(cls.regularClients):
            raise Exception("Not enough users for that many managers!")
        cls.registerPropertiesAndManagers()
        for user in cls.userProperties.keys():
            for prop in cls.userProperties.get(user):
                cls.propertyIDs[prop] = user

    @classmethod
    def registerPropertiesAndManagers(cls):
        emails = list(cls.regularClients.keys())
        for i in range(0, len(emails)):
            email = emails[i]
            cls.userProperties[email] = list()
            apiClient = cls.regularClients.get(email)
            for j in range(0, cls.PROPS_PER_USER):
                response = cls.postProperty(email,
                                            "Name " + str(j + 1),
                                            "Description " + str(j + 1),
                                            "Address " + str(j + 1))
                propID = response.data['prop_id']
                cls.userProperties[email].append(propID)
                cls.postPropManagers(emails, email, propID, i, j)

    @classmethod
    def postPropManagers(cls, emails, ownerEmail, propID, ownerIdx, propIdx):
        ownerAPIClient = cls.regularClients[ownerEmail]
        for i in range(0, cls.MANAGERS_PER_PROP):
            managerIdx = (ownerIdx + propIdx + i) % len(emails)
            if managerIdx == ownerIdx:
                managerIdx = (managerIdx + 1) % len(emails)
            managerEmail = emails[managerIdx]
            ownerAPIClient.post('/properties/' + str(propID) + '/managers/' + managerEmail + '/')

    @classmethod
    def postProperty(cls, email, name, description, address):
        apiClient = cls.regularClients.get(email)
        property = {
            "prop_name": name,
            "prop_description": description,
            "prop_address": address,
            "prop_owner": email
        }
        return apiClient.post("/properties/", property, format='json')

    @classmethod
    def getPropOwnerAPIClient(cls, propID):
        return cls.regularClients.get(cls.propertyIDs.get(propID))
