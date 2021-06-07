from django.contrib import admin

# Register your models here.
from django.contrib.gis import forms

from .models import MultiLanguageChar, MultiLanguageText, MultiLanguageFile

admin.site.register(MultiLanguageChar)
admin.site.register(MultiLanguageText)
admin.site.register(MultiLanguageFile)


class MultiLanguageTextAdmin(admin.ModelAdmin):
    fields = [
        'text_ru',
        'text_kk',
        'text_en'
    ]
