from django.db import models


class MultiLanguageChar(models.Model):
    text_ru = models.CharField("Текст (рус)", max_length=256, null=True)
    text_kk = models.CharField("Текст (каз)", max_length=256, blank=True, null=True)
    text_en = models.CharField("Текст (англ)", max_length=256, blank=True, null=True)

    def text(self, lang: str = 'ru', value: str = None) -> str:
        if value is None:
            return getattr(self, f"text_{lang}")
        else:
            setattr(self, f"text_{lang}", value)
            self.save()

    def set_all_langs(self, lang_dict: dict) -> None:
        for lang, value in lang_dict.items():
            setattr(self, f"text_{lang}", value)
        self.save()

    @property
    def ru(self):
        return self.text_ru

    @ru.setter
    def ru(self, value):
        self.text_ru = value
        self.save()

    @property
    def kk(self):
        return self.text_kk

    @kk.setter
    def kk(self, value):
        self.text_kk = value
        self.save()

    @property
    def en(self):
        return self.text_en

    @en.setter
    def en(self, value):
        self.text_en = value
        self.save()

    def __str__(self):
        return self.text_ru
