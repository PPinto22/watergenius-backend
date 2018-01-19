from datetime import datetime

from django.utils import timezone
from rest_framework import status

from api.tests.globalSetup import APITestGlobalSetup


class UserTest(APITestGlobalSetup):
    fixtures = ['v2/users']

    def test_login_incorrect_password(self):
        response = self.loginRequest('pinto@gmail.com', 'incorrect')
        self.assertTrue(status.is_client_error(response.status_code))

    def test_login_correct(self):
        response = self.loginRequest('pinto@gmail.com', 'pinto')
        self.assertTrue(status.is_success(response.status_code))

    def test_validate_number_of_users(self):
        usersRequest = self.superUserClient.get('/users/')
        self.assertEqual(len(usersRequest.data), 4)

    def test_get_user_validate_superuser_info(self):
        userRequest = self.superUserClient.get('/users/pinto@gmail.com/')
        self.assertEqual(userRequest.data['email'], 'pinto@gmail.com')
        self.assertEqual(userRequest.data['first_name'], 'Pedro')
        self.assertEqual(userRequest.data['last_name'], 'Pinto')
        self.assertEqual(userRequest.data['is_superuser'], True)
        date_joined = datetime.strptime(userRequest.data['date_joined'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # FIXME isto é necessário pq date_joined no JSON vai sem timezone
        date_joined = timezone.make_aware(date_joined, timezone.get_default_timezone())
        self.assertLess(date_joined, timezone.now())

    def test_valid_registration(self):
        response = self.registerUserRequest("new@gmail.com", "new", "John", "Doe")
        return self.assertTrue(status.is_success(response.status_code))

    def registerUserRequest(self, email, password, first_name, last_name, is_superuser=False):
        client = self.anonymousClient
        user = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
        if is_superuser:
            user['is_superuser'] = is_superuser
            client = self.superUserClient

        return client.post('/register/', user, format='json')
