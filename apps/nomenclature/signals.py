from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Category, LocalCategory, BranchCategory


@receiver(post_save, sender=Category)
def update_category(sender, instance, **kwargs):
    print("update_category", instance)
    if instance.brand is None:
        return

    for local_brand in instance.brand.local_brands.all():
        local_category, _ = LocalCategory.objects.update_or_create(
            category=instance,
            local_brand=local_brand,
            defaults={
                "name": instance.name,
                "is_active": instance.is_active,
            }
        )


@receiver(post_save, sender=LocalCategory)
def update_local_category(sender, instance, **kwargs):
    print("local_category signal is called")
    for branch in instance.local_brand.branches.all():
        print("brand:", branch)
        branch_category, _ = BranchCategory.objects.update_or_create(
            local_category=instance,
            branch=branch,
            defaults={
                "name": instance.name,
                "is_active": instance.is_active,
            }
        )
