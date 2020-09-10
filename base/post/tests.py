from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PostViewsTestCase(APITestCase):

    url = reverse('post-list')

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

    # POSTS-LIST

    def test_post_get_authenticated(self):  # GET
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_post_authenticated(self):  # POST
        response = self.client.post(self.url, {'title': "Ruby's post", 'body': "Great news!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_detail_retrieve_put_not_allowed_method(self):  # PUT
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_detail_retrieve_patch_not_allowed_method(self):  # PATCH
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_detail_retrieve_not_delete_allowed_method(self):  # DELETE
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # POSTS-DETAILS

    def test_post_detail_retrieve(self):
        # create post in order to retrieve
        response = self.client.post(self.url, {'title': "Ruby's post", 'body': "Great news!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse('post-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_detail_retrieve_not_allowed_method(self):
        response = self.client.post(reverse('post-detail', kwargs={'pk': 1}))  # POST
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # POSTS-LIKES

    def test_post_like_post(self):  # POST
        # create post in order to like
        response = self.client.post(self.url, {'title': "Ruby's post", 'body': "Great news!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('post-like', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_like_delete(self):  # DELETE
        # create post in order to like
        response = self.client.post(self.url, {'title': "Ruby's post", 'body': "Great news!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # like post in order to unlike
        response = self.client.post(reverse('post-like', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # unlike post
        response = self.client.delete(reverse('post-like', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AnalyticsListTestCase(APITestCase):

    url = reverse('likes-analytics')

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

    def test_analytics_authenticated(self):  # GET
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_analytics_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_analytics_not_allowed_method(self):  # POST
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
