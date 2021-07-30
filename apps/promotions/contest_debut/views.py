import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.mixins import PublicAPIMixin, JSONPublicAPIMixin, JSONRendererMixin
from apps.orders.models import Lead
from apps.promotions import PromotionTypes
from apps.promotions.models import Promotion, Participation
from apps.promotions.services import get_instagram_auth_url, save_user_instagram


class PromoTypeMixin:

    @property
    def promo_type(self):
        return PromotionTypes.CONTEST_DEBUT.lower()


class PromotionContestRenderView(PromoTypeMixin, PublicAPIMixin, APIView):
    queryset = Promotion.objects.all()

    def get(self, request, lead_uuid):
        return render(request, 'promotions/contest.html', {'promo_type': self.promo_type, 'lead_uuid': lead_uuid})


class PromotionContestDebutView(PromoTypeMixin, JSONRendererMixin, APIView):
    queryset = Participation.objects.all()

    def get(self, request, lead_uuid):
        app_name = '/promotions/'
        period = request.GET.get('period')
        promotion = Promotion.objects.filter(
            promo_type__iexact=self.promo_type,
            local_brand__in=[Lead.objects.get(uuid=self.kwargs.get('lead_uuid')).local_brand]
        ).first()
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
            resp_body['takes_part'] = True
            return Response(data=resp_body)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class InstagramAuthView(PromoTypeMixin, JSONPublicAPIMixin, APIView):
    """
    Получение кода авторизации
    """

    def get(self, request):  # noqa
        username = None
        # print('instagram view')
        instagram_code = request.GET.get('code')
        if instagram_code:
            code = instagram_code.split('#')[0]
            save_user_instagram(instagram_code, request.user.pk, self.promo_type, request.path)


            # print("auth code: ", code)
            # data = {
            #     'client_id': settings.INSTAGRAM_CLIENT_ID,
            #     'client_secret': settings.INSTAGRAM_CLIENT_SECRET,
            #     'code': code,
            #     'grant_type': 'authorization_code',
            #     'redirect_uri': request.build_absolute_uri(settings.INSTAGRAM_REDIRECT_URI + promo_type)
            # }
            # response = requests.post(
            #     url='https://api.instagram.com/oauth/access_token/',
            #     data=data,
            # )
            # print("getting access token:")
            # print("response: ", response)
            # print("response content: ", response.content)
            # print(response.json())
            # print(response.text)
            # if response.status_code == 200:
            #     access_token = response.json().get('access_token')
                # print("access_token: ", access_token)
                # if access_token:
                #     resp = requests.get(
                #         f'https://graph.instagram.com/me?fields=id,username&access_token={access_token}'
                #     )
                    # print("getting user profile:")
                    # print("response: ", response)
                    # print("response content: ", response.content)
                    # if resp.status_code == 200:
                        # print(resp.content)
                        # Participation.objects.create(
                        #     user=request.user,
                        #     promotion=Promotion.objects.filter(promo_type=promo_type).first(),
                        #     instagram_username=resp.json().get('username')
                        # )
                        # print(username)
        # response = HttpResponse(status=302)
        # response['Location'] = '/promotions/contest/contest_debut/render/'
        # response['Authorization'] = 'JWT tokentokentoken'
        # return response
        return redirect(reverse('contest_debut:render_view'))
