import json

from rest_framework.test import RequestsClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User
from api.tests.factories import UserFactory
from api.tests.helpers import authenticate


class LoginViewTestCase(APITestCase):
    """Tests of the create view from the SearchViewSet."""

    def setUpTestData(self):
        self.client = RequestsClient()
        self.url = reverse('login')
        self.user = UserFactory.create()

    def test_login_url(self):
        self.assertEqual(self.url, '/login/')

    def test_successful_login(self):
        login_data = {'email': self.user.email, 'password': 'Password123'}
        resp = self.client.post(f'http://localhost:8000{self.url}', data=login_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        result = json.loads(resp.content)
        self.assertIn('access', result)
        self.assertIn('refresh', result)
        self.assertIn('user_id', result)

    def test_login_with_wrong_email(self):
        login_data = {'email': 'lol@gmail.com', 'password': 'Password123'}
        resp = self.client.post(f'http://localhost:8000{self.url}', data=login_data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        result = json.loads(resp.content)
        self.assertNotIn('access', result)
        self.assertNotIn('refresh', result)
        self.assertNotIn('user_id', result)

    def test_login_with_wrong_password(self):
        login_data = {'email': self.user.email, 'password': 'toto'}
        resp = self.client.post(f'http://localhost:8000{self.url}', data=login_data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        result = json.loads(resp.content)
        self.assertNotIn('access', result)
        self.assertNotIn('refresh', result)
        self.assertNotIn('user_id', result)
