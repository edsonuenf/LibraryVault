# Guia de Configuração para Produção - LibraryVault

Este guia descreve as etapas necessárias para configurar o LibraryVault em um ambiente de produção seguro e otimizado.

## Configurações Essenciais de Segurança

### 1. Configurar Variáveis de Ambiente

Em produção, todas as configurações sensíveis devem ser definidas através de variáveis de ambiente ou um arquivo `.env` seguro:

```
SECRET_KEY=chave_secreta_longa_e_aleatoria
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgres://usuario:senha@host:porta/banco

# Configurações de email
EMAIL_HOST=smtp.provedor.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu_email@provedor.com
EMAIL_HOST_PASSWORD=sua_senha
EMAIL_USE_TLS=True

# Configurações de armazenamento (se usar S3/MinIO)
AWS_ACCESS_KEY_ID=sua_chave_de_acesso
AWS_SECRET_ACCESS_KEY=sua_chave_secreta
AWS_STORAGE_BUCKET_NAME=seu_bucket
```

### 2. Configurar Banco de Dados

Para PostgreSQL (recomendado para produção):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'libraryvault',
        'USER': 'usuario_producao',
        'PASSWORD': 'senha_segura',
        'HOST': 'localhost',  # ou endereço do servidor de banco de dados
        'PORT': '5432',
        'CONN_MAX_AGE': 600,  # manter conexões por 10 minutos
        'OPTIONS': {
            'sslmode': 'require',  # se usar SSL
        }
    }
}
```

### 3. Configurar Servidor Web

#### Usando Gunicorn

Instale o Gunicorn:
```bash
pip install gunicorn
```

Execute o servidor:
```bash
gunicorn libraryvault.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
```

#### Configuração com Nginx (proxy reverso)

Exemplo de configuração do Nginx:

```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    # Redirecionar para HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name seu-dominio.com www.seu-dominio.com;

    ssl_certificate /caminho/para/certificado.pem;
    ssl_certificate_key /caminho/para/chave.pem;

    # Configurações SSL recomendadas
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_session_cache shared:SSL:10m;

    # Arquivos estáticos
    location /static/ {
        alias /caminho/para/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    # Arquivos de mídia
    location /media/ {
        alias /caminho/para/media/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    # Proxy para o Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Configurar Serviços Adicionais

#### Redis (para cache e tarefas em segundo plano)

```python
# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/2'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
```

#### Configurar Armazenamento de Arquivos

Para MinIO ou S3:

```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

AWS_S3_ENDPOINT_URL = 'https://seu-endpoint-minio-ou-s3'
AWS_ACCESS_KEY_ID = 'sua_chave_de_acesso'
AWS_SECRET_ACCESS_KEY = 'sua_chave_secreta'
AWS_STORAGE_BUCKET_NAME = 'seu_bucket'
AWS_S3_CUSTOM_DOMAIN = 'seu-dominio-cdn.com'  # opcional, se usar CDN
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = 'public-read'
```

## Checklist Final de Produção

Execute o script de verificação antes do deploy:

```bash
python production_checklist.py
```

Certifique-se de que todos os itens estejam marcados como "OK" antes de colocar em produção.

## Monitoramento e Manutenção

### 1. Configurar Logs

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/caminho/para/logs/libraryvault.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

### 2. Backups

Configure backups automáticos para:
- Banco de dados
- Arquivos de mídia
- Configurações

### 3. Atualizações de Segurança

Mantenha o sistema atualizado regularmente:

```bash
pip install --upgrade -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
```

## Deploy com Docker em Produção

Se estiver usando Docker em produção, crie um arquivo `docker-compose.prod.yml` otimizado:

```yaml
version: '3.9'
services:
  web:
    build: .
    restart: always
    env_file: .env.prod
    depends_on:
      - db
      - redis
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    command: gunicorn libraryvault.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
  
  db:
    image: postgres:15
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file: .env.prod.db
  
  redis:
    image: redis:7
    restart: always
  
  nginx:
    image: nginx:1.25
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - static_volume:/usr/share/nginx/html/static
      - media_volume:/usr/share/nginx/html/media
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```
