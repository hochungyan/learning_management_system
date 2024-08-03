import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from userauths.models import Profile

User = get_user_model()


@pytest.mark.django_db
def test_user_creation_without_username():
    """
    Test creating a user without providing a username.

    Args:
        None

    Returns:
        None
    """
    user = User.objects.create_user(
        email="test@example.com", password="testpassword"
    )
    assert user.email == "test@example.com"
    assert user.username == "test"
    assert user.full_name == "test"
    assert hasattr(user, "profile")
    assert isinstance(user.profile, Profile)


@pytest.mark.django_db
def test_user_creation_with_username():
    """
    Test creating a user with a specified username.

    Args:
        None

    Returns:
        None
    """
    user = User.objects.create_user(
        email="test@example.com",
        password="testpassword",
        username="customuser",
    )
    assert user.email == "test@example.com"
    assert user.username == "customuser"
    assert user.full_name == "customuser"
    assert hasattr(user, "profile")
    assert isinstance(user.profile, Profile)


@pytest.mark.django_db
def test_user_creation_with_all_fields():
    """
    Test creating a user with all required fields provided.

    Args:
        None

    Returns:
        None
    """
    user = User.objects.create_user(
        email="full@example.com",
        password="testpassword",
        username="fulluser",
        full_name="Full User",
    )
    assert user.email == "full@example.com"
    assert user.username == "fulluser"
    assert user.full_name == "Full User"
    assert hasattr(user, "profile")
    assert isinstance(user.profile, Profile)
    assert user.profile.full_name == "Full User"


@pytest.mark.django_db
def test_profile_creation():
    """
    Test profile creation when a user is created.

    Args:
        None

    Returns:
        None
    """
    user = User.objects.create_user(
        email="profile@example.com", password="testpassword"
    )
    assert hasattr(user, "profile")
    assert isinstance(user.profile, Profile)
    assert user.profile.user == user
    assert user.profile.full_name == "profile"


@pytest.mark.django_db
def test_profile_str_method():
    """
    Test the string representation of a profile with a full name.

    Args:
        None

    Returns:
        None
    """
    user = User.objects.create_user(
        email="profile_str@example.com",
        password="testpassword",
        full_name="Test User",
    )
    print(f"User full_name: {user.full_name}")
    print(f"User username: {user.username}")
    print(f"Profile full_name: {user.profile.full_name}")
    print(f"Profile __str__: {str(user.profile)}")
    assert str(user.profile) == "Test User"


@pytest.mark.django_db
def test_profile_image_upload():
    """
    Test uploading an image to a user's profile.

    Args:
        None

    Returns:
        None
    """
    user = User.objects.create_user(
        email="image@example.com", password="testpassword"
    )
    image = SimpleUploadedFile(
        "test_image.jpg", b"file_content", content_type="image/jpeg"
    )
    user.profile.image = image
    user.profile.save()
    assert "test_image" in user.profile.image.name


@pytest.mark.django_db
def test_profile_str_method_without_full_name():
    """
    Test the string representation of a profile without a full name.

    Args:
        None

    Returns:
        None
    """
    user = User.objects.create_user(
        email="profile_str_no_name@example.com", password="testpassword"
    )
    print(f"User full_name: {user.full_name}")
    print(f"User username: {user.username}")
    print(f"Profile full_name: {user.profile.full_name}")
    print(f"Profile __str__: {str(user.profile)}")
    assert str(user.profile) == user.username


@pytest.mark.django_db
def test_profile_update():
    """
    Test updating a user's profile information.

    Args:
        None

    Returns:
        None
    """
    user = User.objects.create_user(
        email="update@example.com", password="testpassword"
    )
    user.profile.full_name = "Updated Name"
    user.profile.country = "Test Country"
    user.profile.about = "Test About"
    user.profile.save()

    updated_user = User.objects.get(email="update@example.com")
    assert updated_user.profile.full_name == "Updated Name"
    assert updated_user.profile.country == "Test Country"
    assert updated_user.profile.about == "Test About"


@pytest.mark.django_db
def test_profile_cascade_delete():
    """
    Test that a profile is deleted when its associated user is deleted.

    Args:
        None

    Returns:
        None
    """
    user = User.objects.create_user(
        email="delete@example.com", password="testpassword"
    )
    profile_id = user.profile.id
    user.delete()
    with pytest.raises(Profile.DoesNotExist):
        Profile.objects.get(id=profile_id)


@pytest.mark.django_db
def test_user_creation_without_email():
    """
    Test creating a user without providing an email.

    Args:
        None

    Returns:
        None

    Raises:
        ValueError: If the email field is not set.
    """
    with pytest.raises(ValueError, match="The Email field must be set"):
        User.objects.create_user(
            email="",
            password="testpassword",
            username="noemail",
        )
