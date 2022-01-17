
from rest_framework.test import RequestsClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User


class MakeSearchViewTestCase(APITestCase):
    """Tests of the create view from the SearchViewSet."""

    def setUpTestData(self):
        self.client = RequestsClient()
        self.url = reverse('sign_up')

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign-up/')

    def test_successful_sign_up(self):
        before = User.objects.count()
        sign_up_data = {'first_name': 'Michel', 'last_name': 'Dupont', 'email': 'michel.dupont@gmail.com',
                        'password': 'Password123', 'confirm_password': 'Password123', 'location': 'UK'}
        resp = self.client.post(f'http://localhost:8000{self.url}', data=sign_up_data)
        after = User.objects.count()
        self.assertEqual(before + 1, after)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=sign_up_data['email']).exists())
        michel = User.objects.get(email=sign_up_data['email'])
        self.assertTrue(michel.is_authenticated)

    def test_sign_up_with_unmatching_password(self):
        before = User.objects.count()
        sign_up_data = {'first_name': 'Michel', 'last_name': 'Dupont', 'email': 'michel.dupont@gmail.com',
                        'password': 'Password123', 'confirm_password': 'Password12', 'location': 'UK'}
        resp = self.client.post(f'http://localhost:8000{self.url}', data=sign_up_data)
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertFalse(User.objects.filter(email=sign_up_data['email']).exists())
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_missing_info(self):
        before = User.objects.count()
        sign_up_data = {'last_name': 'Dupont', 'email': 'michel.dupont@gmail.com',
                        'password': 'Password123', 'confirm_password': 'Password123', 'location': 'UK'}
        resp = self.client.post(f'http://localhost:8000{self.url}', data=sign_up_data)
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertFalse(User.objects.filter(email=sign_up_data['email']).exists())
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_duplicate_email(self):
        User.objects.create_user(first_name='Michel', last_name='Dupont', email='michel.dupont@gmail.com',
                                 password='Password123', location='UK')
        before = User.objects.count()
        sign_up_data = {'first_name': 'Michel', 'last_name': 'Dupont', 'email': 'michel.dupont@gmail.com',
                        'password': 'Password123', 'confirm_password': 'Password123', 'location': 'UK'}
        resp = self.client.post(f'http://localhost:8000{self.url}', data=sign_up_data)
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_bad_password(self):
        before = User.objects.count()
        sign_up_data = {'first_name': 'Michel', 'last_name': 'Dupont', 'email': 'michel.dupont@gmail.com',
                        'password': 'badpass', 'confirm_password': 'badpass', 'location': 'UK'}
        resp = self.client.post(f'http://localhost:8000{self.url}', data=sign_up_data)
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email=sign_up_data['email']).exists())
