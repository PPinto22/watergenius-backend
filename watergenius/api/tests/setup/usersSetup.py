from rest_framework.test import APITestCase, APIClient


class UserTestSetup(APITestCase):
    anonymousClient = None  # An anonymous API Client
    superUserClient = None  # A super user API Client
    regularClients = None  # Map<Email, APIClient>
    regularEmail = None  # An email of a regular usar
    regularClient = None  # A regular user API Client

    @classmethod
    def setUpTestData(cls):
        cls.anonymousClient = APIClient()
        cls.regularClients = dict()

        cls.registerUserRequest('pinto@gmail.com', 'pinto', 'Pedro', 'Pinto', True)
        cls.superUserClient = cls.getAPIClient('pinto@gmail.com', 'pinto')

        cls.registerRegularUser('rua@gmail.com', 'rua', 'Rui', 'Rua')
        cls.registerRegularUser('nine@gmail.com', 'nine', 'Joao', 'Silva')
        cls.registerRegularUser('freitas@gmail.com', 'freitas', 'Rui', 'Freitas')

        cls.regularEmail = list(cls.regularClients)[0]
        cls.regularClient = cls.regularClients[cls.regularEmail]

    @classmethod
    def registerUserRequest(cls, email, password, first_name, last_name, is_superuser=False):
        user = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
        if is_superuser:
            user['is_superuser'] = is_superuser

        return cls.anonymousClient.post('/register/', user, format='json')

    @classmethod
    def registerRegularUser(cls, email, password, first_name, last_name):
        registerResponse = cls.registerUserRequest(email, password, first_name, last_name)
        userAPIClient = cls.getAPIClient(email, password)
        cls.regularClients[email] = userAPIClient

    @classmethod
    def getAPIClient(cls, email, password):
        loginResponse = cls.loginRequest(email, password)
        apiClient = APIClient()
        apiClient.credentials(HTTP_AUTHORIZATION='JWT ' + loginResponse.data['token'])
        return apiClient

    @classmethod
    def loginRequest(cls, email, password):
        login = {
            'email': email,
            'password': password
        }
        return cls.anonymousClient.post('/auth/', login, format='json')
