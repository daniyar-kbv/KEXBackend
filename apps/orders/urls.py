from django.urls import path

from .views import (
    ApplyView,
    BranchPositionView,
    LeadNomenclatureView,
    UpdateCartView,
    IncrementCartPositionView,
    DecrementCartPositionView,
)

urlpatterns = [
    path("apply/", ApplyView.as_view()),
    path("<uuid:lead_uuid>/nomenclature/", LeadNomenclatureView.as_view()),
    path("nomenclature/<uuid:position_uuid>/", BranchPositionView.as_view()),

    # path("<uuid:lead_uuid>/cart/"),
    # path("<uuid:lead_uuid>/cart/add-position/", ),
    # path("<uuid:lead_uuid>/cart/remove-positions/", ),
    path("<uuid:lead_uuid>/cart/", UpdateCartView.as_view()),

    # path("<uuid:lead_uuid>/update-cart/", UpdateCartView.as_view()),
    # path("<uuid:lead_uuid>/cart/increment-count/<uuid:position_uuid>", IncrementCartPositionView.as_view()),
    # path("<uuid:lead_uuid>/cart/decrement-count/<uuid:position_uuid>", DecrementCartPositionView.as_view()),
]
