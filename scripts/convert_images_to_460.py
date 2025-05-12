import os
import django
from django.core.files.base import ContentFile
from PIL import Image as PILImage
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryvault.settings')  # Altere se o settings for diferente

django.setup()

from apps.images.models import Image

def generate_460_version(img_obj):
    if not img_obj.file_460 and img_obj.file:
        try:
            img_path = img_obj.file.path
            pil_img = PILImage.open(img_path)
            w, h = pil_img.size
            new_height = 460
            if h > new_height:
                new_width = int(w * (new_height / h))
                pil_img_460 = pil_img.resize((new_width, new_height), PILImage.LANCZOS)
            else:
                pil_img_460 = pil_img.copy()
            thumb_io = io.BytesIO()
            pil_img_460.save(thumb_io, format=pil_img.format)
            base, ext = os.path.splitext(os.path.basename(img_obj.file.name))
            thumb_name = f"uploads/images/460/{base}_460{ext}"
            img_obj.file_460.save(thumb_name, ContentFile(thumb_io.getvalue()), save=True)
            print(f"Convertida: {img_obj.file.name} -> {thumb_name}")
        except Exception as e:
            print(f"Erro ao converter {img_obj.file.name}: {e}")

if __name__ == "__main__":
    images = Image.objects.filter(file_460__isnull=True).exclude(file='')
    print(f"Total de imagens para converter: {images.count()}")
    for img in images:
        generate_460_version(img)
    print("Conversão concluída.")
