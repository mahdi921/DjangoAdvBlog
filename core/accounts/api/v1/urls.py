from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "api-v1"

urlpatterns = [
    # registration
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
]
