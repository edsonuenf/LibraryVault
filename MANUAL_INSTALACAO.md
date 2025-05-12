# Manual de Instalação – Banco de Documentos

Este manual descreve o processo de instalação do sistema Banco de Documentos em ambiente local ou servidor antes do deploy.

## Pré-requisitos
- Python 3.8 ou superior
- Git
- Gerenciador de pacotes pip
- (Opcional) Ambiente virtual Python (venv)
- Banco de dados (ex: SQLite, PostgreSQL ou outro suportado)

## Passos de Instalação

### 1. Clonar o Repositório
Execute no terminal:
```bash
git clone <URL_DO_REPOSITORIO>
cd banco-de-imagem
```

### 2. Criar Ambiente Virtual (Recomendado)
```bash
python -m venv venv
# Ativar no Windows:
venv\Scripts\activate
# Ativar no Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto e configure as variáveis necessárias, como:
```
SECRET_KEY=sua_chave_secreta
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Migrar o Banco de Dados
```bash
python manage.py migrate
```

### 6. Criar Superusuário
```bash
python manage.py createsuperuser
```

### 7. Testar Execução Local
```bash
python manage.py runserver
```
Acesse `http://localhost:8000` para verificar se o sistema está funcionando.

## Observações
- Adapte as configurações do banco de dados conforme o ambiente de produção.
- Certifique-se de que as portas necessárias estejam liberadas.
- Consulte a documentação do framework utilizado para detalhes adicionais.

Pronto! O sistema está preparado para ser configurado para deploy.
