# Guia de Instalação - LibraryVault

Este guia descreve o processo completo de instalação do sistema LibraryVault em ambiente de desenvolvimento e produção.

## Pré-requisitos

- Python 3.8 ou superior
- Git
- Pip (gerenciador de pacotes Python)
- Ambiente virtual Python (recomendado)
- MySQL, PostgreSQL ou SQLite (para desenvolvimento)
- Docker e Docker Compose (opcional, para ambiente containerizado)

## Instalação para Desenvolvimento

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd LibraryVault
```

### 2. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```
SECRET_KEY=sua_chave_secreta_segura
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Para Google Auth (opcional)
GOOGLE_CLIENT_ID=seu_client_id
GOOGLE_CLIENT_SECRET=seu_client_secret

# Para Microsoft Auth (opcional)
MICROSOFT_CLIENT_ID=seu_client_id
MICROSOFT_CLIENT_SECRET=seu_client_secret
```

### 5. Configurar Banco de Dados

Para SQLite (desenvolvimento):
- Já está configurado por padrão

Para MySQL:
- Instale o pacote: `pip install mysqlclient`
- Edite o arquivo `libraryvault/settings.py` para usar MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'libraryvault',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Para PostgreSQL:
- Instale o pacote: `pip install psycopg2-binary`
- Edite o arquivo `libraryvault/settings.py` para usar PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'libraryvault',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Aplicar Migrações

```bash
python manage.py migrate
```

### 7. Criar Superusuário

```bash
python manage.py createsuperuser
```

### 8. Coletar Arquivos Estáticos

```bash
python manage.py collectstatic
```

### 9. Iniciar Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000` para verificar se a aplicação está funcionando.

## Instalação com Docker (Desenvolvimento ou Produção)

### 1. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as configurações necessárias.

### 2. Iniciar com Docker Compose

```bash
docker-compose up --build
```

Este comando iniciará todos os serviços definidos no `docker-compose.yml`, incluindo:
- Banco de dados PostgreSQL
- MinIO para armazenamento de arquivos
- Redis para cache e tarefas assíncronas
- ElasticSearch para busca
- Weaviate para vetorização e busca semântica

### 3. Executar Migrações e Criar Superusuário

```bash
# Em outro terminal, com os containers rodando
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Verificação de Ambiente de Produção

Antes de colocar em produção, execute o script de verificação:

```bash
python production_checklist.py
```

Este script verificará se todas as configurações necessárias para produção estão corretas.
