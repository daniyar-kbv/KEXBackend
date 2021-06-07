from django.db import models
from ckeditor.fields import RichTextField


class MultiLanguageProperties(object):
    # class Meta:
    #     abstract = True

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


class MultiLanguageChar(models.Model, MultiLanguageProperties):
    text_ru = models.CharField("Текст (рус)", max_length=256, null=True)
    text_kk = models.CharField("Текст (каз)", max_length=256, blank=True, null=True)
    text_en = models.CharField("Текст (англ)", max_length=256, blank=True, null=True)


class MultiLanguageText(models.Model, MultiLanguageProperties):
    text_ru = RichTextField("Текст (рус)", null=True)
    text_kk = RichTextField("Текст (каз)", blank=True, null=True)
    text_en = RichTextField("Текст (англ)", blank=True, null=True)


class MultiLanguageFile(models.Model):
    file_ru = models.FileField("Файл (рус)", upload_to='', null=True)
    file_kk = models.FileField("Файл (каз)", upload_to='', blank=True, null=True)
    file_en = models.FileField("Файл (англ)", upload_to='', blank=True, null=True)

    @property
    def ru(self):
        return self.file_ru

    @ru.setter
    def ru(self, value):
        self.file_ru = value
        self.save()

    @property
    def kk(self):
        return self.file_kk

    @kk.setter
    def kk(self, value):
        self.file_kk = value
        self.save()

    @property
    def en(self):
        return self.file_en

    @en.setter
    def en(self, value):
        self.file_en = value
        self.save()

    def __str__(self):
        return self.file_ru.name

