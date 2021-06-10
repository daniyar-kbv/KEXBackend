from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AccountInfoView

urlpatterns = [
    path("account-info/", AccountInfoView.as_view()),
]
