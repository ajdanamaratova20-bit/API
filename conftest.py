import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from catalog.models import Category


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    User = get_user_model()

    def make_user(username='testuser', password='testpass123'):
        return User.objects.create_user(
            username=username,
            password=password
        )

    return make_user


@pytest.fixture
def auth_client(create_user):
    user = create_user()

    client = APIClient()

    response = client.post(
        '/api/token/',
        {
            'username': 'testuser',
            'password': 'testpass123'
        },
        format='json'
    )

    token = response.data['access']

    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )

    return client


@pytest.fixture
def category():
    return Category.objects.create(
        name='Phones',
        slug='phones'
    )