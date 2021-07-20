from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AccountInfoView,
    AccountUpdateView,
    UserAddressListView,
    UpdateUserAddressView,
)

urlpatterns = [
    path("account-info/", AccountInfoView.as_view()),
    path("account-update/", AccountUpdateView.as_view()),
    path("addresses/", UserAddressListView.as_view()),
    path("addresses/<int:pk>/", UpdateUserAddressView.as_view()),
]
