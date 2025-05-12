from django.urls import path
from .views import global_settings_view

app_name = 'config'
urlpatterns = [
    path('global/', global_settings_view, name='global_settings'),
]
