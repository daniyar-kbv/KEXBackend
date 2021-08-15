from django.urls import path

from .views import (
    RegisterAccountView,
    VerifyAccountView,
    OTPResendView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterAccountView.as_view()),
    path("otp-verify/", VerifyAccountView.as_view(), name="otp_verify_view"),
    path("otp-resend/", OTPResendView.as_view(), name="otp_resend_view"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
