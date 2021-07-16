from django.urls import path

from .views import CreatePaymentView, DebitCardsListView

urlpatterns = [
    path("create-payment/", CreatePaymentView.as_view()),
    path("my-cards/", DebitCardsListView.as_view()),
]
