from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/dashboard/', views.dashboard_profile, name='dashboard_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('admin-only/', views.admin_only_view, name='admin_only'),
    path('librarian-only/', views.librarian_only_view, name='librarian_only'),
]
