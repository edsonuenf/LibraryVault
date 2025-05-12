from django.urls import path
from .views import first_superuser_wizard

urlpatterns = [
    path('first-superuser/', first_superuser_wizard, name='first_superuser'),
]
