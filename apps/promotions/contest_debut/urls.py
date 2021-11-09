from django.urls import path

from .views import PromotionContestDebutView, PromotionContestRenderView

urlpatterns = [
    path("", PromotionContestDebutView.as_view(), name='api_view'),
    path("render/", PromotionContestRenderView.as_view(), name='render_view'),
]
