from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationViewTestCase(APITestCase):

    def test_registration(self):
        data = {'username': 'ruby', 'email': 'ruby@gmail.com',
                'password': 'strong_pass', 'password2': 'strong_pass'}
        response = self.client.post('/api/user/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class JWTAuthViewsTests(APITestCase):

    def setUp(self):
        self.username = 'ruby'
        self.email = 'ruby@gmail.com'
        self.password = 'green'

        # Create user, need to register before requesting token
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.assertEqual(user.is_active, 1, 'Active User')

    def test_access_jwt_token(self):
        # Get token
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        access_token = response.data['access']

        # Use token to connect
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(reverse('activity'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_refresh_jwt_token(self):
        # Get token
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        refresh_token = response.data['refresh']

        # Use token to refresh
        response = self.client.post(reverse('token-refresh'), {'refresh': refresh_token, 'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)


class UserActivityListTestCase(APITestCase):

    url = reverse('activity')

    def setUp(self) -> None:
        self.username = 'ruby'
        self.password = 'strong_pass'

        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.access_token = self.get_token()
        self.authentication = self.authentication()

    def get_token(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        return response.data['access']

    def authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_user_activity_authenticated(self):  # GET
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_activity_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_activity_not_allowed_method(self):  # POST
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
