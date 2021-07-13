from django.urls import path, include

from .views import PromotionRenderView, PromotionListView

urlpatterns = [
    path("", PromotionListView.as_view()),
    path("contest/contest_debut/", include(('apps.promotions.contest_debut.urls', 'contest_debut'), namespace='contest_debut')),
    path("<str:promotion_slug>/", PromotionRenderView.as_view(), name='promotion_render_view'),
]
