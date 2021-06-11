from django.urls import path

from .views import PromotionView, PromotionListView

urlpatterns = [
    path("", PromotionListView.as_view()),
    path("<str:promotion_slug>/", PromotionView.as_view()),
]
