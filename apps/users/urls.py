from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AccountInfoView,
    AccountUpdateView,
    UserAddressViewSet,
)

router = DefaultRouter()
router.register("addresses", UserAddressViewSet)

urlpatterns = [
    path("account-info/", AccountInfoView.as_view()),
    path("account-update/", AccountUpdateView.as_view()),
    path("", include(router.urls)),
]
