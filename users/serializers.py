from django.db.models import fields
from .models import CustomUser
from rest_framework import serializers
from django.contrib import auth
from . import google
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import os
import string
import random

from users import models


class CustomUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'gender',
                  'age', 'email_verified', 'mobile_verified']
        depth = 1


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255, min_length=3, allow_blank=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['user_id', 'email', 'password', 'tokens','staff_type']

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        try:
            filtered_user_by_email = CustomUser.objects.get(
                email__iexact=email)
            if filtered_user_by_email and filtered_user_by_email.auth_provider != 'email':
                raise AuthenticationFailed(
                    detail='Please continue your login using ' +
                    filtered_user_by_email.auth_provider
                )
        except:
            print("User does not exist.")

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.email_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'user_id': user.user_id,
            'email': user.email,
            'tokens': user.tokens(),
            'staff_type': user.staff_type
        }


class PhoneLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.RegexField(
        '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$', max_length=15)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'user_id', 'tokens']

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        try:
            user_obj = CustomUser.objects.get(
                phone_number__icontains=phone_number)
            if user_obj:
                # send OTP
                # validate OTP
                return {
                    'user_id': user_obj.user_id,
                    'phone_number': user_obj.phone_number,
                    'tokens': user_obj.tokens()
                }
        except:
            raise serializers.ValidationError({
                'error': 'User does not exists.'
            })
        return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    # redirect_url = serializers.CharField(max_length=500, allow_blank=True)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    user_id = serializers.CharField(read_only=True)

    class Meta:
        fields = ['password']

    def update(self, instance, validated_data):
        try:
            user = CustomUser.objects.get(
                user_id=validated_data.get('user_id', instance.user_id))
            user.set_password(validated_data.get(
                'password', instance.password))
            user.save()
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

        return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.tokenRefresh = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        default_error_message = {
            'bad_token': ('Token is expired or invalid')
        }

        try:
            RefreshToken(self.tokenRefresh).blacklist()
            return {
                'success': 'Logged Out'
            }

        except TokenError:
            return default_error_message


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'staff_type', 'password']

 #####No need for custom validation as validation now happens in the frontend#####

    # default_error_messages = {
    #     'username': 'The username should only contain alphanumeric characters'
    #     }
    #
    # def validate(self, attrs):
    #     print(attrs)
    #     email = attrs.get('email', '')
    #     username = attrs.get('username', '')
    #
    #     if not username.isalnum():
    #         raise serializers.ValidationError(
    #             self.default_error_messages)
        # return attrs

    # def create(self, validated_data):
    #     return CustomUser.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


class MobileVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate(self, attrs):
        auth_token = attrs['auth_token']
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')

        email = user_data['email']
        name = user_data['name']
        username = str(name).replace(' ', '_').lower()

        try:
            filtered_user_by_email = CustomUser.objects.get(
                email__iexact=email)
            if filtered_user_by_email:
                return {
                    'user_id': filtered_user_by_email.user_id,
                    'tokens': filtered_user_by_email.tokens()
                }
        except:
            randomString = string.ascii_letters + string.digits
            password = ''.join(random.choice(randomString) for i in range(10))

            CustomUser.objects.create_user(
                email=email, username=username, password=password, auth_provider='google', email_verified=True)
            return {
                'newUser': "User does not exist. New User Created"
            }


class ApproverSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'email']
