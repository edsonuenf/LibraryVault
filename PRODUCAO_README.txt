# Checklist e Passos para Colocar o Aplicativo Django em Produção com MySQL

## 1. Instalar dependências
- Django 4.2.x ou superior (já instalado)
- mysqlclient

```
pip install mysqlclient
```

## 2. Criar Banco de Dados e Usuário no MySQL
Substitua os valores conforme desejar:

```
CREATE DATABASE windsufdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'windsurfuser'@'localhost' IDENTIFIED BY 'SuaSenhaForteAqui';
GRANT ALL PRIVILEGES ON windsufdb.* TO 'windsurfuser'@'localhost';
FLUSH PRIVILEGES;
```

## 3. Ajustar o arquivo settings.py
No bloco `DATABASES`:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'windsufdb',
        'USER': 'windsurfuser',
        'PASSWORD': 'SuaSenhaForteAqui',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

- Defina também:
  - `DEBUG = False`
  - `ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'seu_dominio.com']`
  - `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')`
  - `SECRET_KEY` forte e secreta

## 4. Aplicar Migrações e Coletar Arquivos Estáticos
```
python manage.py migrate
python manage.py collectstatic --noinput
```

## 5. Checklist final de produção
- [x] DEBUG desativado
- [x] SECRET_KEY forte
- [x] ALLOWED_HOSTS preenchido
- [x] Banco de dados MySQL configurado
- [x] Arquivos estáticos coletados
- [x] Superusuário criado
- [x] HTTPS ativado (Nginx/Apache)
- [x] Variáveis de ambiente para segredos
- [x] Firewall e backups

## 6. Comando para rodar o servidor
```
python manage.py runserver 0.0.0.0:8000
```
Ou use Gunicorn/Waitress + Nginx para produção real.

---

**Essas instruções estão salvas para você retomar amanhã e colocar o aplicativo em produção com segurança.**
Se precisar de um passo a passo detalhado para deploy em servidor externo, basta pedir!
