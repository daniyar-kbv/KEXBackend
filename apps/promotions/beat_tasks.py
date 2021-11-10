from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q
from django.core.cache import cache

from config import celery_app

from . import PromotionTypes
from .models import Promotion


@celery_app.task(name='promotions.debut_contest_stats')
def debut_contest_stats() -> None:
    promotion = get_object_or_404(Promotion, promo_type=PromotionTypes.CONTEST_DEBUT)

    participation = promotion.participations\
        .values(
            'user', 'instagram_username'
        ).order_by('user').annotate(
            total_price=Sum('user__payments__price', filter=(
                Q(user__payments__status='COMPLETED')
            ))
        ).filter(total_price__isnull=False)\
        .order_by('-total_price')

    cache.set(f'{promotion.promo_type}_PARTICIPATION', participation)
