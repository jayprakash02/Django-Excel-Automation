from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
import uuid
from phone_field import PhoneField
from .managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

AUTH_PROVIDERS = {'google': 'google', 'email': 'email'}
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('N', 'Prefer not to say'),
)
STAFF = (
    ('C', 'Creator'),
    ('A', 'Approver'),
)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    phone_number = PhoneField(blank=True)
    gender = models.CharField(max_length=32, choices=GENDER, default='N')
    age = models.IntegerField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    staff_type = models.CharField(max_length=32,choices=STAFF,default='C')
    is_staff = models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    mobile_verified = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
    notification = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
