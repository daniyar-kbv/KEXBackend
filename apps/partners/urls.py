from django.urls import path

from .views import BrandListView

urlpatterns = [
    path("brands_of_city/<str:city_id>/", BrandListView.as_view()),
]
