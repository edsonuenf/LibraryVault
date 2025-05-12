from django.core.management.base import BaseCommand
import os
from PIL import Image

class Command(BaseCommand):
    help = 'Converte todas as imagens da pasta uploads/images/460 para webp e remove os arquivos antigos (exceto .webp)'

    def handle(self, *args, **options):
        pasta = os.path.join('media', 'uploads', 'images', '460')
        if not os.path.exists(pasta):
            self.stdout.write(self.style.ERROR(f'Pasta não encontrada: {pasta}'))
            return
        convertidos = 0
        for nome_arquivo in os.listdir(pasta):
            caminho = os.path.join(pasta, nome_arquivo)
            if not os.path.isfile(caminho):
                continue
            nome, ext = os.path.splitext(nome_arquivo)
            if ext.lower() == '.webp':
                continue
            try:
                img = Image.open(caminho).convert('RGB')
                destino = os.path.join(pasta, nome + '.webp')
                img.save(destino, 'WEBP', quality=90)
                os.remove(caminho)
                convertidos += 1
                self.stdout.write(self.style.SUCCESS(f'Convertido: {nome_arquivo} -> {nome}.webp'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao converter {nome_arquivo}: {e}'))
        self.stdout.write(self.style.SUCCESS(f'Total convertidos: {convertidos}'))
