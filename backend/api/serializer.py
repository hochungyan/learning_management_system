from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from userauths.models import Profile, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["full_name"] = user.full_name
        token["username"] = user.username

        return token


class UserSerializer(serializers.ModelSerializer):
    """
    A class to define metadata options for a serializer.

    Args:
        model: The model class that the serializer should use.
        fields: The fields to include in the serialization.

    Returns:
        None
    """

    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    """
    A serializer class for Profile model instances.

    Args:
        model: The model class that the serializer should use.
        fields: The fields to include in the serialization.

    Returns:
        None
    """

    class Meta:
        model = Profile
        fields = "__all__"
