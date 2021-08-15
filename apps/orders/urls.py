from django.urls import path

from .views import (
    ApplyView,
    AuthorizedApplyView,
    AuthorizedApplyWithAddressView,
    LeadNomenclatureView,
    LeadNomenclatureRetrieveView,
    LeadAdditionalNomenclatureView,
    UpdateCartView,
    LeadShowView,
    RateStarListView,
    CreateRateOrderView,
    CreateOrderView,
    OrdersListView,
    OrderStatusView,
    CouponDetailView,
)

urlpatterns = [
    path("", OrdersListView.as_view()),
    path("<uuid:lead_uuid>/show/", LeadShowView.as_view()),

    path("apply/", ApplyView.as_view()),
    path("authorized-apply/", AuthorizedApplyView.as_view()),
    path("authorized-apply-with-address/", AuthorizedApplyWithAddressView.as_view()),

    path("<uuid:lead_uuid>/nomenclature/", LeadNomenclatureView.as_view(), name="order-nomenclature"),
    path("<uuid:lead_uuid>/additional-nomenclature/", LeadAdditionalNomenclatureView.as_view()),
    path("<uuid:lead_uuid>/nomenclature/<uuid:position_uuid>/", LeadNomenclatureRetrieveView.as_view()),

    path("<uuid:lead_uuid>/cart/", UpdateCartView.as_view()),

    path("create/", CreateOrderView.as_view()),
    path("<uuid:lead_uuid>/status/", OrderStatusView.as_view()),

    path("coupons/<str:promocode>/", CouponDetailView.as_view()),
    path('ratestars/', RateStarListView.as_view()),
    path('rates/', CreateRateOrderView.as_view()),
]
