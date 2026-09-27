from django.urls import path
from .views import (
    RegisterView, VerifyOTPView, LoginView, ResendOTPView,
    ForgotPasswordView, ResetPasswordView, LogoutView, MeView,
)

urlpatterns = [
    path('register/',        RegisterView.as_view()),
    path('verify-otp/',      VerifyOTPView.as_view()),
    path('login/',           LoginView.as_view()),
    path('resend-otp/',      ResendOTPView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/',  ResetPasswordView.as_view()),
    path('logout/',          LogoutView.as_view()),
    path('me/',              MeView.as_view()),
]
