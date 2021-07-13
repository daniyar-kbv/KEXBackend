from django.urls import path

from .views import PromotionContestDebutView, PromotionContestRenderView, InstagramAuthView

urlpatterns = [
    path("", PromotionContestDebutView.as_view(), name='api_view'),
    path("render/", PromotionContestRenderView.as_view(), name='render_view'),
    path("instagram/", InstagramAuthView.as_view(), name="instagram_auth_view"),

]
