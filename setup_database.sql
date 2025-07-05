-- Script para configurar o banco de dados MySQL do Sistema CRM
-- Execute este script como usuário root do MySQL

-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS crmBD 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Criar o usuário
CREATE USER IF NOT EXISTS 'crmBD'@'localhost' IDENTIFIED BY 'crm123';

-- Conceder privilégios ao usuário
GRANT ALL PRIVILEGES ON crmBD.* TO 'crmBD'@'localhost';

-- Aplicar as mudanças
FLUSH PRIVILEGES;

-- Verificar se foi criado corretamente
SHOW DATABASES LIKE 'crmBD';
SELECT User, Host FROM mysql.user WHERE User = 'crmBD'; 