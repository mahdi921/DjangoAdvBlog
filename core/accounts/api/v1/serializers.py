from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import Profile
import jwt
from decouple import config
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from mail_templated import EmailMessage
from ..utils import EmailThreading


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        min_length=11, max_length=255, write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "password", "password2"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError(
                {"detail": "Password fields didn't match."}
            )
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password2", None)
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if user.is_verified is False:
                msg = {"details": "Please verify your Email."}
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if self.user.is_verified is False:
            msg = {"details": "Please verify your Email."}
            raise serializers.ValidationError(msg)
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError(
                {"detail": "Password fields didn't match."}
            )
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )
        return super().validate(attrs)


class ProfileSeriaizer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "email", "first_name", "last_name", "avatar", "bio"]


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "User does not exist."}
            )
        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"detail": "User is already verified."}
            )
        attrs["user"] = user_obj
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    """
    serializer for user requesting a password reset
    """

    email = serializers.EmailField(required=True)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
            user_id = user_obj.id
            token = PasswordResetTokenGenerator().make_token(user=user_obj)
            encoded_token = urlsafe_base64_encode(force_bytes(token))
            enc_user_id = urlsafe_base64_encode(force_bytes(user_id))
            link = f"http://localhost:8000/accounts/api/v1/reset-password/ \
            confirm/{enc_user_id}/{encoded_token}"
            email_obj = EmailMessage(
                "email/password-reset.tpl",
                {"link": link},
                "m@m.com",
                to=[user_obj.email],
            )
            EmailThreading(email_obj).start()
        except User.DoesNotExist:
            attrs["user"] = None
        return super().validate(attrs)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    serializer for confirming the reset password
    """

    password = serializers.CharField()
    password1 = serializers.CharField()

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        """validate the password entered by the user"""
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(
                {"password": "Password fields did not match."}
            )
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)
