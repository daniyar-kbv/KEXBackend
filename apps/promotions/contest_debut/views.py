from datetime import timedelta
from operator import itemgetter

import requests
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.encryption import decrypt_and_get_user
from apps.common.mixins import PublicAPIMixin, PublicJSONRendererMixin, JSONRendererMixin
from apps.orders.models import Lead
from apps.promotions import PromotionTypes
from apps.promotions.models import Promotion, Participation
from apps.promotions.services import get_instagram_auth_url, get_instagram_username


class PromoTypeMixin:

    @property
    def promo_type(self):
        return PromotionTypes.CONTEST_DEBUT.lower()

    @property
    def promotion(self):
        return Promotion.objects.get(promo_type=self.promo_type)


class PromotionContestRenderView(PromoTypeMixin, PublicAPIMixin, APIView):
    queryset = Promotion.objects.all()

    def get(self, request, lead_uuid):
        return render(request, 'promotions/contest.html', {'promo_type': self.promo_type, 'lead_uuid': lead_uuid})


class PromotionContestDebutView(PromoTypeMixin, PublicJSONRendererMixin, APIView):
    queryset = Participation.objects.all()

    def get(self, request, lead_uuid):
        app_name = '/promotions/'
        period = request.GET.get('period')
        promotion = Promotion.objects.filter(
            promo_type__iexact=self.promo_type,
            local_brand__in=[Lead.objects.get(uuid=self.kwargs.get('lead_uuid')).local_brand]
        ).first()
        if promotion:
            # if not period:
            #     objs = self.queryset.filter(promotion=promotion).select_related('payments')
            # else:
            objs = self.queryset.filter(promotion=promotion).select_related('user')
            # print(objs)
            resp_body = {
                "info_url": request.build_absolute_uri(app_name + promotion.slug),
                "users": [],
                "user_info": None,
            }
            if period:
                contest_date = timezone.now() - timedelta(days=7)
            else:
                contest_date = promotion.start_date

            user_id = request.user.id if request.user else None
            if objs.exists():
                for obj in objs:
                    user_payments = obj.user.payments.filter(created_at__gte=contest_date)
                    user = {
                        'id': obj.user.id,
                        'name': obj.user.name,
                        'instagram': obj.instagram_username,
                        'sum': int(user_payments.aggregate(Sum('price'))['price__sum']) if user_payments else 0
                    }
                    resp_body['users'].append(user)
                    if obj.user.id == user_id:
                        resp_body['user_info'] = user
                resp_body['users'] = sorted(resp_body['users'], key=itemgetter('sum'), reverse=True)
            if user_id and not resp_body['user_info']:
                resp_body['user_info'] = {
                    'participate_url': get_instagram_auth_url(promotion.web_url)
                }
            return Response(data=resp_body)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
