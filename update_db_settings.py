"""
Script utilitário para atualizar o settings.py do Django de acordo com a configuração escolhida no admin (DatabaseConfig).
Requer que o Django esteja instalado e o DJANGO_SETTINGS_MODULE configurado.
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryvault.settings')
django.setup()

from apps.core.models import DatabaseConfig

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), 'libraryvault', 'settings.py')

DB_ENGINES = {
    'sqlite': 'django.db.backends.sqlite3',
    'mysql': 'django.db.backends.mysql',
    'postgres': 'django.db.backends.postgresql',
    # MongoDB não é backend oficial do Django, mas pode ser usado com djongo ou mongoengine
    'mongodb': 'djongo',
}

def update_settings():
    try:
        config = DatabaseConfig.objects.latest('id')
    except DatabaseConfig.DoesNotExist:
        print('Nenhuma configuração de banco encontrada.')
        sys.exit(1)
    engine = DB_ENGINES.get(config.db_engine, 'django.db.backends.sqlite3')
    if config.db_engine == 'sqlite':
        db_settings = f"""
DATABASES = {{
    'default': {{
        'ENGINE': '{engine}',
        'NAME': '{config.db_name or os.path.join(os.path.dirname(__file__), 'db.sqlite3')}',
    }}
}}
"""
    elif config.db_engine == 'mongodb':
        db_settings = f"""
DATABASES = {{
    'default': {{
        'ENGINE': '{engine}',
        'NAME': '{config.db_name}',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {{
            'host': '{config.db_host}',
            'port': {config.db_port or 27017},
            'username': '{config.db_user}',
            'password': '{config.db_password}',
        }}
    }}
}}
"""
    else:
        db_settings = f"""
DATABASES = {{
    'default': {{
        'ENGINE': '{engine}',
        'NAME': '{config.db_name}',
        'USER': '{config.db_user}',
        'PASSWORD': '{config.db_password}',
        'HOST': '{config.db_host}',
        'PORT': '{config.db_port}',
    }}
}}
"""
    # Atualiza o settings.py
    with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Remove blocos antigos de DATABASES
    new_lines = []
    in_db_block = False
    for line in lines:
        if line.strip().startswith('DATABASES ='):
            in_db_block = True
            continue
        if in_db_block and line.strip().startswith('}'):  # fim do bloco
            in_db_block = False
            continue
        if not in_db_block:
            new_lines.append(line)
    new_lines.append('\n# Atualizado automaticamente pelo update_db_settings.py\n')
    new_lines.append(db_settings)
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print('Configuração de banco de dados atualizada com sucesso!')

if __name__ == '__main__':
    update_settings()
