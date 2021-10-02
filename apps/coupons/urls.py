from django.urls import path

from .views import CouponDetailView

urlpatterns = [
    path("coupons/<str:promocode>/", CouponDetailView.as_view()),
]
