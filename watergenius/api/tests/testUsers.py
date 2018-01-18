from datetime import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import User
from api.tests.testUsersSetup import UserTestSetup


class UserTest(UserTestSetup):

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
