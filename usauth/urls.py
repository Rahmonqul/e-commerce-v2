from django.urls import path
from .views import RegisterUserAPIView, ProfileAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]