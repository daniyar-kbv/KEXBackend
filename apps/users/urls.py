from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, Test

router = DefaultRouter()
# router.register("", UserViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path("test/", Test.as_view()),
]
