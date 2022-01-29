import json
from rest_framework.test import RequestsClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.hashers import check_password
from api.models import User
from rest_framework.test import APITestCase
from api.tests.factories import UserFactory
from api.tests.helpers import authenticate


class ChangeProfileViewTestCase(APITestCase):
    """Tests of the create view from the SearchViewSet."""

    def setUpTestData(self):
        self.client = RequestsClient()
        self.user = UserFactory.create()
        self.url = reverse('change_password', kwargs={'pk': self.user.id})
        self.user_token = authenticate(self.user)

    def test_successful_change_password(self):
        before = User.objects.count()
        pass_data = {'new_password': 'Newpass123', 'confirm_password': 'Newpass123', 'current_password': 'Password123'}
        resp = self.client.patch(f'http://localhost:8000{self.url}', data=pass_data)
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        is_password_correct = check_password('Newpass123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_change_password_with_wrong_current_password(self):
        before = User.objects.count()
        pass_data = {'new_password': 'Newpass123', 'confirm_password': 'Newpass123', 'current_password': 'Yolo123'}
        resp = self.client.patch(f'http://localhost:8000{self.url}', data=pass_data)
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_change_password_with_bad_new_password(self):
        before = User.objects.count()
        pass_data = {'new_password': 'newpass', 'confirm_password': 'Newpass123', 'current_password': 'Password123'}
        resp = self.client.patch(f'http://localhost:8000{self.url}', data=pass_data)
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        is_password_correct = check_password('newpass', self.user.password)
        self.assertFalse(is_password_correct)

    def test_change_password_with_unmatching_passwords(self):
        before = User.objects.count()
        pass_data = {'new_password': 'Newpass123', 'confirm_password': 'Newpass1234', 'current_password': 'Password123'}
        resp = self.client.patch(f'http://localhost:8000{self.url}', data=pass_data)
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)


