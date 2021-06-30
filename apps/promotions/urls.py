from django.urls import path

from .views import PromotionRenderView, PromotionListView, PromotionContestView, PromotionContestRenderView

urlpatterns = [
    path("", PromotionListView.as_view()),
    path("contest/render/<str:promo_type>/", PromotionContestRenderView.as_view(), name='promotion_contest_render_view'),
    path("contest/<str:promo_type>/", PromotionContestView.as_view(), name='promotion_contest_view'),
    path("<str:promotion_slug>/", PromotionRenderView.as_view(), name='promotion_render_view'),
]
