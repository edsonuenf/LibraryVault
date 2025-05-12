import os
import sys
import django
import importlib
from pathlib import Path
from django.core.management import call_command
from django.conf import settings
from termcolor import colored

def print_status(msg, status):
    if status == 'OK':
        print(colored(f'✔ {msg}', 'green'))
    elif status == 'ALERTA':
        print(colored(f'! {msg}', 'yellow'))
    else:
        print(colored(f'✖ {msg}', 'red'))

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
        # Checa dependências
        if 'postgresql' in engine:
            try:
                import psycopg2
                print_status('psycopg2 instalado.', 'OK')
            except ImportError:
                print_status('psycopg2 NÃO instalado! Rode: pip install psycopg2-binary', 'ERRO')
        elif 'mysql' in engine:
            try:
                import MySQLdb
                print_status('mysqlclient instalado.', 'OK')
            except ImportError:
                print_status('mysqlclient NÃO instalado! Rode: pip install mysqlclient', 'ERRO')
        elif 'djongo' in engine:
            try:
                import djongo
                print_status('djongo instalado.', 'OK')
            except ImportError:
                print_status('djongo NÃO instalado! Rode: pip install djongo', 'ERRO')

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

def check_collectstatic():
    static_root = getattr(settings, 'STATIC_ROOT', None)
    if static_root and os.path.isdir(static_root) and os.listdir(static_root):
        print_status('Arquivos estáticos coletados em STATIC_ROOT.', 'OK')
    else:
        print_status('Arquivos estáticos NÃO coletados! Rode: python manage.py collectstatic', 'ERRO')

def check_migrations():
    try:
        call_command('showmigrations', '--plan')
        print_status('Migrações aplicadas/verificadas.', 'OK')
    except Exception:
        print_status('Erro ao verificar migrações!', 'ERRO')

def check_superuser():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if User.objects.filter(is_superuser=True).exists():
        print_status('Superusuário existe.', 'OK')
    else:
        print_status('NÃO existe superusuário! Crie um com: python manage.py createsuperuser', 'ERRO')

def check_wsgi():
    try:
        import gunicorn
        print_status('Gunicorn instalado.', 'OK')
    except ImportError:
        try:
            import waitress
            print_status('Waitress instalado.', 'OK')
        except ImportError:
            print_status('Nenhum servidor WSGI (gunicorn/waitress) instalado! Instale um para produção.', 'ALERTA')

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryvault.settings')
    try:
        django.setup()
    except Exception as e:
        print(colored(f'Erro ao carregar Django: {e}', 'red'))
        sys.exit(1)
    print(colored('\n===== CHECKLIST DE PRODUÇÃO DJANGO =====\n', 'cyan', attrs=['bold']))
    check_debug()
    check_allowed_hosts()
    check_secret_key()
    check_database()
    check_static_media()
    check_collectstatic()
    check_migrations()
    check_superuser()
    check_wsgi()
    print(colored('\nChecklist concluído! Revise os itens em vermelho/alaranja antes de colocar em produção.\n', 'cyan', attrs=['bold']))
    print('Sugestões de segurança adicionais:')
    print('- Ative HTTPS (SSL) com Nginx/Apache')
    print('- Revise permissões de arquivos e pastas')
    print('- Use variáveis de ambiente para segredos')
    print('- Configure firewall e backups')

if __name__ == '__main__':
    main()
