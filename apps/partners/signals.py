from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Brand
from apps.nomenclature.models import Category, LocalCategory, BranchCategory


@receiver(post_save, sender=Brand)
def update_category(sender, instance, **kwargs):
    print('lol kek')
    for category in instance.categories.all():
        for local_brand in instance.local_brands.all():
            local_category, _ = LocalCategory.objects.update_or_create(
                category=category,
                local_brand=local_brand,
                defaults={
                    "name": category.name,
                    "is_active": category.is_active,
                }
            )
