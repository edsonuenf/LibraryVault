from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='list'),
    path('upload/', views.document_upload, name='upload'),
    path('teste-upload-multiplo/', views.teste_upload_multiplo, name='teste_upload_multiplo'),
]
