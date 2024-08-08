from django.urls import path

from . import views

urlpatterns = [
    path(
        "user/token",
        views.MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
]
