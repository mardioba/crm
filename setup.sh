#!/bin/bash

echo "🚀 Configurando Sistema CRM - Django + MySQL"
echo "=============================================="

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale o Python 3.8+ primeiro."
    exit 1
fi

# Verificar se o MySQL está instalado
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL não encontrado. Instale o MySQL primeiro."
    echo "Ubuntu/Debian: sudo apt-get install mysql-server"
    echo "CentOS/RHEL: sudo yum install mysql-server"
    exit 1
fi

echo "✅ Python e MySQL encontrados"

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Configurar banco de dados MySQL
echo "🗄️ Configurando banco de dados MySQL..."
echo "Digite a senha do usuário root do MySQL:"
mysql -u root -p < setup_database.sql

# Executar migrações
echo "🔄 Executando migrações..."
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
echo "👤 Criando superusuário..."
echo "Digite as informações do superusuário:"
python manage.py createsuperuser

echo ""
echo "🎉 Instalação concluída com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Ative o ambiente virtual: source venv/bin/activate"
echo "2. Execute o servidor: python manage.py runserver"
echo "3. Acesse: http://localhost:8000"
echo ""
echo "🔧 Configurações do banco:"
echo "   - Banco: crmBD"
echo "   - Usuário: crmBD"
echo "   - Senha: crm123"
echo "" 