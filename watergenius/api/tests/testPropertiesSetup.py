from rest_framework.test import APITestCase, APIClient

from api.tests.testUsersSetup import UserTestSetup


class PropertyTestSetup(UserTestSetup):

    @classmethod
    def setUpTestData(cls):
        super(PropertyTestSetup, cls).setUpTestData()
