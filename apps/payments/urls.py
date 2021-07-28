from django.urls import path

from .views import (
    CreatePaymentView,
    DebitCardsListView,
    CreateCardPaymentView,
    Confirm3DSPaymentView,
    TestPaymentRenderView
)

urlpatterns = [
    path("my-cards/", DebitCardsListView.as_view()),
    path("create-payment/", CreatePaymentView.as_view()),
    path("create-card-payment/", CreateCardPaymentView.as_view()),
    path("confirm-payment/<uuid:payment_uuid>/", Confirm3DSPaymentView.as_view()),
    path("test-template/", TestPaymentRenderView.as_view()),
]
