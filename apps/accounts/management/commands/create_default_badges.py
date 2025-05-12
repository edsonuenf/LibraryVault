
from apps.accounts.models import Badge

BADGES = [
    {
        'name': 'Primeiro Upload',
        'description': 'Realize seu primeiro upload de imagem, áudio ou vídeo.',
        'icon': 'bi-upload',
    },
    {
        'name': 'Perfil Completo',
        'description': 'Preencha todos os campos do seu perfil.',
        'icon': 'bi-person-check',
    },
    {
        'name': 'Uploader do Mês',
        'description': 'Seja o usuário com mais uploads em um mês.',
        'icon': 'bi-trophy',
    },
    {
        'name': '10 Imagens',
        'description': 'Envie 10 imagens.',
        'icon': 'bi-image',
    },
    {
        'name': '100 Imagens',
        'description': 'Envie 100 imagens.',
        'icon': 'bi-images',
    },
]

class Command(BaseCommand):
    help = 'Cria badges/conquistas padrão para o sistema.'

    def handle(self, *args, **options):
        for badge_data in BADGES:
            badge, created = Badge.objects.get_or_create(name=badge_data['name'], defaults=badge_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Badge criado: {badge.name}"))
            else:
                self.stdout.write(f"Badge já existe: {badge.name}")
