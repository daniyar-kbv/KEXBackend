from django.contrib import admin

from .models import MultiLanguageChar, MultiLanguageText, MultiLanguageFile, MultiLanguageTextEditor

admin.site.register(MultiLanguageChar)
admin.site.register(MultiLanguageText)
admin.site.register(MultiLanguageFile)
admin.site.register(MultiLanguageTextEditor)


class MultiLanguageTextAdmin(admin.ModelAdmin):
    fields = [
        'text_ru',
        'text_kk',
        'text_en'
    ]
