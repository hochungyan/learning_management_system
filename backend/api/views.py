from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """
    A serializer class for Profile model instances.

    Args:
        model: The model class that the serializer should use.
        fields: The fields to include in the serialization.

    Returns:
        None
    """

    serializer_class = MyTokenObtainPairSerializer
