from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from PIL import Image
import os

class Usuario(AbstractUser):
    """Modelo para usuários do sistema com permissões especiais"""
    CARGO_CHOICES = [
        ('vendedor', 'Vendedor'),
        ('gerente', 'Gerente'),
        ('admin', 'Administrador'),
    ]
    
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='vendedor')
    telefone = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class Cliente(models.Model):
    """Modelo para clientes da empresa"""
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True, 
                          validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'CPF deve estar no formato XXX.XXX.XXX-XX')])
    endereco = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return self.nome

class Modelo(models.Model):
    """Modelo para modelos de veículos"""
    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    ano = models.IntegerField()
    
    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
    
    def __str__(self):
        return f"{self.marca} {self.nome} {self.ano}"

class Veiculo(models.Model):
    """Modelo para veículos em estoque"""
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    placa = models.CharField(max_length=8, blank=True, null=True)
    cor = models.CharField(max_length=30)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
    
    def __str__(self):
        return f"{self.modelo} - {self.cor}"

class Acessorio(models.Model):
    """Modelo para acessórios disponíveis por modelo de veículo"""
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name='acessorios')
    
    class Meta:
        verbose_name = 'Acessório'
        verbose_name_plural = 'Acessórios'
    
    def __str__(self):
        return self.nome

class Atendimento(models.Model):
    """Modelo para atendimentos realizados pelos vendedores"""
    STATUS_CHOICES = [
        ('em_andamento', 'Em Andamento'),
        ('venda_efetuada', 'Venda Efetuada'),
        ('venda_perdida', 'Venda Perdida'),
        ('cancelado', 'Cancelado'),
    ]
    
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_andamento')
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'
    
    def __str__(self):
        return f"Atendimento {self.id} - {self.cliente.nome}"

class Contato(models.Model):
    """Modelo para contatos realizados entre vendedor e cliente"""
    TIPO_CHOICES = [
        ('telefone', 'Telefone'),
        ('email', 'E-mail'),
        ('whatsapp', 'WhatsApp'),
        ('pessoal', 'Pessoal'),
    ]
    
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE, related_name='contatos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_contato = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    
    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
    
    def __str__(self):
        return f"Contato {self.tipo} - {self.atendimento.cliente.nome}"

class Orcamento(models.Model):
    """Modelo para orçamentos emitidos"""
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    acessorios = models.ManyToManyField(Acessorio, blank=True)
    valor_veiculo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_acessorios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateTimeField(auto_now_add=True)
    enviado_email = models.BooleanField(default=False)
    impresso = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
    
    def __str__(self):
        return f"Orçamento {self.id} - {self.atendimento.cliente.nome}"
    
    def save(self, *args, **kwargs):
        # Calcula o valor total automaticamente
        self.valor_total = self.valor_veiculo + self.valor_acessorios
        super().save(*args, **kwargs)

class Configuracao(models.Model):
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name='Logo do Sistema')
    atualizado_em = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.logo:
            logo_path = self.logo.path
            img = Image.open(logo_path)
            img = img.convert('RGBA') if img.mode != 'RGBA' else img
            img = img.resize((180, 40), Image.LANCZOS)
            img.save(logo_path)

    def __str__(self):
        return 'Configuração do Sistema'

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
