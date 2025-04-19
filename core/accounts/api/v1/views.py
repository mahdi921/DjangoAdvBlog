from rest_framework import generics
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSeriaizer,
    ActivationResendSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from accounts.models import Profile
from accounts.api.utils import EmailThreading
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from decouple import config


User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data['email']
        data = {
            'email': email,
            'message': 'User registered successfully'
        }
        user_obj = get_object_or_404(User, email=email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl',
                                 {'token': token},
                                 'm@m.com',
                                 to=[email],
                                 )
        EmailThreading(email_obj).start()
        data = {
            'details': 'Email sent successfully'
        }
        return Response(
            data,
            status=status.HTTP_201_CREATED
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        return access


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    Model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, query_set=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_pwd = serializer.validated_data.get('old_password')
            if not self.object.check_password(old_pwd):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(
                serializer.validated_data.get('new_password')
            )
            self.object.save()
            data = {
                'detail': 'Password updated successfully',
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSeriaizer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestEmailSend(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        self.email = 'a@m.com'
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl',
                                 {'token': token},
                                 'm@m.com',
                                 to=[self.email],
                                 )
        EmailThreading(email_obj).start()
        data = {
            'details': 'Email sent successfully'
        }
        return Response(data, status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        return access


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        # decode -> user_id
        try:
            token = jwt.decode(token, config('SECRET_KEY'),
                               algorithms=['HS256'])
            user_id = token.get('user_id')

        except jwt.ExpiredSignatureError:
            return Response(
                {'details': 'Token expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.InvalidSignatureError:
            return Response(
                {'details': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.DecodeError:
            return Response(
                {'details': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response(
                {'details': 'User already activated'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_obj.is_verified = True
        user_obj.save()
        data = {
            'details': 'User activated successfully'
        }
        return Response(data, status=status.HTTP_200_OK)


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        user_obj = serializer.validated_data['user']
        token = self.get_tokens_for_user(user_obj)
        
        email_obj = EmailMessage(
                        'email/activation_email.tpl',
                        {'token': token},
                        'm@m.com',
                        to=[user_obj.email],
                    )
        
        EmailThreading(email_obj).start()
        
        data = {
            'details': 'Email resent successfully'
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        return access
