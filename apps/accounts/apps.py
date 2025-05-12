from django.apps import AppConfig

import os
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Accounts & Permissions'
    path = os.path.dirname(os.path.abspath(__file__))
