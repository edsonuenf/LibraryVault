from django.db import models
from django.contrib.auth import get_user_model

class Document(models.Model):
    DOC_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'Word'),
        ('txt', 'Texto'),
        ('xlsx', 'Excel'),
        ('ods', 'OpenDocument Spreadsheet'),
        ('pptx', 'PowerPoint'),
        ('odp', 'OpenDocument Presentation'),
        ('jpg', 'Imagem JPG'),
        ('png', 'Imagem PNG'),
        ('outro', 'Outro'),
    ]

    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    creation_date = models.DateField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=50, blank=True)
    languages = models.CharField(max_length=100, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    doc_type = models.CharField(max_length=10, choices=DOC_TYPES, default='outro')
    file = models.FileField(upload_to='documents/%Y/%m/')
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='versions')
    is_active = models.BooleanField(default=True)
    folder = models.CharField(max_length=255, blank=True)  # para organização por pastas

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return self.title
