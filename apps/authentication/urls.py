from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterAccountView, VerifyAccountView

urlpatterns = [
    path("register/", RegisterAccountView.as_view()),
    path("verify/", VerifyAccountView.as_view()),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
