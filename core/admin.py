from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, Modelo, Veiculo, Acessorio, Atendimento, Contato, Orcamento, Configuracao

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'cargo', 'is_active')
    list_filter = ('cargo', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
        ('Informações Adicionais', {'fields': ('cargo', 'telefone')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'cargo', 'telefone'),
        }),
    )

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'data_cadastro')
    list_filter = ('data_cadastro',)
    search_fields = ('nome', 'telefone', 'email', 'cpf')
    readonly_fields = ('data_cadastro',)

@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'ano')
    list_filter = ('marca', 'ano')
    search_fields = ('nome', 'marca')

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'cor', 'preco', 'disponivel', 'placa')
    list_filter = ('disponivel', 'cor', 'modelo__marca')
    search_fields = ('placa', 'modelo__nome', 'modelo__marca')
    list_editable = ('disponivel', 'preco')

@admin.register(Acessorio)
class AcessorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modelo', 'preco')
    list_filter = ('modelo',)
    search_fields = ('nome', 'descricao')

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'vendedor', 'veiculo', 'status', 'data_abertura')
    list_filter = ('status', 'data_abertura', 'vendedor')
    search_fields = ('cliente__nome', 'vendedor__username')
    readonly_fields = ('data_abertura', 'data_fechamento')
    date_hierarchy = 'data_abertura'

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('atendimento', 'tipo', 'data_contato')
    list_filter = ('tipo', 'data_contato')
    search_fields = ('atendimento__cliente__nome', 'descricao')
    readonly_fields = ('data_contato',)

@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'atendimento', 'veiculo', 'valor_total', 'data_emissao', 'enviado_email', 'impresso')
    list_filter = ('data_emissao', 'enviado_email', 'impresso')
    search_fields = ('atendimento__cliente__nome', 'veiculo__modelo__nome')
    readonly_fields = ('data_emissao', 'valor_total')
    filter_horizontal = ('acessorios',)

@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('logo', 'atualizado_em')
