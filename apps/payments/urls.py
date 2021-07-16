from django.urls import path

from .views import (
    CreatePaymentView,
    DebitCardsListView,
    CreateCardPaymentView,
    Confirm3DSPaymentView,
)

urlpatterns = [
    path("my-cards/", DebitCardsListView.as_view()),
    path("create-payment/", CreatePaymentView.as_view()),
    path("confirm-payment/", Confirm3DSPaymentView.as_view()),
    path("create-card-payment/<uuid:card_uuid>", CreateCardPaymentView.as_view()),
]
