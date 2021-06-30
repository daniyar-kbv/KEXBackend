from django.shortcuts import render
from django.urls import resolve
from rest_framework import status

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from .models import Promotion, Participation
from apps.common.mixins import PublicAPIMixin, JSONPublicAPIMixin
from .serializers import PromotionListSerializer
from ..authentication.services import get_instagram_auth_url


class PromotionRenderView(PublicAPIMixin, APIView):
    queryset = Promotion.objects.all()

    def get(self, request, promotion_slug):
        content = None
        promotion = self.queryset.filter(slug=promotion_slug)
        if promotion.exists():
            print('exists baby')
            content = promotion.first().template
            content = getattr(content, request.headers.get('Language'))
        return render(request, 'docs/template_page.html', {'content': content})


class PromotionContestRenderView(PublicAPIMixin, APIView):
    queryset = Promotion.objects.all()

    def get(self, request, promo_type):
        return render(request, 'promotions/contest.html', {'promo_type': promo_type})


class PromotionContestView(JSONPublicAPIMixin, APIView):
    queryset = Participation.objects.all()

    def get(self, request, promo_type):
        app_name = '/promotions/'
        promo_type = promo_type.upper()
        period = request.GET.get('period')
        promotion = Promotion.objects.filter(promo_type=promo_type).first()
        if promotion:
            if not period:
                objs = self.queryset.filter(promotion=promotion)
            else:
                objs = self.queryset.filter(promotion=promotion)
            print(objs)
            resp_body = {
                "users": [],
                "participate_url": get_instagram_auth_url(request),
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


class PromotionListView(JSONPublicAPIMixin, ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionListSerializer

    def get_queryset(self):
        app_name = self.request.path
        print("app_name: ", app_name)
        queryset = super().get_queryset()

        for promo in queryset:
            link = self.request.build_absolute_uri(app_name + promo.slug)
            setattr(promo, 'link', link)

        return queryset

