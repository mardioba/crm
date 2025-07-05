# CRM PARA CONCESSIONÁRIAS DE VEÍCULOS = tecnologia: Django + Bootstrap

Sistema de Customer Relationship Management (CRM) desenvolvido em Django com interface Bootstrap 5, focado no gerenciamento de vendas de veículos.

## 🚀 Funcionalidades

### Requisitos Funcionais Implementados

- **RF1**: Cadastro de usuários com permissões de acesso
- **RF2**: Registro de atendimentos com status (venda efetuada/perdida)
- **RF3**: Registro de contatos entre vendedor e cliente
- **RF4**: Cadastro de acessórios por modelo de veículo
- **RF5**: Emissão de orçamentos (impresso/email)
- **RF6**: Abertura de atendimentos para novos clientes

### Módulos Principais

- **Dashboard**: Visão geral com estatísticas e atendimentos recentes
- **Clientes**: Cadastro e gerenciamento de clientes
- **Atendimentos**: Controle de atendimentos e contatos
- **Veículos**: Listagem de veículos disponíveis
- **Orçamentos**: Criação e visualização de orçamentos
- **Administração**: Interface administrativa completa

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 4.2.23
- **Frontend**: Bootstrap 5.3.0 (via CDN)
- **Banco de Dados**: MySQL
- **Autenticação**: Sistema de usuários customizado
- **Ícones**: Bootstrap Icons

## 📋 Pré-requisitos

- Python 3.8+
- MySQL
- pip

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd crm
```

### 2. Crie e ative o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados MySQL

#### 4.1. Crie o banco de dados e usuário no MySQL:
```sql
CREATE DATABASE crmBD CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'crmBD'@'localhost' IDENTIFIED BY 'crm123';
GRANT ALL PRIVILEGES ON crmBD.* TO 'crmBD'@'localhost';
FLUSH PRIVILEGES;
```

#### 4.2. As configurações já estão definidas no arquivo `crm/settings.py`:
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

### 5. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 7. Execute o servidor
```bash
python manage.py runserver
```

## 🚀 Como Usar

### Acesso ao Sistema

1. Acesse `http://localhost:8000`
2. Faça login com as credenciais do superusuário
3. Você será redirecionado para o dashboard

### Fluxo de Trabalho

1. **Cadastrar Cliente**: Acesse "Clientes" → "Novo Cliente"
2. **Criar Atendimento**: Acesse "Atendimentos" → "Novo Atendimento"
3. **Registrar Contatos**: Na página do atendimento, adicione contatos
4. **Criar Orçamento**: No atendimento, clique em "Criar Orçamento"
5. **Finalizar Venda**: Atualize o status do atendimento

### Permissões de Usuário

- **Vendedor**: Pode criar atendimentos e orçamentos
- **Gerente**: Acesso completo ao sistema
- **Administrador**: Acesso total incluindo admin do Django

## 📁 Estrutura do Projeto

```
crm/
├── crm/                 # Configurações do projeto
│   ├── settings.py     # Configurações principais
│   ├── urls.py         # URLs principais
│   └── ...
├── core/               # App principal
│   ├── models.py       # Modelos de dados
│   ├── views.py        # Views do sistema
│   ├── forms.py        # Formulários
│   ├── admin.py        # Interface administrativa
│   └── urls.py         # URLs do app
├── templates/          # Templates HTML
│   ├── base.html       # Template base
│   ├── core/           # Templates do app core
│   └── registration/   # Templates de autenticação
└── manage.py           # Script de gerenciamento Django
```

## 🎨 Interface

O sistema utiliza Bootstrap 5 para uma interface moderna e responsiva:

- **Sidebar**: Navegação principal
- **Cards**: Exibição de estatísticas
- **Tabelas**: Listagem de dados
- **Formulários**: Cadastro e edição
- **Alertas**: Mensagens de feedback

## 🔒 Segurança

- Autenticação obrigatória para todas as páginas
- Sistema de permissões por cargo
- Validação de formulários
- Proteção CSRF

## 📊 Funcionalidades Avançadas

### Dashboard
- Estatísticas em tempo real
- Atendimentos recentes
- Ações rápidas

### Busca e Filtros
- Busca por nome, telefone, email
- Filtros por status
- Paginação automática

### Orçamentos
- Cálculo automático de valores
- Seleção de acessórios por modelo
- Opções de impressão e email

## 🐛 Solução de Problemas

### Erro de Conexão com MySQL
- Verifique se o MySQL está rodando: `sudo systemctl status mysql`
- Confirme as credenciais no settings.py
- Teste a conexão: `mysql -u crmBD -p crmBD`

### Erro de Migrações
```bash
python manage.py makemigrations --empty core
python manage.py makemigrations
python manage.py migrate
```

### Erro de Templates
- Verifique se o diretório `templates/` está configurado
- Confirme se os templates estão no local correto

### Erro de Instalação do mysqlclient
Se houver problemas com a instalação do mysqlclient:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# CentOS/RHEL
sudo yum install python3-devel mysql-devel gcc

# macOS
brew install mysql-connector-c
```

## 📝 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório. 