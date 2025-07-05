# Deploy do Sistema CRM Django no Debian Bookworm

Este guia cobre o passo a passo para deploy do sistema CRM Django com MySQL, Gunicorn e Nginx no Debian 12 (Bookworm).

---

## 1. Atualize o sistema
```bash
sudo apt update && sudo apt upgrade -y
```

## 2. Instale dependências do sistema
```bash
sudo apt install python3 python3-venv python3-pip python3-dev build-essential libmysqlclient-dev \
    mysql-server nginx git -y
sudo systemctl enable --now mysql
sudo systemctl enable --now nginx
```

## 3. Clone o projeto
```bash
git clone <url-do-repositorio>
cd crm
```

## 4. Crie e ative o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

## 5. Instale as dependências Python
```bash
pip install -r requirements.txt
```

## 6. Configure o banco de dados MySQL
```bash
sudo mysql -u root

CREATE DATABASE crmBD CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'crmBD'@'localhost' IDENTIFIED BY 'crm123';
GRANT ALL PRIVILEGES ON crmBD.* TO 'crmBD'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 7. Configure as variáveis do Django
- Edite `crm/settings.py` e confira as credenciais do banco:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crmBD',
        'USER': 'crmBD',
        'PASSWORD': 'crm123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

## 8. Migre o banco e crie superusuário
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 9. Teste localmente
```bash
python manage.py runserver 0.0.0.0:8000
```
Acesse: http://<ip-do-servidor>:8000

---

## 10. Configure Gunicorn

### Instale Gunicorn
```bash
pip install gunicorn
```

### Teste Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 crm.wsgi:application
```

### Crie um serviço systemd para Gunicorn
Crie o arquivo `/etc/systemd/system/crm_gunicorn.service`:
```ini
[Unit]
Description=Gunicorn instance to serve CRM Django
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/caminho/para/seu/projeto/crm
Environment="PATH=/caminho/para/seu/projeto/crm/venv/bin"
ExecStart=/caminho/para/seu/projeto/crm/venv/bin/gunicorn --workers 3 --bind unix:/caminho/para/seu/projeto/crm/crm.sock crm.wsgi:application

[Install]
WantedBy=multi-user.target
```
> Substitua `/caminho/para/seu/projeto/crm` pelo caminho real do projeto.

### Ative e inicie o serviço
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now crm_gunicorn
```

---

## 11. Configure o Nginx

Crie o arquivo `/etc/nginx/sites-available/crm`:
```nginx
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /caminho/para/seu/projeto/crm/static/;
    }
    location /media/ {
        alias /caminho/para/seu/projeto/crm/media/;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/caminho/para/seu/projeto/crm/crm.sock;
    }
}
```
> Substitua `/caminho/para/seu/projeto/crm` pelo caminho real do projeto.

Ative o site e reinicie o Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/crm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 12. Coletar arquivos estáticos
```bash
source venv/bin/activate
python manage.py collectstatic
```

---

## 13. Permissões

Garanta que o usuário `www-data` tenha acesso ao diretório do projeto:
```bash
sudo chown -R www-data:www-data /caminho/para/seu/projeto/crm
```

---

## 14. Uploads e mídia
- O diretório `media/` será usado para uploads (ex: logo do sistema).
- O diretório `static/` será usado para arquivos estáticos (CSS, JS, etc).

---

## 15. Segurança e produção
- Configure um domínio real e HTTPS (Let's Encrypt).
- Ajuste `ALLOWED_HOSTS` no `settings.py`.
- Use variáveis de ambiente para senhas e segredos.
- Desative o DEBUG em produção.

---

## 16. Acesso ao sistema
- Acesse pelo navegador: http://<ip-ou-dominio>
- Faça login com o superusuário criado.

---

## 17. Dicas
- Para logs: `sudo journalctl -u crm_gunicorn -f`
- Para reiniciar Gunicorn: `sudo systemctl restart crm_gunicorn`
- Para reiniciar Nginx: `sudo systemctl restart nginx`

---

## 18. Referências
- [Documentação Django](https://docs.djangoproject.com/pt-br/4.2/howto/deployment/wsgi/gunicorn/)
- [Documentação Gunicorn](https://docs.gunicorn.org/en/stable/deploy.html)
- [Documentação Nginx](https://nginx.org/pt/docs/)

---

Pronto! Seu CRM Django estará rodando em produção no Debian Bookworm 🚀 