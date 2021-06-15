from django.urls import path

from .views import (
    ApplyView,
    BranchPositionView,
    LeadNomenclatureView,
    UpdateCartView,
)

urlpatterns = [
    path("apply/", ApplyView.as_view()),
    path("<uuid:lead_uuid>/nomenclature/", LeadNomenclatureView.as_view()),
    path("nomenclature/<uuid:position_uuid>/", BranchPositionView.as_view()),
    path("<uuid:lead_uuid>/cart/", UpdateCartView.as_view()),
]
