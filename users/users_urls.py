from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers
router = routers.DefaultRouter()
router.register('', UserViewSet)
app_name = "users"

urlpatterns = [
    path('profile/', include(router.urls)),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    # path('mobile-verify/', VerifyMobile.as_view(), name='mobile-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('google/', GoogleSocialAuthView.as_view()),
    path('verify-aprover/', VerifyAprovers.as_view(), name='aprover-verify')
]
