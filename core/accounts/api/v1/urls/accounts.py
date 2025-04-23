from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .. import views


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
    path('test-email/', views.TestEmailSend.as_view(), name='test-email'),
    path('activation/confirm/<str:token>',
         views.ActivationApiView.as_view(), name='activation'),
    path('activation/resend/', views.ActivationResendApiView.as_view(),
         name='activation-resend'),
    path(
        'change-password/',
        views.ChangePasswordApiView.as_view(),
        name='change-password'
    ),
    path('reset-password/',
         views.ResetPasswordApiView.as_view(),
         name='reset-password'
         ),
    path('reset-password/confirm/<str:token>',
         views.ResetPasswordConfirmApiView.as_view(),
         name='reset-password-confirm'),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
