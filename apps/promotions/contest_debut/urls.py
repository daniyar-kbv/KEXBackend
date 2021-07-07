from django.urls import path

from .views import PromotionContestDebutView, PromotionContestRenderView

urlpatterns = [
    path("", PromotionContestDebutView.as_view(), name='promotion_contest_debut_view'),
    path("render/", PromotionContestRenderView.as_view(), name='promotion_contest_debut_render_view'),
]
