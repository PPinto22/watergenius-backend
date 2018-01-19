from rest_framework.test import APIClient, APITestCase


class APITestGlobalSetup(APITestCase):

    def setUp(self):
        self.anonymousClient = APIClient()
        self.superUserClient = self.getAPIClient("pinto@gmail.com")
        self.rua = self.getAPIClient("rua@gmail.com")
        self.freitas = self.getAPIClient("freitas@gmail.com")
        self.nine = self.getAPIClient("nine@gmail.com")

    def getAPIClient(self, email, password=None):
        if password is None:
            password = email.split('@')[0]
        loginResponse = self.loginRequest(email, password)
        apiClient = APIClient()
        apiClient.credentials(HTTP_AUTHORIZATION='JWT ' + loginResponse.data['token'])
        return apiClient

    def loginRequest(self, email, password):
        login = {
            'email': email,
            'password': password
        }
        return APIClient().post('/auth/', login, format='json')
