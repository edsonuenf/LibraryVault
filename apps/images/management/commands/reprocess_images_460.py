from django.core.management.base import BaseCommand
from django.conf import settings
from apps.images.models import Image
import hashlib
import os
from PIL import Image as PILImage
import io

class Command(BaseCommand):
    help = 'Reprocessa todas as imagens para garantir que a versão 460px hashificada seja criada e salva corretamente.'

    def handle(self, *args, **options):
        media_root = getattr(settings, 'MEDIA_ROOT', 'media')
        dest_dir = os.path.join(media_root, 'uploads', 'images', '460')
        os.makedirs(dest_dir, exist_ok=True)
        count = 0
        for img in Image.objects.all():
            if not img.file:
                continue
            original_filename = os.path.basename(img.file.name)
            ext = os.path.splitext(original_filename)[1].lower()
            if ext == '.png':
                thumb_ext = '.png'
                thumb_format = 'PNG'
            elif ext in ['.jpg', '.jpeg']:
                thumb_ext = '.jpg'
                thumb_format = 'JPEG'
            elif ext == '.gif':
                thumb_ext = '.gif'
                thumb_format = 'GIF'
            elif ext == '.svg':
                thumb_ext = '.svg'
                thumb_format = 'SVG'
            elif ext == '.cdr':
                thumb_ext = '.cdr'
                thumb_format = 'CDR'
            elif ext in ['.tif', '.tiff']:
                thumb_ext = '.tif'
                thumb_format = 'TIFF'
            elif ext == '.webp':
                thumb_ext = '.webp'
                thumb_format = 'WEBP'
            elif ext == '.html':
                # Miniatura de HTML: apenas copia o arquivo para a pasta 460
                thumb_ext = '.html'
                original_filename = os.path.basename(img.file.name)
                thumb_name = f"uploads/images/460/{os.path.splitext(original_filename)[0]}{thumb_ext}"
                file_path = os.path.join(dest_dir, f"{os.path.splitext(original_filename)[0]}{thumb_ext}")
                import shutil
                shutil.copyfile(img.file.path, file_path)
                img.file_460.name = thumb_name
                img.save(update_fields=['file_460'])
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Processado: {img.id} -> {thumb_name}'))
                continue
            else:
                # Ignora outros formatos por enquanto
                continue
            try:
                pil_img_460 = pil_img_460.convert('RGB') if thumb_format in ['JPEG', 'WEBP'] else pil_img_460
                pil_img_460.save(thumb_io, format=thumb_format)
            except Exception:
                # Se Pillow não suportar o formato para salvar, ignora
                continue
            thumb_name = f"uploads/images/460/{os.path.splitext(original_filename)[0]}{thumb_ext}"
            file_path = os.path.join(dest_dir, f"{os.path.splitext(original_filename)[0]}{thumb_ext}")
            # Só gera se não existir ou se o campo file_460 não estiver correto
            if not os.path.exists(file_path) or img.file_460.name != thumb_name:
                try:
                    pil_img = PILImage.open(img.file.path)
                    w, h = pil_img.size
                    new_width = 460
                    if w > new_width:
                        new_height = int(h * (new_width / w))
                        pil_img_460 = pil_img.resize((new_width, new_height), PILImage.LANCZOS)
                    else:
                        pil_img_460 = pil_img.copy()
                    thumb_io = io.BytesIO()
                    pil_img_460 = pil_img_460.convert('RGB') if thumb_format == 'JPEG' else pil_img_460
                    pil_img_460.save(thumb_io, format=thumb_format)
                    with open(file_path, 'wb') as f:
                        f.write(thumb_io.getvalue())
                    img.file_460.name = thumb_name
                    img.save(update_fields=['file_460'])
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f'Processado: {img.id} -> {thumb_name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Erro ao processar imagem {img.id}: {e}'))
        self.stdout.write(self.style.SUCCESS(f'Finalizado. {count} imagens processadas.'))
