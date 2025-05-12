from .models import GlobalSettings

def get_global_settings():
    return GlobalSettings.objects.first() or GlobalSettings(items_per_page=15, pagination_visible_pages=5)
