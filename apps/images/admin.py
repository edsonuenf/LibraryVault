from django.contrib import admin
from .models_organization import Organization, UserProfile
from .models import Image, Document, Video, Audio

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization')
    search_fields = ('user__username', 'organization__name')
    list_filter = ('organization',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def thumbnail_tag(self, obj):
        import os
        from django.utils.html import format_html
        from django.conf import settings
        # Base para nome do arquivo
        if obj.file and obj.file.name:
            base_name = os.path.splitext(os.path.basename(obj.file.name))[0]
        elif hasattr(obj, 'original_filename') and obj.original_filename:
            base_name = os.path.splitext(os.path.basename(obj.original_filename))[0]
        else:
            base_name = None
        thumb_url = ''
        if base_name:
            webp_name = base_name + '.webp'
            webp_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'images', '460', webp_name)
            webp_url = os.path.join(settings.MEDIA_URL, 'uploads', 'images', '460', webp_name)
            if os.path.isfile(webp_path):
                thumb_url = webp_url
        if not thumb_url and obj.file_460 and obj.file_460.url:
            thumb_url = obj.file_460.url
        if thumb_url:
            return format_html('<img src="{}" style="height:60px;object-fit:cover;" />', thumb_url)
        return 'Sem imagem'
    thumbnail_tag.short_description = 'Miniatura'
    list_display = ('thumbnail_tag', 'title', 'user', 'organization', 'upload_date')
    search_fields = ('title', 'user__username', 'organization__name')
    list_filter = ('organization',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'organization', 'uploaded_at')
    search_fields = ('title', 'user__username', 'organization__name')
    list_filter = ('organization',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'organization', 'uploaded_at')
    search_fields = ('title', 'user__username', 'organization__name')
    list_filter = ('organization',)

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'organization', 'uploaded_at')
    search_fields = ('title', 'user__username', 'organization__name')
    list_filter = ('organization',)
