from django import forms
from .models import GlobalSettings

class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = ['items_per_page', 'pagination_visible_pages']
