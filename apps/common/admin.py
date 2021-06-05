from django import forms
from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

from apps.common.models import MultiLanguageChar, MultiLanguageText
from apps.pipeline.models import ServiceHistory


class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}  # Hide model in admin list


class ChangeOnlyMixin:
    def has_add_permission(self, request, obj=None):
        return False


class ReadOnlyMixin(ChangeOnlyMixin):
    def has_change_permission(self, request, obj=None):
        return False


class ReadChangeOnlyMixin():
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


class ReadChangeOnlyTabularInline(ReadChangeOnlyMixin, admin.TabularInline):
    ...


class ReadChangeOnlyStackedInline(ReadChangeOnlyTabularInline, admin.StackedInline):
    ...


class HistoryInline(ReadOnlyMixin, GenericTabularInline):
    model = ServiceHistory
    fields = ["service", "service_pretty", "runtime", "created_at", "show"]
    readonly_fields = ["show", "created_at"]
    classes = ("collapse",)

    def show(self, obj):
        url = reverse("admin:pipeline_servicehistory_change", args=(obj.pk,))  # noqa
        return mark_safe(f"<a href='{url}'>Посмотреть</a>")

    show.short_description = _("Лог сервиса")


admin.site.register(MultiLanguageChar)
admin.site.register(MultiLanguageText)


class AbstractNameModelForm(forms.ModelForm):
    name_ru = forms.CharField(label="Название (рус)", required=True, max_length=256)
    name_kk = forms.CharField(label="Название (каз)", required=False, max_length=256)
    name_en = forms.CharField(label="Название (англ)", required=False, max_length=256)

    class Meta:
        fields = ('name_ru', 'name_kk', 'name_en',)

    def __init__(self, *args, **kwargs):
        super(AbstractNameModelForm, self).__init__(*args, **kwargs)
        self.fields['name_ru'] = forms.CharField(
            label="Название (рус)", required=True, max_length=256
        )
        self.fields['name_kk'] = forms.CharField(
            label="Название (каз)", required=False, max_length=256
        )
        self.fields['name_en'] = forms.CharField(
            label="Название (англ)", required=False, max_length=256
        )
        if self.instance.name:
            name_ru = self.instance.name.ru
            name_kk = self.instance.name.kk
            name_en = self.instance.name.en
            self.initial['name_ru'] = name_ru
            self.initial['name_kk'] = name_kk
            self.initial['name_en'] = name_en

    def save(self, commit=True):
        obj = super(AbstractNameModelForm, self).save(commit=False)
        lang_dict = {
            'ru': self.cleaned_data.get('name_ru', None),
            'kk': self.cleaned_data.get('name_kk', None),
            'en': self.cleaned_data.get('name_en', None)
        }
        if obj.name:
            obj.name.set_all_langs(lang_dict)
        else:
            mlchar, created = MultiLanguageChar.objects.get_or_create(
                text_ru=lang_dict['ru'], text_kk=lang_dict['kk'], text_en=lang_dict['en']
            )
            if created:
                obj.name = mlchar
        if commit:
            obj.save()
        return obj
