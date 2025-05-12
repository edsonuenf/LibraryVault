from django.urls import path
from . import views
from . import views_bulk

app_name = 'images'

from django.shortcuts import redirect

urlpatterns = [
    path('bulk-delete-documents/', views_bulk.bulk_delete_documents, name='bulk_delete_documents'),
    path('bulk-delete-audios/', views_bulk.bulk_delete_audios, name='bulk_delete_audios'),
    path('', lambda request: redirect('images:image_list'), name='images_root'),
    path('bulk-delete-videos/', views_bulk.bulk_delete_videos, name='bulk_delete_videos'),
    path('bulk-delete/', views_bulk.bulk_delete_images, name='bulk_delete_images'),
    path('relatorio-imagens-usuario/', views.relatorio_imagens_usuario, name='relatorio_imagens_usuario'),
    path('delete-video/<int:pk>/', views.delete_video, name='delete_video'),
    path('delete-image/<int:pk>/', views.delete_image, name='delete_image'),
    path('delete-document/<int:pk>/', views.delete_document, name='delete_document'),
    path('download-document/<int:pk>/', views.download_document, name='download_document'),
    path('download-audio/<int:pk>/', views.download_audio, name='download_audio'),
    path('download-video/<int:pk>/', views.download_video, name='download_video'),
    path('download-image/<int:pk>/', views.download_image, name='download_image'),
    path('delete-audio/<int:pk>/', views.delete_audio, name='delete_audio'),
    path('upload/', views.upload_image, name='upload_image'),
    path('list/', views.image_list, name='image_list'),
    path('toggle-like/<int:image_id>/', views.toggle_like, name='toggle_like'),
    path('imagem/<int:pk>/', views.image_detail, name='image_detail'),
    path('imagem/<int:pk>/export/<str:fmt>/', views.image_export_metadata, name='image_export_metadata'),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('list-documents/', views.document_list, name='document_list'),
    path('upload-video/', views.upload_video, name='upload_video'),
    path('list-videos/', views.video_list, name='video_list'),
    path('upload-audio/', views.upload_audio, name='upload_audio'),
    path('list-audios/', views.audio_list, name='audio_list'),
]
