from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_type', 'uploaded_by', 'uploaded_at', 'is_active')
    list_filter = ('doc_type', 'uploaded_at', 'is_active')
    search_fields = ('title', 'authors', 'keywords', 'description')
    readonly_fields = ('uploaded_at', 'updated_at')
