import os
import sys
import django
from pathlib import Path

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryvault.settings')
try:
    django.setup()
except Exception as e:
    print(f'Erro ao carregar Django: {e}')
    sys.exit(1)

from django.conf import settings

def print_status(msg, status):
    if status == 'OK':
        print(f'✓ {msg}')
    elif status == 'ALERTA':
        print(f'! {msg}')
    else:
        print(f'✗ {msg}')

def check_debug():
    if not settings.DEBUG:
        print_status('DEBUG está DESATIVADO.', 'OK')
    else:
        print_status('DEBUG está ATIVADO! Altere para False em produção.', 'ERRO')

def check_allowed_hosts():
    if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS != ['*']:
        print_status(f'ALLOWED_HOSTS definido: {settings.ALLOWED_HOSTS}', 'OK')
    else:
        print_status('ALLOWED_HOSTS não está definido corretamente!', 'ERRO')

def check_secret_key():
    key = getattr(settings, 'SECRET_KEY', '')
    if key and 'django-insecure' not in key:
        print_status('SECRET_KEY está definida e parece segura.', 'OK')
    else:
        print_status('SECRET_KEY padrão ou insegura! Defina uma chave forte.', 'ERRO')

def check_database():
    db = settings.DATABASES['default']
    engine = db['ENGINE']
    if 'sqlite3' in engine:
        print_status('Banco de dados SQLite NÃO recomendado para produção.', 'ALERTA')
    else:
        print_status(f'Banco de dados em uso: {engine}', 'OK')

def check_static_media():
    static_root = getattr(settings, 'STATIC_ROOT', None)
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if static_root and os.path.isdir(static_root):
        print_status(f'STATIC_ROOT definido: {static_root}', 'OK')
    else:
        print_status('STATIC_ROOT não definido ou pasta não existe!', 'ERRO')
    if media_root and os.path.isdir(media_root):
        print_status(f'MEDIA_ROOT definido: {media_root}', 'OK')
    else:
        print_status('MEDIA_ROOT não definido ou pasta não existe!', 'ALERTA')

def main():
    print('\n===== CHECKLIST DE PRODUÇÃO DJANGO =====\n')
    check_debug()
    check_allowed_hosts()
    check_secret_key()
    check_database()
    check_static_media()
    print('\nChecklist concluído! Revise os itens marcados como erro ou alerta antes de colocar em produção.\n')
    print('Sugestões de segurança adicionais:')
    print('- Ative HTTPS (SSL) com Nginx/Apache')
    print('- Revise permissões de arquivos e pastas')
    print('- Use variáveis de ambiente para segredos')
    print('- Configure firewall e backups')

if __name__ == '__main__':
    main()
