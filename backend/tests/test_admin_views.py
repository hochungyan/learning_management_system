import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(email='admin@example.com', password='test')

@pytest.mark.django_db
def test_admin_login_redirects_to_login_page(api_client):
    """
    Tests that accessing the admin page without logging in redirects to the login page.

    Args:
        api_client (APIClient): The Django REST framework API client.

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 302 (redirect).
    """
    response = api_client.get(reverse('admin:index'))
    assert response.status_code == 302

@pytest.mark.django_db
def test_admin_login_successful(api_client, admin_user):
    """
    Tests that admin login is successful.

    Args:
        api_client (APIClient): The Django REST framework API client.
        admin_user (User): The admin user fixture.

    Returns:
        None

    Raises:
        AssertionError: If the login is not successful.
    """
    login_successful = api_client.login(email='admin@example.com', password='test')
    assert login_successful

@pytest.mark.django_db
def test_admin_access_after_logging_in(api_client, admin_user):
    """
    Tests that an authenticated admin can access the admin page.

    Args:
        api_client (APIClient): The Django REST framework API client.
        admin_user (User): The admin user fixture.

    Returns:
        None

    Raises:
        AssertionError: If the response status code is not 200.
    """
    api_client.force_login(admin_user)
    response = api_client.get(reverse('admin:index'))
    assert response.status_code == 200
