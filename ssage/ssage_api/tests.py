from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model



class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login(self):
        # create a user in the database
        user_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/v1/users/', user_data)
        self.assertEqual(response.status_code, 201)

        # try to login with the created user
        login_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/v1/token/login/', login_data)

        # assert that the login was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.data)


User = get_user_model()


class MultiUserLoginTestCase(TestCase):

    def test_multi_user_login(self):
        # Create two users
        user1 = User.objects.create_user(
            username='user1', password='testpassword1')
        user2 = User.objects.create_user(
            username='user2', password='testpassword2')

        # Create two API clients
        client1 = APIClient()
        client2 = APIClient()

        # Log in both users
        response1 = client1.post(
            '/v1/token/login/', {'username': 'user1', 'password': 'testpassword1'})
        response2 = client2.post(
            '/v1/token/login/', {'username': 'user2', 'password': 'testpassword2'})

        # Check if both logins were successful
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
       
