# scripts to fill db

def run_background_tasks():
    from apps.pipeline.iiko.celery_tasks.beat_tasks import update_brand_branches, update_brand_nomenclatures

    update_brand_branches()
    update_brand_nomenclatures()


def add_random_categories():
    from apps.partners.models import Brand
    from apps.translations.models import MultiLanguageChar

    category_names = [
        MultiLanguageChar.objects.create(
            text_ru="Burgers",
            text_kk="Burgers",
            text_en="Burgers",
        ),
        MultiLanguageChar.objects.create(
            text_ru="HotDogs",
            text_kk="HotDogs",
            text_en="HotDogs",
        ),
        MultiLanguageChar.objects.create(
            text_ru="Juices",
            text_kk="Juices",
            text_en="Juices",
        ),
        MultiLanguageChar.objects.create(
            text_ru="StillWater",
            text_kk="StillWater",
            text_en="StillWater",
        ),
        MultiLanguageChar.objects.create(
            text_ru="Pervoe",
            text_kk="Pervoe",
            text_en="Pervoe",
        ),
        MultiLanguageChar.objects.create(
            text_ru="Vtoroe",
            text_kk="Vtoroe",
            text_en="Vtoroe",
        ),
        MultiLanguageChar.objects.create(
            text_ru="Syuwnyak",
            text_kk="Syuwnyak",
            text_en="Syuwnyak",
        ),
    ]

    for brand in Brand.objects.all():
        for category_name in category_names:
            Category.objects.create(
                name=category_name,
                brand=brand
            )


def set_position_names():
    import random
    import string
    from apps.partners.models import LocalBrand
    from apps.translations.models import MultiLanguageChar, MultiLanguageText

    for local_brand in LocalBrand.objects.all():

        for local_position in local_brand.local_positions.all():
            iiko_name = local_position.branch_positions.filter(
                iiko_name__isnull=False
            ).first()
            local_position_name = iiko_name.iiko_name if iiko_name else "".join([random.choice(string.ascii_letters) for i in range(10)])

            iiko_description = local_position.branch_positions.filter(
                iiko_description__isnull=False
            ).first()
            local_position_description = iiko_description.iiko_description if iiko_description else "".join(
                [random.choice(string.ascii_letters) for i in range(10)])

            local_position.name = MultiLanguageChar.objects.create(
                text_ru=local_position_name,
                text_kk=local_position_name,
                text_en=local_position_name,
            )
            local_position.description = MultiLanguageText.objects.create(
                text_ru=local_position_description,
                text_kk=local_position_description,
                text_en=local_position_description,
            )
            local_position.local_category = random.choice(local_brand.local_categories.all())
            local_position.save()


def run_fill_processes():
    run_background_tasks()
    add_random_categories()
    set_position_names()
