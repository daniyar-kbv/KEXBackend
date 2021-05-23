from django.urls import path

from .views import ApplyView, LeadNomenclatureView

urlpatterns = [
    path("apply/", ApplyView.as_view()),
    path("<uuid:uuid>/nomenclature", LeadNomenclatureView.as_view()),
]
