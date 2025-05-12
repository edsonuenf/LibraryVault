from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'organization')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('organization',)

from PIL import Image
from django.core.files.base import ContentFile
import io
import os

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, label='Email')
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'organization', 'endereco', 'cep', 'telefone', 'profile_picture', 'email')

    def save(self, commit=True):
        instance = super().save(commit=False)
        uploaded = self.cleaned_data.get('profile_picture')
        if uploaded:
            try:
                img = Image.open(uploaded)
                img = img.convert('RGBA') if img.mode in ('RGBA', 'LA') else img.convert('RGB')
                buffer = io.BytesIO()
                img.save(buffer, format='WEBP')
                file_name = os.path.splitext(uploaded.name)[0] + '.webp'
                instance.profile_picture.save(file_name, ContentFile(buffer.getvalue()), save=False)
            except Exception:
                pass  # fallback: salva original se não conseguir converter
        if commit:
            instance.save()
        return instance
