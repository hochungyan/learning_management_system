import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation_without_username():
    user = User.objects.create_user(email='test@example.com', password='testpassword')
    assert user.email == 'test@example.com'
    assert user.username == 'test'
    assert user.full_name == 'test'

@pytest.mark.django_db
def test_user_creation_with_username():
    user = User.objects.create_user(email='test@example.com', password='testpassword', username='customuser')
    assert user.email == 'test@example.com'
    assert user.username == 'customuser'
    assert user.full_name == 'customuser'

@pytest.mark.django_db
def test_user_creation_with_all_fields():
    user = User.objects.create_user(email='full@example.com', password='testpassword', username='fulluser', full_name='Full User')
    assert user.email == 'full@example.com'
    assert user.username == 'fulluser'
    assert user.full_name == 'Full User'