from django.contrib import admin

from .models import Document
from apps.common.admin import AbstractNameModelForm, AbstractTemplateModelForm


class DocumentForm(AbstractNameModelForm, AbstractTemplateModelForm):
    class Meta:
        model = Document
        exclude = ('name',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'priority',
        'slug',
    ]
    list_editable = ['priority']
    ordering = ['-priority']
    form = DocumentForm
    # prepopulated_fields = {"slug": ("template", 'type')}
    # exclude = ('slug',)
