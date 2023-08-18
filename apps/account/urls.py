from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from apps.account.apis.authentication import SignInAPI, sign_out, AuthenticationAPI, ForgetPasswordAPI, \
    EmailAuthenticationAPI

from .apis.profile import profile_api, profile_avatar_api

urlpatterns = [
    path('auth/send-code/<str:phone>/', AuthenticationAPI.as_view(), name='send-code'),
    path('auth/send-code-email/', EmailAuthenticationAPI.as_view(), name='send-code-email'),
    path('auth/verify-code/', SignInAPI.as_view(), name='verify-code'),
    path('auth/signin/', SignInAPI.as_view(), name='sign-in'),
    path('auth/forget-password/', ForgetPasswordAPI.as_view(), name='forget-password'),
    path('auth/signup/', AuthenticationAPI.as_view(), name='sign-up'),
    path('auth/sign-out/', sign_out, name='sign-out'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),
    # path('auth/reset-password/', UserAuthentication.as_view(), name='reset-password'),
    path('profile/', profile_api, name='profile'),
]
