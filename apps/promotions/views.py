from django.shortcuts import render

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from .models import Promotion
from apps.common.mixins import PublicAPIMixin, JSONPublicAPIMixin
from .serializers import PromotionListSerializer


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

