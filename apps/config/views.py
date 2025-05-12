from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import GlobalSettings
from .forms import GlobalSettingsForm

def is_admin_or_superadmin(user):
    return user.is_superuser or (hasattr(user, 'userprofile') and getattr(user.userprofile, 'is_admin', False))

@user_passes_test(is_admin_or_superadmin)
def global_settings_view(request):
    settings = GlobalSettings.objects.first()
    if not settings:
        settings = GlobalSettings.objects.create()
    if request.method == 'POST':
        form = GlobalSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('config:global_settings')
    else:
        form = GlobalSettingsForm(instance=settings)
    return render(request, 'config/global_settings.html', {'form': form})
