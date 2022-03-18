from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from users.views import UserDetailsView, user_detail_from_jwt

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('details/<int:uid>', UserDetailsView.as_view(), name="user_details"),
    path('details/jwt', user_detail_from_jwt, name="user_details_jwt")
]
