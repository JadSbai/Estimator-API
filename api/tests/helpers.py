import json
from rest_framework import status
from django.utils import timezone
import requests
from rest_framework_simplejwt.tokens import RefreshToken


def authenticate(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return access_token


def get_user_searches(client, token, user=None):
    if user:
        resp = client.get(url=f'http://localhost:8000/searches/',
                          headers={'Authorization': f'Bearer {token}'},
                          params={'user': user.id})
    else:
        resp = client.get(url=f'http://localhost:8000/searches/',
                          headers={'Authorization': f'Bearer {token}'})
    user_searches = json.loads(resp.content)
    return user_searches


def make_new_search(client, token):
    resp = client.post(url=f'http://localhost:8000/searches/', params={
        'data': 'MacbookPro',
        'date': timezone.now().isoformat()
    }, headers={'Authorization': f'Bearer {token}'})

    while resp.status_code == status.HTTP_200_OK:
        resp = client.post(url=f'http://localhost:8000/searches/', params={
            'data': 'MacbookPro',
            'date': timezone.now().isoformat()
        }, headers={'Authorization': f'Bearer {token}'})

    if resp.status_code != status.HTTP_201_CREATED:
        raise ValueError("A problem occurred when making the search: ", resp)

    result = json.loads(resp.content)
    return result
