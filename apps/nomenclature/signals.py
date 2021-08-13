from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Position, BranchCategory


@receiver(post_save, sender=Position)
def update_local_position(sender, instance, created, **kwargs):
    if created:
        return

    if instance.local_category is not None:
        for branch_position in instance.branch_positions.all():
            branch_category, _ = BranchCategory.objects.get_or_create(
                local_category_id=instance.local_category_id,
                branch_id=branch_position.branch_id,
            )

            branch_position.name = instance.name
            branch_position.description = instance.description
            branch_position.branch_category = branch_category
            branch_position.save(update_fields=[
                "name",
                "description",
                "branch_category",
            ])
