from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image as PILImage
import os
import io

from .models_organization import Organization
from .models_like import Like

class Image(models.Model):
    original_filename = models.CharField(max_length=255, blank=True, verbose_name='Nome original do arquivo')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    original_date = models.DateField(blank=True, null=True, verbose_name='Data de criação original')
    upload_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Data de upload')
    author = models.CharField(max_length=255, blank=True, verbose_name='Autor/Fotógrafo')
    copyright = models.CharField(max_length=255, blank=True, verbose_name='Direitos autorais/Licença')
    keywords = models.CharField(max_length=512, blank=True, verbose_name='Palavras-chave/Tags')
    # Técnicos (extraídos automaticamente)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    dpi = models.CharField(max_length=32, blank=True)
    file_format = models.CharField(max_length=16, blank=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    bit_depth = models.CharField(max_length=16, blank=True)
    color_mode = models.CharField(max_length=32, blank=True)
    color_profile = models.CharField(max_length=255, blank=True)
    # Específicos para Bibliotecas
    collection = models.CharField(max_length=255, blank=True, verbose_name='Coleção/Acervo')
    catalog_number = models.CharField(max_length=128, blank=True, verbose_name='Número de catalogação')
    physical_location = models.CharField(max_length=255, blank=True, verbose_name='Localização física')
    provenance = models.CharField(max_length=255, blank=True, verbose_name='Proveniência')
    cross_reference = models.CharField(max_length=255, blank=True, verbose_name='Referência cruzada')
    exif_data = models.JSONField(blank=True, null=True, verbose_name='Dados EXIF')
    geolocation = models.CharField(max_length=255, blank=True, verbose_name='Informações geográficas/geolocalização')
    file = models.ImageField(upload_to='uploads/images/')
    file_460 = models.ImageField(upload_to='uploads/images/460/', blank=True, null=True, editable=False)

    def __str__(self):
        return self.title or self.file.name

    @property
    def likes_count(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Extração automática de metadados técnicos e EXIF
        try:
            from PIL import Image as PILImage
            import PIL.ExifTags as ExifTags
            import os
            img_path = self.file.path
            pil_img = PILImage.open(img_path)
            self.width, self.height = pil_img.size
            self.file_format = pil_img.format
            self.color_mode = pil_img.mode
            self.file_size = os.path.getsize(img_path)
            if 'dpi' in pil_img.info:
                self.dpi = str(pil_img.info['dpi'])
            else:
                self.dpi = ''
            if 'icc_profile' in pil_img.info:
                self.color_profile = 'ICC'
            else:
                self.color_profile = ''
            # Bit depth
            self.bit_depth = str(pil_img.bits) if hasattr(pil_img, 'bits') else ''
            # EXIF
            exif = pil_img._getexif() if hasattr(pil_img, '_getexif') and pil_img._getexif() else None
            exif_dict = {}
            if exif:
                for tag, value in exif.items():
                    decoded = ExifTags.TAGS.get(tag, tag)
                    exif_dict[decoded] = value
                self.exif_data = exif_dict
                # Data de criação original
                if not self.original_date:
                    dt = exif_dict.get('DateTimeOriginal')
                    if dt:
                        try:
                            self.original_date = dt.split(' ')[0].replace(':','-')
                        except Exception:
                            pass
                # Geolocalização
                gps = exif_dict.get('GPSInfo')
                if gps:
                    self.geolocation = str(gps)

            # Salva a versão 460px de largura, nomeando por hash do nome real + hash do autor
            try:
                import hashlib
                base, ext = os.path.splitext(os.path.basename(self.file.name))
                pil_img_460 = pil_img.copy()
                w, h = pil_img_460.size
                new_width = 460
                if w > new_width:
                    new_height = int(h * (new_width / w))
                    pil_img_460 = pil_img_460.resize((new_width, new_height), PILImage.LANCZOS)
                thumb_io = io.BytesIO()
                # Sempre salva a miniatura como JPEG para máxima compatibilidade
                pil_img_460 = pil_img_460.convert('RGB')
                try:
                    pil_img_460.save(thumb_io, format='JPEG')
                except Exception as e:
                    logger.error(f'Erro ao salvar miniatura JPEG para {self.file.name} (possível problema AVIF): {e}')
                    raise
                # Salva a miniatura 460 com o MESMO nome do arquivo principal, mas na pasta 460
                from django.conf import settings
                media_root = getattr(settings, 'MEDIA_ROOT', 'media')
                dest_dir = os.path.join(media_root, 'uploads', 'images', '460')
                os.makedirs(dest_dir, exist_ok=True)
                # Sempre salva a versão 460px como WEBP
                original_filename = os.path.basename(self.file.name)
                thumb_ext = '.webp'
                thumb_format = 'WEBP'
                thumb_name = f"uploads/images/460/{os.path.splitext(original_filename)[0]}{thumb_ext}"
                file_path = os.path.join(dest_dir, f"{os.path.splitext(original_filename)[0]}{thumb_ext}")
                pil_img_460 = pil_img_460.convert('RGB')
                pil_img_460.save(thumb_io, format=thumb_format, quality=90)
                with open(file_path, 'wb') as f:
                    f.write(thumb_io.getvalue())
                self.file_460.name = thumb_name
            except Exception as e:
                logger.error(f'Erro ao gerar miniatura 460px para {self.file.name}: {e}')
                pass

            super().save(update_fields=[
                'width', 'height', 'file_format', 'color_mode', 'file_size', 'dpi', 'color_profile', 'bit_depth', 'exif_data', 'original_date', 'geolocation', 'file_460'
            ])
        except Exception:
            pass

class Document(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='documents')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, blank=True, verbose_name='Autor(es)')
    subject = models.CharField(max_length=255, blank=True, verbose_name='Assunto/Tema')
    description = models.TextField(blank=True, verbose_name='Descrição/Resumo')
    creation_date = models.DateField(blank=True, null=True, verbose_name='Data de criação')
    publication_date = models.DateField(blank=True, null=True, verbose_name='Data de publicação')
    publisher = models.CharField(max_length=255, blank=True, verbose_name='Editora/Publicador')
    version = models.CharField(max_length=50, blank=True, verbose_name='Versão/Edição')
    languages = models.CharField(max_length=128, blank=True, verbose_name='Idioma(s)')
    keywords = models.CharField(max_length=512, blank=True, verbose_name='Palavras-chave/Tags')
    original_filename = models.CharField(max_length=255, blank=True, verbose_name='Nome original do arquivo')
    DOCUMENT_TYPE_CHOICES = [
        ('artigo', 'Artigo'),
        ('relatorio', 'Relatório'),
        ('livro', 'Livro'),
        ('monografia', 'Monografia'),
        ('tese', 'Tese'),
        ('outro', 'Outro'),
    ]
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, blank=True, verbose_name='Tipo de documento')
    file = models.FileField(upload_to='uploads/documents/')
    file_format = models.CharField(max_length=16, blank=True, verbose_name='Formato do arquivo')
    file_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='Tamanho do arquivo (bytes)')
    num_pages = models.PositiveIntegerField(blank=True, null=True, verbose_name='Número de páginas')
    orientation = models.CharField(max_length=16, blank=True, verbose_name='Orientação')
    extracted_text = models.TextField(blank=True, verbose_name='Texto extraído para indexação')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Preencher automaticamente campos técnicos
        if self.file:
            import os
            name, ext = os.path.splitext(self.file.name)
            self.file_format = ext[1:].upper()
            self.file_size = self.file.size
            # Extração automática de número de páginas e texto para PDF
            if self.file_format == 'PDF':
                try:
                    from PyPDF2 import PdfReader
                    self.file.open('rb')
                    reader = PdfReader(self.file)
                    self.num_pages = len(reader.pages)
                    text = "\n".join(page.extract_text() or '' for page in reader.pages)
                    self.extracted_text = text[:10000]  # Limite opcional
                    self.file.close()
                except Exception:
                    pass
        super().save(*args, **kwargs)

    @property
    def file_extension(self):
        import os
        return os.path.splitext(self.file.name)[1][1:].upper()

class Audio(models.Model):
    original_filename = models.CharField(max_length=255, blank=True, verbose_name='Nome original do arquivo')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='audios', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='audios')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/audios/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def file_extension(self):
        import os
        return os.path.splitext(self.file.name)[1][1:].lower() if self.file else ''

class Video(models.Model):
    original_filename = models.CharField(max_length=255, blank=True, verbose_name='Nome original do arquivo')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    def video_upload_to(instance, filename):
        import hashlib
        username = instance.user.username if instance.user_id else 'anon'
        file_hash = hashlib.sha256(filename.encode('utf-8')).hexdigest()
        ext = filename.split('.')[-1]
        return f"uploads/videos/{file_hash}_{username}.{ext}"

    def thumb_upload_to(instance, filename):
        import hashlib
        username = instance.user.username if instance.user_id else 'anon'
        file_hash = hashlib.sha256(filename.encode('utf-8')).hexdigest()
        return f"uploads/videos/video_thumbs/{file_hash}_{username}.webp"

    file = models.FileField(upload_to=video_upload_to)
    thumbnail = models.ImageField(upload_to=thumb_upload_to, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def file_extension(self):
        import os
        return os.path.splitext(self.file.name)[1][1:].lower() if self.file else ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file and not self.thumbnail:
            try:
                import cv2
                from PIL import Image as PILImage
                import numpy as np
                import os
                video_path = self.file.path
                cap = cv2.VideoCapture(video_path)
                success, frame = cap.read()
                if success:
                    # Convert BGR to RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img_pil = PILImage.fromarray(frame)
                    # Redimensiona para largura 460px mantendo proporção
                    w, h = img_pil.size
                    new_width = 460
                    if w > new_width:
                        new_height = int(h * (new_width / w))
                        img_pil = img_pil.resize((new_width, new_height), PILImage.LANCZOS)
                    # Salva como webp em memória
                    thumb_io = io.BytesIO()
                    img_pil.save(thumb_io, format='WEBP', quality=90)
                    thumb_io.seek(0)
                    # Caminho: videos/460/video_<id>.webp
                    import hashlib
                    username = self.user.username if self.user_id else 'anon'
                    # Usa o nome do arquivo de vídeo para gerar o hash
                    file_hash = hashlib.sha256(os.path.basename(self.file.name).encode('utf-8')).hexdigest()
                    thumb_name = f"uploads/videos/video_thumbs/{file_hash}_{username}.webp"
                    self.thumbnail.save(thumb_name, ContentFile(thumb_io.read()), save=False)
                    super().save(update_fields=['thumbnail'])
                cap.release()
            except Exception:
                pass
