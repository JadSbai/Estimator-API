import json
from rest_framework.test import RequestsClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests.factories import UserFactory
from django.utils import timezone
from api.tests.helpers import authenticate, make_new_search, get_user_searches


class MakeSearchViewTestCase(APITestCase):
    """Tests of the create view from the SearchViewSet."""

    def setUpTestData(self):
        self.client = RequestsClient()
        self.client2 = RequestsClient()
        self.url = reverse('search_list')
        self.user = UserFactory.create()
        self.user2 = UserFactory.create()
        self.user_token = authenticate(self.user)
        self.user2_token = authenticate(self.user2)

    def test_make_search_url(self):
        self.assertEqual(self.url, '/searches/')

    def test_successful_new_search(self):
        searches_before = get_user_searches(self.client, self.user_token, self.user)
        num_before = searches_before['count']

        result = make_new_search(self.client, self.user_token)

        searches_after = get_user_searches(self.client, self.user_token, self.user)
        num_after = searches_after['count']

        self.assertIn("url", result['result']['suggested_product']['description'])
        self.assertIn("price", result['result']['suggested_product']['description'])
        self.assertEqual(num_before + 1, num_after)

    def test_make_new_search_with_empty_string(self):
        resp = self.client.post(url=f'http://localhost:8000/searches/', params={
            'data': '',
            'date': timezone.now().isoformat()
        }, headers={'Authorization': f'Bearer {self.user_token}'})

        content = json.loads(resp.content)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('custom_message', content)
