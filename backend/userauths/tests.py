import os

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from userauths.models import Profile

User = get_user_model()
password = os.getenv("TEST_PASSWORD")


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
        email="test@example.com", password=password
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
        password=password,
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
        password=password,
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
        email="profile@example.com", password=password
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
        password=password,
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
        email="image@example.com", password=password
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
        email="profile_str_no_name@example.com", password=password
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
        email="update@example.com", password=password
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
        email="delete@example.com", password=password
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
            password=password,
            username="noemail",
        )


@pytest.mark.django_db
def test_create_superuser():
    """
    Test creating a superuser.
    """
    superuser = User.objects.create_superuser(
        email="admin@example.com", password=password
    )
    # Check if the superuser is created correctly
    assert superuser.email == "admin@example.com"
    assert superuser.is_staff
    assert superuser.is_superuser
    # Check if a profile is automatically created for the superuser
    assert hasattr(superuser, "profile")
    assert isinstance(superuser.profile, Profile)

    # Test creating a superuser with custom fields
    custom_superuser = User.objects.create_superuser(
        email="custom_admin@example.com",
        password=password,
        full_name="Custom Admin",
    )
    assert custom_superuser.email == "custom_admin@example.com"
    assert custom_superuser.is_staff
    assert custom_superuser.is_superuser
    assert custom_superuser.full_name == "Custom Admin"

    # Test that is_staff and is_superuser can't be set to False
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="fail_admin@example.com",
            password=password,
            is_staff=False,
        )

    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="fail_admin@example.com",
            password=password,
            is_superuser=False,
        )


@pytest.mark.django_db
def test_create_superuser_setdefault_and_extra_fields():
    """
    Test the setdefault behavior and extra fields in create_superuser method.
    """
    User = get_user_model()
    # Test that explicitly setting is_staff and is_superuser to True works
    # and that extra fields are passed through
    superuser = User.objects.create_superuser(
        email="explicit@example.com",
        password=password,
        is_staff=True,
        is_superuser=True,
        full_name="Explicit Superuser",
    )
    assert superuser.is_staff
    assert superuser.is_superuser
    assert superuser.full_name == "Explicit Superuser"

    # Test that setting is_staff to False raises an error
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        User.objects.create_superuser(
            email="staff_false@example.com",
            password=password,
            is_staff=False,
        )
    # Test that setting is_superuser to False raises an error
    with pytest.raises(
        ValueError, match="Superuser must have is_superuser=True."
    ):
        User.objects.create_superuser(
            email="staff_false@example.com",
            password=password,
            is_superuser=False,
        )


@pytest.mark.django_db
def test_user_str_method():
    """
    Test the __str__ method of the User model.

    This test creates a User instance with a specific email and password, then
    checks if calling the __str__ method on the user object returns
    the expected email.

    Args:
        self

    Returns:
        None
    """
    User = get_user_model()
    user = User.objects.create_user(
        email="test@example.com", password=password
    )
    assert str(user) == "test@example.com"


@pytest.mark.django_db
def test():
    user = User.objects.create_user(
        email="test@test.com", username="customuser", password=password
    )
    assert user.full_name == "customuser"


@pytest.mark.django_db
def test_profile_full_name_update():
    """
    Test the update of the full_name attribute in the Profile model.

    This test creates a User instance, sets the full_name attribute
    of the associated Profile to an empty string, saves the
    profile triggering the save method,
    and then checks if the full_name has been updated to the username.

    Args:
        self

    Returns:
        None
    """
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password=password
    )
    user.refresh_from_db()
    # Get the associated profile
    profile = user.profile
    # Set the full_name to an empty string
    profile.full_name = ""
    # Save the profile, which should trigger the save method
    profile.save()
    # Refresh the profile from the database
    profile.refresh_from_db()
    # Assert that the full_name has been set to the username
    assert profile.full_name == "testuser"


@pytest.mark.django_db
class TestUserProfileSignal:

    def test_profile_created_on_user_creation(self):
        """
        Test the creation of a profile when a user is created.

        This test creates a new user and checks if a profile
        is created for the user with the correct full name.

        Args:
            self

        Returns:
            None
        """
        user = User.objects.create_user(
            username="newuser",
            email="newuser@example.com",
            password=password,
            full_name="New User",
        )

        assert hasattr(user, "profile")
        assert isinstance(user.profile, Profile)
        assert user.profile.full_name == "New User"

    def test_profile_updated_on_user_update(self):
        """
        Test the update of a profile when a user is updated.

        This test creates a user, updates the user's
        full name,saves the user, refreshes
        the user from the database,
        and then checks if the profile's full name
        has been updated accordingly.

        Args:
            self

        Returns:
            None
        """
        # Create a user
        user = User.objects.create_user(
            username="updateuser",
            email="updateuser@example.com",
            password=password,
            full_name="Update User",
        )

        # Update the user's full name
        user.full_name = "Updated User"
        user.save()

        # Refresh the user from the database
        user.refresh_from_db()

        # Check if the profile's full name was updated
        assert user.profile.full_name == "Updated User"

    def test_profile_not_created_if_exists(self):
        """
        Test the behavior when a profile is not created if it already exists.

        This test creates a user, updates the user's full name, saves the user,
        and then checks that no new profile is created and the existing
        profile is updated accordingly.

        Args:
            self

        Returns:
            None
        """
        # Create a user
        user = User.objects.create_user(
            username="existinguser",
            email="existinguser@example.com",
            password=password,
            full_name="Existing User",
        )

        # Count the number of profiles
        initial_profile_count = Profile.objects.count()

        # Update the user
        user.full_name = "Updated Existing User"
        user.save()

        # Check that no new profile was created
        assert Profile.objects.count() == initial_profile_count

        # Check that the existing profile was updated
        user.refresh_from_db()
        assert user.profile.full_name == "Updated Existing User"
