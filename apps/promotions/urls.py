from django.urls import path, include

from .views import PromotionRenderView, PromotionListView, PromotionDetailView

urlpatterns = [
    path("<uuid:lead_uuid>/", PromotionListView.as_view()),
    path('<uuid:lead_uuid>/<int:pk>/', PromotionDetailView.as_view()),
    path("<uuid:lead_uuid>/contest/contest_debut/", include(('apps.promotions.contest_debut.urls', 'contest_debut'), namespace='contest_debut')),
    path("<uuid:lead_uuid>/<str:promotion_slug>/", PromotionRenderView.as_view(), name='promotion_render_view'),
]
