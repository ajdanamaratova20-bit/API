import pytest


@pytest.mark.django_db
def test_register_login_me(api_client):
    # 1. Регистрация
    register_data = {
        'username': 'newuser',
        'password': 'testpass123'
    }

    register_response = api_client.post(
        '/api/register/',
        register_data,
        format='json'
    )

    assert register_response.status_code == 201

    # 2. Логин
    login_data = {
        'username': 'newuser',
        'password': 'testpass123'
    }

    login_response = api_client.post(
        '/api/token/',
        login_data,
        format='json'
    )

    assert login_response.status_code == 200

    access_token = login_response.data['access']

    # 3. GET /api/me/
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {access_token}'
    )

    me_response = api_client.get('/api/me/')

    assert me_response.status_code == 200
    assert me_response.data['username'] == 'newuser'


@pytest.mark.django_db
def test_me_without_token(api_client):
    response = api_client.get('/api/me/')

    assert response.status_code == 401

@pytest.mark.django_db
def test_wrong_password(api_client, create_user):
    create_user(
        username='testwrong',
        password='correctpassword'
    )

    response = api_client.post(
        '/api/token/',
        {
            'username': 'testwrong',
            'password': 'wrongpassword'
        },
        format='json'
    )

    assert response.status_code == 401