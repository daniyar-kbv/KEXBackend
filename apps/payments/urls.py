from rest_framework import routers
from django.urls import path, include


from .views import (
    CreatePaymentView,
    DebitCardsListViewSet,
    CreateCardPaymentView,
    Confirm3DSPaymentView,
    TestPaymentRenderView,
    CreateWidgetPaymentView,
)

from .cloud_payments_apis import (
    CloudPaymentsCheckView,
    SuccessView,
    FailureView,
)

router = routers.SimpleRouter()
router.register(r'my-cards', DebitCardsListViewSet)

urlpatterns = [
    path("create-payment/", CreatePaymentView.as_view()),
    path("create-card-payment/", CreateCardPaymentView.as_view()),
    path("confirm-payment/<uuid:payment_uuid>/", Confirm3DSPaymentView.as_view()),
    path("create-widget-payment/", CreateWidgetPaymentView.as_view()),
    path("", include(router.urls)),
    path("test-template/", TestPaymentRenderView.as_view()),

    path('cloud-payments/check', CloudPaymentsCheckView.as_view()),
    path('cloud-payments/success', SuccessView.as_view()),
    path('cloud-payments/failure', FailureView.as_view()),
]
