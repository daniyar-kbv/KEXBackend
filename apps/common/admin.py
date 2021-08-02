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


class AbstractTitleModelForm(forms.ModelForm):
    title_ru = forms.CharField(label="Заголовок (рус)", required=True, max_length=256)
    title_kk = forms.CharField(label="Заголовок (каз)", required=False, max_length=256)
    title_en = forms.CharField(label="Заголовок (англ)", required=False, max_length=256)

    class Meta:
        fields = ('title_ru', 'title_kk', 'title_en',)

    def __init__(self, *args, **kwargs):
        super(AbstractTitleModelForm, self).__init__(*args, **kwargs)
        self.fields['title_ru'] = forms.CharField(
            label="Заголовок (рус)", required=True, max_length=256
        )
        self.fields['title_kk'] = forms.CharField(
            label="Заголовок (каз)", required=False, max_length=256
        )
        self.fields['title_en'] = forms.CharField(
            label="Заголовок (англ)", required=False, max_length=256
        )
        if self.instance.title:
            title_ru = self.instance.title.ru
            title_kk = self.instance.title.kk
            title_en = self.instance.title.en
            self.initial['title_ru'] = title_ru
            self.initial['title_kk'] = title_kk
            self.initial['title_en'] = title_en

    def save(self, commit=True):
        obj = super(AbstractTitleModelForm, self).save(commit=False)
        lang_dict = {
            'ru': self.cleaned_data.get('title_ru', None),
            'kk': self.cleaned_data.get('title_kk', None),
            'en': self.cleaned_data.get('title_en', None)
        }
        if obj.title:
            obj.title.set_all_langs(lang_dict)
        else:
            mlchar, created = MultiLanguageChar.objects.get_or_create(
                text_ru=lang_dict['ru'], text_kk=lang_dict['kk'], text_en=lang_dict['en']
            )
            if created:
                obj.title = mlchar
        if commit:
            obj.save()
        return obj


class AbstractDescriptionModelForm(forms.ModelForm):
    description_ru = forms.CharField(label="Название (рус)", required=True, max_length=256)
    description_kk = forms.CharField(label="Название (каз)", required=False, max_length=256)
    description_en = forms.CharField(label="Название (англ)", required=False, max_length=256)

    class Meta:
        fields = ('description_ru', 'description_kk', 'description_en',)

    def __init__(self, *args, **kwargs):
        super(AbstractDescriptionModelForm, self).__init__(*args, **kwargs)
        self.fields['description_ru'] = forms.CharField(
            label="Название (рус)", required=True, max_length=256
        )
        self.fields['description_kk'] = forms.CharField(
            label="Название (каз)", required=False, max_length=256
        )
        self.fields['description_en'] = forms.CharField(
            label="Название (англ)", required=False, max_length=256
        )
        if self.instance.description:
            description_ru = self.instance.description.ru
            description_kk = self.instance.description.kk
            description_en = self.instance.description.en
            self.initial['description_ru'] = description_ru
            self.initial['description_kk'] = description_kk
            self.initial['description_en'] = description_en

    def save(self, commit=True):
        obj = super(AbstractDescriptionModelForm, self).save(commit=False)
        lang_dict = {
            'ru': self.cleaned_data.get('description_ru', None),
            'kk': self.cleaned_data.get('description_kk', None),
            'en': self.cleaned_data.get('description_en', None)
        }
        if obj.description:
            obj.description.set_all_langs(lang_dict)
        else:
            mlchar, created = MultiLanguageChar.objects.get_or_create(
                text_ru=lang_dict['ru'], text_kk=lang_dict['kk'], text_en=lang_dict['en']
            )
            if created:
                obj.description = mlchar
        if commit:
            obj.save()
        return obj
