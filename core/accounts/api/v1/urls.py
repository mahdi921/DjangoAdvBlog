from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "api-v1"

urlpatterns = [
    path('registration/',
         views.RegistrationApiView.as_view(),
         name='registration'
         ),
    path(
        'token/login/',
        views.CustomObtainAuthToken.as_view(),
        name='token-login'
    ),
    path(
        'token/logout/',
        views.CustomDiscardAuthToken.as_view(),
        name='token-logout'
    ),
    path(
        'change-password/',
        views.ChangePasswordApiView.as_view(),
        name='change-password'
    ),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
