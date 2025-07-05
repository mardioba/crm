from django.urls import path
from . import views
from django.shortcuts import render

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    
    # Atendimentos
    path('atendimentos/', views.atendimento_list, name='atendimento_list'),
    path('atendimentos/novo/', views.atendimento_create, name='atendimento_create'),
    path('atendimentos/<int:pk>/', views.atendimento_detail, name='atendimento_detail'),
    path('atendimentos/<int:pk>/editar/', views.atendimento_update, name='atendimento_update'),
    
    # Veículos
    path('veiculos/', views.veiculo_list, name='veiculo_list'),
    path('veiculos/novo/', views.veiculo_create, name='veiculo_create'),
    path('veiculos/<int:pk>/editar/', views.veiculo_update, name='veiculo_update'),
    path('veiculos/<int:pk>/excluir/', views.veiculo_delete, name='veiculo_delete'),
    
    # Orçamentos
    path('atendimentos/<int:atendimento_pk>/orcamento/', views.orcamento_create, name='orcamento_create'),
    path('orcamentos/<int:pk>/', views.orcamento_detail, name='orcamento_detail'),
    
    # Modelos
    path('modelos/', views.modelo_list, name='modelo_list'),
    path('modelos/novo/', views.modelo_create, name='modelo_create'),
    path('modelos/<int:pk>/editar/', views.modelo_update, name='modelo_update'),
    path('modelos/<int:pk>/excluir/', views.modelo_delete, name='modelo_delete'),
    
    # Configuração do sistema
    path('configuracao/logo/', views.configuracao_logo, name='configuracao_logo'),
    
    # Ajuda
    path('ajuda/', lambda request: render(request, 'core/ajuda.html'), name='ajuda'),
] 