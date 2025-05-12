# Views para registro, login, logout e dashboard do usuário. Usa formulários customizados e autenticação padrão Django.

from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Organization
from apps.images.models import Image, Document, Video
from apps.images.views import dashboard_video_stats
import calendar

# User Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def dashboard(request):
    User = get_user_model()
    total_users = User.objects.count()
    if request.user.is_superuser:
        total_images = Image.objects.count()
        total_documents = Document.objects.count()
        total_videos = Video.objects.count()
    else:
        total_images = Image.objects.filter(user=request.user).count()
        total_documents = Document.objects.filter(user=request.user).count()
        total_videos = Video.objects.filter(user=request.user).count()

    # Estatística de uploads por mês
    current_year = timezone.now().year
    if request.user.is_superuser:
        images_qs = Image.objects.filter(upload_date__year=current_year)
        documents_qs = Document.objects.filter(uploaded_at__year=current_year)
        videos_qs = Video.objects.filter(uploaded_at__year=current_year)
    else:
        images_qs = Image.objects.filter(user=request.user, upload_date__year=current_year)
        documents_qs = Document.objects.filter(user=request.user, uploaded_at__year=current_year)
        videos_qs = Video.objects.filter(user=request.user, uploaded_at__year=current_year)

    images_month = images_qs.annotate(month=TruncMonth('upload_date')).values('month').annotate(count=Count('id')).order_by('month')
    images_per_month = {m:0 for m in range(1,13)}
    for entry in images_month:
        if entry['month']:
            images_per_month[entry['month'].month] += entry['count']
    documents_month = documents_qs.annotate(month=TruncMonth('uploaded_at')).values('month').annotate(count=Count('id')).order_by('month')
    documents_per_month = {m:0 for m in range(1,13)}
    for entry in documents_month:
        if entry['month']:
            documents_per_month[entry['month'].month] += entry['count']
    images_per_month_list = [images_per_month[m] for m in range(1,13)]
    documents_per_month_list = [documents_per_month[m] for m in range(1,13)]

    videos_per_month_list = dashboard_video_stats(request)

    context = {
        'total_users': total_users,
        'total_images': total_images,
        'total_documents': total_documents,
        'total_videos': total_videos,
        'images_per_month': images_per_month_list,
        'documents_per_month': documents_per_month_list,
        'videos_per_month': videos_per_month_list,
    }
    return render(request, 'accounts/dashboard.html', context)

# Página de perfil do usuário
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

from django.contrib import messages

@login_required
def edit_profile(request):
    from .forms import ProfileForm
    user = request.user
    if request.method == 'POST':
        if 'delete_profile_picture' in request.POST:
            if user.profile_picture:
                user.profile_picture.delete(save=False)
                user.profile_picture = None
                user.save()
                messages.success(request, 'Foto de perfil removida com sucesso!')
                return redirect('accounts:edit_profile')
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'accounts/edit_profile.html', {'form': form, 'user': user})

from django.db.models import Count
from apps.images.models import Image, Audio, Video
from django.utils import timezone
from datetime import timedelta


from .models import Badge, UserBadge

def grant_badge(user, badge_name):
    badge, _ = Badge.objects.get_or_create(name=badge_name, defaults={'description': badge_name, 'icon': ''})
    UserBadge.objects.get_or_create(user=user, badge=badge)


@login_required
def dashboard_profile(request):
    user = request.user
    # Total de imagens
    total_images = Image.objects.filter(user=user).count()
    total_audios = Audio.objects.filter(user=user).count()
    total_videos = Video.objects.filter(user=user).count()
    # Data do último upload
    last_image = Image.objects.filter(user=user).order_by('-upload_date').first()
    last_audio = Audio.objects.filter(user=user).order_by('-uploaded_at').first()
    last_video = Video.objects.filter(user=user).order_by('-uploaded_at').first()
    # Tipo de mídia mais enviada
    media_counts = {
        'Imagens': total_images,
        'Áudios': total_audios,
        'Vídeos': total_videos,
    }
    top_media = max(media_counts, key=media_counts.get) if any(media_counts.values()) else None
    # Gráfico: uploads por mês (últimos 12 meses)
    today = timezone.now().date().replace(day=1)
    months = [(today - timedelta(days=30*i)).replace(day=1) for i in reversed(range(12))]
    image_counts = []
    for m in months:
        next_month = (m + timedelta(days=32)).replace(day=1)
        count = Image.objects.filter(user=user, upload_date__gte=m, upload_date__lt=next_month).count()
        image_counts.append({'month': m.strftime('%b/%Y'), 'count': count})
    # Badges: primeiro upload, 10 e 100 imagens, perfil completo
    if total_images >= 1:
        grant_badge(user, 'Primeiro Upload')
    if total_images >= 10:
        grant_badge(user, '10 Imagens')
    if total_images >= 100:
        grant_badge(user, '100 Imagens')
    # Perfil completo
    required_fields = ['first_name','last_name','organization','endereco','cep','telefone','profile_picture']
    if all(getattr(user, f) for f in required_fields):
        grant_badge(user, 'Perfil Completo')
    # Badges do usuário
    user_badges = UserBadge.objects.filter(user=user).select_related('badge')
    chart_labels = [item['month'] for item in image_counts]
    chart_data = [item['count'] for item in image_counts]
    context = {
        'total_images': total_images,
        'total_audios': total_audios,
        'total_videos': total_videos,
        'last_image': last_image,
        'last_audio': last_audio,
        'last_video': last_video,
        'top_media': top_media,
        'image_counts': image_counts,
        'user_badges': user_badges,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'accounts/dashboard_profile.html', context)

# Funções auxiliares para checar papel

def is_admin(user):
    return user.is_superuser or user.membership_set.filter(role='ADMIN').exists()

def is_librarian(user):
    return user.membership_set.filter(role='LIBRARIAN').exists()

@user_passes_test(is_admin)
def admin_only_view(request):
    return render(request, 'accounts/admin_only.html')

@user_passes_test(is_librarian)
def librarian_only_view(request):
    return render(request, 'accounts/librarian_only.html')
