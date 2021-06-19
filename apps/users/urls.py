from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AccountInfoView,
    AccountUpdateView,
    AddUserAddressView,
    ChangeCurrentAddressView,
)

urlpatterns = [
    path("account-info/", AccountInfoView.as_view()),
    path("account-update/", AccountUpdateView.as_view()),
    path("add-address/", AddUserAddressView.as_view()),
    path("set-current/<int:pk>/", ChangeCurrentAddressView.as_view()),
]
