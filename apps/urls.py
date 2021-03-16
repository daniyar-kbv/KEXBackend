from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
]