from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import TokenObtainPairView

urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
