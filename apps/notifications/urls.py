from django.urls import path, include

from .views import FirebaseTokenSaveView, FirebaseTokenUpdateView, PromotionQuerysetView, OrderQuerysetView

urlpatterns = [
    path("fbtoken/save/", FirebaseTokenSaveView.as_view()),
    path("fbtoken/update/", FirebaseTokenUpdateView.as_view()),
    path("promotion-queryset/", PromotionQuerysetView.as_view()),
    path("order-queryset/", OrderQuerysetView.as_view()),
]
