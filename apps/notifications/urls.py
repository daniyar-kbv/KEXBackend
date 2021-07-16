from django.urls import path, include

from .views import CreateFirebaseTokenView, AddUserToFirebaseTokenView, UpdateFirebaseTokenView

urlpatterns = [
    path("fbtoken-create/", CreateFirebaseTokenView.as_view()),
    path("fbtoken-login/<uuid:lead_uuid>/", AddUserToFirebaseTokenView.as_view()),
    path("fbtoken-update/", UpdateFirebaseTokenView.as_view()),
]
