from django.urls import path, include

from .views import CreateFirebaseTokenView, AddUserToFirebaseTokenView, UpdateFirebaseTokenView, PromotionQuerysetView, \
    OrderQuerysetView

urlpatterns = [
    path("fbtoken-create/", CreateFirebaseTokenView.as_view()),
    path("fbtoken-login/<uuid:lead_uuid>/", AddUserToFirebaseTokenView.as_view()),
    path("fbtoken-update/", UpdateFirebaseTokenView.as_view()),
    path("promotion-queryset/", PromotionQuerysetView.as_view()),
    path("order-queryset/", OrderQuerysetView.as_view()),
]
