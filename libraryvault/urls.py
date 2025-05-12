from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return HttpResponse('<h1>Bem-vindo ao LibraryVault!</h1><p>O sistema está rodando corretamente.</p>')

urlpatterns = [
    path('core/', include('apps.core.urls')),
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),  # Rotas do django-allauth
    path('accounts/', include('django.contrib.auth.urls')),  # Rotas padrão do Django para login, logout, password_reset, etc.
    path('config/', include(('apps.config.urls', 'config'), namespace='config')),
]

urlpatterns += [
    path('images/', include('apps.images.urls', namespace='images')),
    path('documents/', include('apps.documents.urls', namespace='documents')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
