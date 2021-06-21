from apps.translations.models import MultiLanguageText, MultiLanguageChar


def create_multi_language_model_instance(default_text: str, model):
    return model.objects.create(
        text_ru=default_text,
        text_kk=default_text,
        text_en=default_text,
    )


def create_multi_language_text(default_text: str):
    return create_multi_language_model_instance(
        default_text=default_text,
        model=MultiLanguageText,
    )


def create_multi_language_char(default_text: str):
    return create_multi_language_model_instance(
        default_text=default_text,
        model=MultiLanguageChar,
    )
