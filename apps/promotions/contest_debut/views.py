from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.common.mixins import PublicAPIMixin, PublicJSONRendererMixin
from apps.promotions import PromotionTypes
from apps.promotions.models import Promotion
from apps.promotions.services import get_instagram_auth_url
from apps.promotions.beat_tasks import debut_contest_stats


class PromoTypeMixin:
    _promo_type = PromotionTypes.CONTEST_DEBUT

    @property
    def promotion(self):
        return get_object_or_404(Promotion, promo_type=self._promo_type)


class PromotionContestRenderView(PromoTypeMixin, PublicAPIMixin, APIView):
    queryset = Promotion.objects.all()

    def get(self, request):
        return render(request, 'promotions/contest.html', {'promo_type': self._promo_type.lower()})


class PromotionContestDebutView(PromoTypeMixin, PublicJSONRendererMixin, APIView):
    def get(self, request):
        app_name = '/promotions/'
        promotion = self.promotion
        participation = cache.get(f'{promotion.promo_type}_PARTICIPATION', [])
        if not participation:
            debut_contest_stats()

        show_participate_url = False

        if request.user and request.user.id not in [i.get('user') for i in participation]:
            show_participate_url = True

        return Response(data={
            'info_url': request.build_absolute_uri(app_name + promotion.slug),
            'users': participation,
            'participate_url': get_instagram_auth_url(promotion) if show_participate_url else None
        })
