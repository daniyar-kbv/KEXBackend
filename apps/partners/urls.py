from django.urls import path

from .views import BrandImagesView

urlpatterns = [
    path("brands_images/<str:city>/", BrandImagesView.as_view()),
]
