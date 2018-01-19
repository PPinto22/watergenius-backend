from rest_framework import status

from api.tests.globalSetup import APITestGlobalSetup


class SpaceTest(APITestGlobalSetup):
    fixtures = ['v1/users', 'v1/properties', 'v1/spaces']

    def test_get_spaces_by_property(self):
        spaces = self.rua.get('/spaces/?propertyid=1')
        self.assertEqual(len(spaces.data), 2)

    def test_get_spaces_by_manager(self):
        spaces = self.freitas.get('/spaces/?managerid=freitas@gmail.com')
        self.assertEqual(len(spaces.data), 1)

    def test_get_time_restrictions(self):
        restrictions = self.nine.get('/spaces/3/restrictions/')
        self.assertEqual(len(restrictions.data), 2)

    def test_post_space(self):
        space = {
            "space_name": "Name 4",
            "space_description": "Description 4",
            "space_irrigation_hour": 20,
            "space_property": 2,
            "space_plant_type": 1
        }
        post_response = self.rua.post('/spaces/', space, format='json')
        self.assertTrue(status.is_success(post_response.status_code))
        spaces = self.rua.get('/spaces/?propertyid=2')
        self.assertEqual(len(spaces.data), 1)

    def test_post_time_restriction(self):
        restriction = {
            "time_restriction_begin": "2018-01-18T22:47:03.603Z",
            "time_restriction_end": "2018-01-19T00:47:03.603Z",
            "time_restriction_space": 1
        }
        post_response = self.rua.post('/spaces/1/restrictions/', restriction, format='json')
        self.assertTrue(status.is_success(post_response.status_code))
        restrictions = self.rua.get('/spaces/1/restrictions/')
        self.assertEqual(len(restrictions.data), 2)

    def test_update_space(self):
        space = {
            'space_name': 'New name',
            'space_description': 'New description'
        }
        response = self.rua.put('/spaces/1/', space, format='json')
        self.assertTrue(status.is_success(response.status_code))
        for attr in space:
            self.assertEqual(space[attr], response.data[attr])

    def test_delete_empty_space(self):
        response = self.rua.delete('/spaces/2/')
        self.assertTrue(status.is_success(response.status_code))
        spaces = self.rua.get('/spaces/?propertyid=1')
        self.assertEqual(len(spaces.data), 1)

    def test_delete_cascade_space(self):
        response = self.rua.delete('/spaces/1/')
        self.assertTrue(status.is_success(response.status_code))
        spaces = self.rua.get('/spaces/?propertyid=1')
        self.assertEqual(len(spaces.data), 1)
        subspaces = self.rua.get('/subspaces/?ownerid=rua@gmail.com')
        self.assertEqual(len(subspaces.data), 0)