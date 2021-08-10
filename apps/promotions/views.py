from django.shortcuts import render

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from . import PromotionTypes
from .models import Promotion
from apps.common.mixins import PublicAPIMixin, JSONPublicAPIMixin
from .serializers import PromotionListSerializer
from ..orders.models import Lead


class PromotionRenderView(PublicAPIMixin, APIView):
    queryset = Promotion.objects.all()

    def get(self, request, lead_uuid, promotion_slug):
        print(lead_uuid)
        print(promotion_slug)
        content = None
        promotion = self.queryset.filter(
            slug=promotion_slug,
            local_brand__in=[Lead.objects.get(uuid=self.kwargs.get('lead_uuid')).local_brand]
        )
        if promotion.exists():
            print('exists baby')
            content = promotion.first().template
            content = getattr(content, request.headers.get('Language'))
        else:
            content = "Данная акция недоступна в выбранном городе/бренде"
        return render(request, 'docs/template_page.html', {'content': content})


class PromotionListView(JSONPublicAPIMixin, ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionListSerializer

    def get_queryset(self):
        app_name = self.request.path
        print("app_name: ", app_name)
        queryset = super().get_queryset().filter(
            local_brand__in=[Lead.objects.get(uuid=self.kwargs.get('lead_uuid')).local_brand]
        )

        for promo in queryset:
            if promo.promo_type == PromotionTypes.ARTICLE:
                link = self.request.build_absolute_uri(app_name + promo.slug)
            else:
                link = promo.web_url
            setattr(promo, 'link', link)

        return queryset

