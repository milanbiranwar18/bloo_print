from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user.models import User


class UserAuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(first_name="milan",last_name="biranwar",location="pune",
                    username='testuser', password='testpassword', email="newuser@example.com", mobile_num=918785220)

    def test_user_registration(self):
        url = reverse('register_user')
        data = {
            "first_name":"milan",
            "last_name":"biranwar",
            "location":"pune",
            "mobile_num":918785220,
            "email":"milanbiranwar@gmail.com",
            "username":"milan1",
            "password":"1234"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully')

    def test_user_login(self):
        url = reverse('login_user')
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access token', response.data)

    def test_user_login_invalid_credentials(self):
        url = reverse('login_user')
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        # Log in first to get the refresh token
        login_url = reverse('login_user')
        login_data = {"username": "testuser", "password": "testpassword"}
        login_response = self.client.post(login_url, login_data, format='json')

        refresh_token = login_response.data['refresh token']
        logout_url = reverse('logout_user')
        response = self.client.post(logout_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data['message'], "Logout successfully")

