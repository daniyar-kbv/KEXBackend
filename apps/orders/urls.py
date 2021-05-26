from django.urls import path

from .views import (
    ApplyView,
    LeadNomenclatureView,
    UpdateCartView,
    IncrementCartPositionView,
    DecrementCartPositionView,
)

urlpatterns = [
    path("apply/", ApplyView.as_view()),
    path("<uuid:lead_uuid>/nomenclature/", LeadNomenclatureView.as_view()),
    path("<uuid:lead_uuid>/update-cart/", UpdateCartView.as_view()),
    path("<uuid:lead_uuid>/increment/<uuid:position_uuid>", IncrementCartPositionView.as_view()),
    path("<uuid:lead_uuid>/decrement/<uuid:position_uuid>", DecrementCartPositionView.as_view()),
]
