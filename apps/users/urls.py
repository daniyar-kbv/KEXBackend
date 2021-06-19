from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AccountInfoView, AccountUpdateView

urlpatterns = [
    path("account-info/", AccountInfoView.as_view()),
    path("account-update/", AccountUpdateView.as_view()),
    # path()
]
