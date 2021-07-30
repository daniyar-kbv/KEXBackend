from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'priority',
        'slug',
    ]
    list_editable = ['priority']
    ordering = ['-priority']
    # prepopulated_fields = {"slug": ("template", 'type')}
    # exclude = ('slug',)
