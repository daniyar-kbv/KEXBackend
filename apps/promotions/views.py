from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from .models import Promotion


class PromotionView(APIView):
    queryset = Promotion.objects.all()

    def get(self, request, promotion_slug):
        content = None
        promotion = self.queryset.filter(slug=promotion_slug)
        if promotion.exists():
            print('exists baby')
            content = promotion.first().template
        return render('promotions/promotion_page.html', request, {'content': content})
