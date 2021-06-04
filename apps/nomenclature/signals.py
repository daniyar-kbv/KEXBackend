# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import Category, LocalCategory, BranchCategory
#
#
# @receiver(post_save, sender=Category)
# def update_category(sender, instance, **kwargs):
#     print(";lolkek")
#     if instance.brand is not None:
#         for local_brand in instance.brand.local_brands.all():
#             local_category, _ = LocalCategory.objects.update_or_create(
#                 category=instance,
#                 local_brand=local_brand,
#                 defaults={
#                     "name": instance.name,
#                     "is_active": instance.is_active,
#                 }
#             )
