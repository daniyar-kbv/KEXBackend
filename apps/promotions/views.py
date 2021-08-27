from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import APIException

from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from . import PromotionTypes
from .models import Promotion, Participation
from apps.common.mixins import PublicAPIMixin, PublicJSONRendererMixin, JSONRendererMixin
from .serializers import PromotionListSerializer
from .services import get_instagram_username, save_participation_in_promotion, is_participant
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


class PromotionMixin(PublicJSONRendererMixin, GenericAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionListSerializer

    def get_link(self, promo, app_name):
        if promo.promo_type == PromotionTypes.ARTICLE:
            return self.request.build_absolute_uri(app_name + promo.slug)
        else:
            return promo.web_url


class PromotionListView(PromotionMixin, ListAPIView):
    def get_queryset(self):
        app_name = self.request.path
        print("app_name: ", app_name)
        queryset = super().get_queryset().filter(
            local_brand__in=[Lead.objects.get(uuid=self.kwargs.get('lead_uuid')).local_brand]
        )

        for promo in queryset:
            setattr(promo, 'link', self.get_link(promo, app_name))

        return queryset

    def list(self, request, *args, **kwargs):

        res = super(PromotionListView, self).list(request, *args, **kwargs)
        res.data['results'] = {
            "promotions": res.data['results'],
            "instagram_verification_url": request.build_absolute_uri(settings.INSTAGRAM_VERIFICATION_URI),
            # "instagram_redirect_url": request.build_absolute_uri(settings.INSTAGRAM_REDIRECT_URI),
            # "instagram_parameter": settings.INSTAGRAM_PARAMETER,
        }
        return res


class PromotionDetailView(PromotionMixin, RetrieveAPIView):
    lookup_field = 'pk'

    def get_object(self):
        obj = super().get_object()
        app_name = self.request.path.replace(f'{self.kwargs.get("pk")}/', '')
        setattr(obj, 'link', self.get_link(obj, app_name))
        return obj


class InstagramAuthParticipationView(JSONRendererMixin, APIView):
    """
    Получение кода авторизации
    """

    def post(self, request):  # noqa
        insta_auth_code = request.data.get('code')
        promo_type = request.data.get('promo_type')
        user = request.user
        if not is_participant(user, promo_type):
            print("not participant")
            if insta_auth_code and promo_type and user:
                username = get_instagram_username(insta_auth_code.split('#')[0], promo_type)
                save_participation_in_promotion(user, promo_type, username)
                return Response(status.HTTP_200_OK)
            else:
                raise APIException("Нужные поля не указаны")
        return Response(status.HTTP_200_OK)


class InstagramRedirectURLView(PublicAPIMixin, APIView):
    def get(self, request):
        return Response(status.HTTP_200_OK)
