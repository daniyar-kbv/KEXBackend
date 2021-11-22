from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q, F
from django.core.cache import cache

from config import celery_app

from . import PromotionTypes
from .models import Promotion


@celery_app.task(name='promotions.debut_contest_stats')
def debut_contest_stats() -> None:
    promotion = get_object_or_404(Promotion, promo_type=PromotionTypes.CONTEST_DEBUT)

    participation = list(promotion.participations.values('user')\
        .order_by('user')\
        .annotate(total_price=Sum('user__payments__price', filter=(
            Q(user__payments__status='COMPLETED') &
            Q(user__payments__created_at__date__gte=promotion.start_date) &
            Q(user__payments__created_at__date__lte=promotion.end_date)
        )))\
        .annotate(instagram=F('instagram_username'))\
        .annotate(name=F('user__name'))\
        .filter(total_price__isnull=False)\
        .order_by('-total_price')
    )

    cache.set(f'{promotion.promo_type}_PARTICIPATION', participation)
