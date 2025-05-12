from django.apps import AppConfig

import os
class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.images'
    path = os.path.dirname(os.path.abspath(__file__))

    def ready(self):
        import apps.images.signals
