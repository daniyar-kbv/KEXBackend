from django.urls import path

from .views import (
    ApplyView,
    BranchPositionView,
    LeadNomenclatureView,
    CartRetrieveUpdateView,
)

urlpatterns = [
    path("apply/", ApplyView.as_view()),
    path("<uuid:lead_uuid>/nomenclature/", LeadNomenclatureView.as_view(), name="order-nomenclature"),
    path(
        "<uuid:lead_uuid>/nomenclature/<uuid:position_uuid>/",
        BranchPositionView.as_view(),
        name="order-nomenclature-position"
    ),
    path("<uuid:lead_uuid>/cart/", CartRetrieveUpdateView.as_view()),
]
