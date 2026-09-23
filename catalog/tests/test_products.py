import pytest
from catalog.models import Product


@pytest.mark.django_db
def test_product_list(api_client):
    response = api_client.get('/api/products/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_product_price_filter(api_client, category):
    Product.objects.create(
        name='Cheap Phone',
        description='Test',
        price=100,
        in_stock=5,
        category=category
    )

    Product.objects.create(
        name='Expensive Phone',
        description='Test',
        price=1000,
        in_stock=5,
        category=category
    )

    response = api_client.get(
        '/api/products/?min_price=200&max_price=900'
    )

    assert response.status_code == 200
    assert response.data['count'] == 0


@pytest.mark.django_db
def test_anonymous_cannot_create_product(api_client, category):
    data = {
        'name': 'Test Phone',
        'description': 'Test',
        'price': 500,
        'in_stock': 5,
        'category': category.id
    }

    response = api_client.post(
        '/api/products/',
        data,
        format='json'
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_authenticated_can_create_product(auth_client, category):
    data = {
        'name': 'Test Phone',
        'description': 'Test',
        'price': 500,
        'in_stock': 5,
        'category': category.id
    }

    response = auth_client.post(
        '/api/products/',
        data,
        format='json'
    )

    assert response.status_code == 201
    assert response.data['owner'] == 'testuser'


@pytest.mark.django_db
def test_negative_price_rejected(auth_client, category):
    data = {
        'name': 'Test Phone',
        'description': 'Test',
        'price': -100,
        'in_stock': 5,
        'category': category.id
    }

    response = auth_client.post(
        '/api/products/',
        data,
        format='json'
    )

    assert response.status_code == 400