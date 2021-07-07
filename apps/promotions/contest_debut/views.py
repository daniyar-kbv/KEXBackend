from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.services import get_instagram_auth_url
from apps.common.mixins import PublicAPIMixin, JSONPublicAPIMixin
from apps.promotions import PromotionTypes
from apps.promotions.models import Promotion, Participation


class PromoTypeMixin:

    @property
    def promo_type(self):
        return PromotionTypes.CONTEST_DEBUT.lower()


class PromotionContestRenderView(PromoTypeMixin, PublicAPIMixin, APIView):
    queryset = Promotion.objects.all()

    def get(self, request):
        return render(request, 'promotions/contest.html', {'promo_type': self.promo_type})


class PromotionContestDebutView(PromoTypeMixin, JSONPublicAPIMixin, APIView):
    queryset = Participation.objects.all()

    def get(self, request):
        app_name = '/promotions/'
        period = request.GET.get('period')
        promotion = Promotion.objects.filter(promo_type__iexact=self.promo_type).first()
        if promotion:
            if not period:
                objs = self.queryset.filter(promotion=promotion)
            else:
                objs = self.queryset.filter(promotion=promotion)
            print(objs)
            resp_body = {
                "users": [],
                "participate_url": get_instagram_auth_url(request, self.promo_type),
                "info_url": request.build_absolute_uri(app_name + promotion.slug)
            }
            if objs.exists():
                for obj in objs:
                    resp_body['users'].append({
                        'name': obj.user.name,
                        'instagram': obj.instagram_username,
                        'sum': 0.0
                    })
            return Response(data=resp_body)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
