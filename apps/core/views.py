from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django import forms

User = get_user_model()

class FirstSuperuserForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data

def first_superuser_wizard(request):
    User = get_user_model()
    if User.objects.filter(is_superuser=True).exists():
        return redirect('admin:login')
    if request.method == 'POST':
        form = FirstSuperuserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_superuser(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('admin:index')
    else:
        form = FirstSuperuserForm()
    return render(request, 'core/first_superuser.html', {'form': form})
