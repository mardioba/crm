from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Cliente, Atendimento, Contato, Veiculo, Modelo, Acessorio, Orcamento, Configuracao
from .forms import ClienteForm, AtendimentoForm, ContatoForm, OrcamentoForm, ConfiguracaoForm
from django.urls import reverse

@login_required
def dashboard(request):
    """Dashboard principal do sistema"""
    context = {
        'total_clientes': Cliente.objects.count(),
        'atendimentos_em_andamento': Atendimento.objects.filter(status='em_andamento').count(),
        'vendas_efetuadas': Atendimento.objects.filter(status='venda_efetuada').count(),
        'veiculos_disponiveis': Veiculo.objects.filter(disponivel=True).count(),
        'atendimentos_recentes': Atendimento.objects.select_related('cliente', 'vendedor').order_by('-data_abertura')[:5],
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def cliente_list(request):
    """Lista de clientes"""
    clientes = Cliente.objects.all().order_by('-data_cadastro')
    
    # Busca
    query = request.GET.get('q')
    if query:
        clientes = clientes.filter(
            Q(nome__icontains=query) | 
            Q(telefone__icontains=query) | 
            Q(email__icontains=query)
        )
    
    # Paginação
    paginator = Paginator(clientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'core/cliente_list.html', context)

@login_required
def cliente_create(request):
    """Criar novo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('core:cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm()
    
    context = {'form': form, 'title': 'Novo Cliente'}
    return render(request, 'core/cliente_form.html', context)

@login_required
def cliente_detail(request, pk):
    """Detalhes do cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    atendimentos = Atendimento.objects.filter(cliente=cliente).order_by('-data_abertura')
    
    context = {
        'cliente': cliente,
        'atendimentos': atendimentos,
    }
    return render(request, 'core/cliente_detail.html', context)

@login_required
def cliente_update(request, pk):
    """Editar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('core:cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    
    context = {'form': form, 'cliente': cliente, 'title': 'Editar Cliente'}
    return render(request, 'core/cliente_form.html', context)

@login_required
def atendimento_list(request):
    """Lista de atendimentos"""
    atendimentos = Atendimento.objects.select_related('cliente', 'vendedor', 'veiculo').order_by('-data_abertura')
    
    # Filtros
    status = request.GET.get('status')
    if status:
        atendimentos = atendimentos.filter(status=status)
    
    # Busca
    query = request.GET.get('q')
    if query:
        atendimentos = atendimentos.filter(
            Q(cliente__nome__icontains=query) | 
            Q(vendedor__username__icontains=query)
        )
    
    # Paginação
    paginator = Paginator(atendimentos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status': status,
        'query': query,
    }
    return render(request, 'core/atendimento_list.html', context)

@login_required
def atendimento_create(request):
    """Criar novo atendimento"""
    cliente_id = request.GET.get('cliente')
    cliente_instance = None
    
    if cliente_id:
        try:
            cliente_instance = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            pass
    
    if request.method == 'POST':
        data = request.POST.copy()
        if cliente_instance:
            data['cliente'] = request.POST.get('cliente', cliente_instance.pk)
        form = AtendimentoForm(data)
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.vendedor = request.user
            atendimento.save()
            messages.success(request, 'Atendimento criado com sucesso!')
            return redirect('core:atendimento_detail', pk=atendimento.pk)
    else:
        if cliente_instance:
            form = AtendimentoForm(initial={'cliente': cliente_instance})
            form.fields['cliente'].disabled = True
        else:
            form = AtendimentoForm()
    
    context = {
        'form': form, 
        'title': 'Novo Atendimento', 
        'cliente_instance': cliente_instance
    }
    return render(request, 'core/atendimento_form.html', context)

@login_required
def atendimento_detail(request, pk):
    """Detalhes do atendimento"""
    atendimento = get_object_or_404(Atendimento, pk=pk)
    contatos = Contato.objects.filter(atendimento=atendimento).order_by('-data_contato')
    
    if request.method == 'POST':
        contato_form = ContatoForm(request.POST)
        if contato_form.is_valid():
            contato = contato_form.save(commit=False)
            contato.atendimento = atendimento
            contato.save()
            messages.success(request, 'Contato registrado com sucesso!')
            return redirect('atendimento_detail', pk=atendimento.pk)
    else:
        contato_form = ContatoForm()
    
    context = {
        'atendimento': atendimento,
        'contatos': contatos,
        'contato_form': contato_form,
    }
    return render(request, 'core/atendimento_detail.html', context)

@login_required
def atendimento_update(request, pk):
    """Editar atendimento"""
    atendimento = get_object_or_404(Atendimento, pk=pk)
    if request.method == 'POST':
        form = AtendimentoForm(request.POST, instance=atendimento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atendimento atualizado com sucesso!')
            return redirect('atendimento_detail', pk=atendimento.pk)
    else:
        form = AtendimentoForm(instance=atendimento)
    
    context = {'form': form, 'atendimento': atendimento, 'title': 'Editar Atendimento'}
    return render(request, 'core/atendimento_form.html', context)

@login_required
def veiculo_list(request):
    """Lista de veículos"""
    veiculos = Veiculo.objects.select_related('modelo').all().order_by('modelo__marca', 'modelo__nome')
    
    # Filtros
    disponivel = request.GET.get('disponivel')
    if disponivel is not None:
        veiculos = veiculos.filter(disponivel=disponivel == 'true')
    
    # Busca
    query = request.GET.get('q')
    if query:
        veiculos = veiculos.filter(
            Q(modelo__nome__icontains=query) | 
            Q(modelo__marca__icontains=query) | 
            Q(placa__icontains=query)
        )
    
    # Paginação
    paginator = Paginator(veiculos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'disponivel': disponivel,
        'query': query,
    }
    return render(request, 'core/veiculo_list.html', context)

@login_required
def orcamento_create(request, atendimento_pk):
    """Criar orçamento para um atendimento"""
    atendimento = get_object_or_404(Atendimento, pk=atendimento_pk)
    
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            orcamento = form.save(commit=False)
            orcamento.atendimento = atendimento
            orcamento.save()
            form.save_m2m()  # Salvar acessórios
            
            # Marcar como impresso/enviado se solicitado
            if request.POST.get('impresso'):
                orcamento.impresso = True
            if request.POST.get('enviado_email'):
                orcamento.enviado_email = True
            orcamento.save()
            
            messages.success(request, 'Orçamento criado com sucesso!')
            return redirect('orcamento_detail', pk=orcamento.pk)
    else:
        form = OrcamentoForm()
    
    context = {
        'form': form,
        'atendimento': atendimento,
        'title': 'Novo Orçamento',
    }
    return render(request, 'core/orcamento_form.html', context)

@login_required
def orcamento_detail(request, pk):
    """Detalhes do orçamento"""
    orcamento = get_object_or_404(Orcamento, pk=pk)
    
    context = {
        'orcamento': orcamento,
    }
    return render(request, 'core/orcamento_detail.html', context)

@login_required
def veiculo_create(request):
    from .models import Veiculo, Modelo
    from django import forms
    modelo_id = request.GET.get('modelo')
    modelo_instance = None
    if modelo_id:
        try:
            modelo_instance = Modelo.objects.get(pk=modelo_id)
        except Modelo.DoesNotExist:
            pass
    class VeiculoForm(forms.ModelForm):
        class Meta:
            model = Veiculo
            fields = ['modelo', 'placa', 'cor', 'preco', 'disponivel']
            widgets = {
                'modelo': forms.Select(attrs={'class': 'form-control'}),
                'placa': forms.TextInput(attrs={'class': 'form-control'}),
                'cor': forms.TextInput(attrs={'class': 'form-control'}),
                'preco': forms.NumberInput(attrs={'class': 'form-control'}),
                'disponivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            }
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('core:veiculo_list')
    else:
        if modelo_instance:
            form = VeiculoForm(initial={'modelo': modelo_instance.pk})
        else:
            form = VeiculoForm()
    return render(request, 'core/veiculo_form.html', {'form': form, 'title': 'Novo Veículo'})

@login_required
def veiculo_update(request, pk):
    from .models import Veiculo
    from django import forms
    class VeiculoForm(forms.ModelForm):
        class Meta:
            model = Veiculo
            fields = ['modelo', 'placa', 'cor', 'preco', 'disponivel']
            widgets = {
                'modelo': forms.Select(attrs={'class': 'form-control'}),
                'placa': forms.TextInput(attrs={'class': 'form-control'}),
                'cor': forms.TextInput(attrs={'class': 'form-control'}),
                'preco': forms.NumberInput(attrs={'class': 'form-control'}),
                'disponivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            }
    veiculo = Veiculo.objects.get(pk=pk)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('core:veiculo_list')
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, 'core/veiculo_form.html', {'form': form, 'title': 'Editar Veículo'})

@login_required
def veiculo_delete(request, pk):
    from .models import Veiculo
    veiculo = Veiculo.objects.get(pk=pk)
    if request.method == 'POST':
        veiculo.delete()
        messages.success(request, 'Veículo excluído com sucesso!')
        return redirect('core:veiculo_list')
    return render(request, 'core/veiculo_confirm_delete.html', {'veiculo': veiculo})

@login_required
def modelo_list(request):
    from .models import Modelo
    query = request.GET.get('q', '')
    marca = request.GET.get('marca', '')
    ano = request.GET.get('ano', '')
    modelos = Modelo.objects.all()
    if query:
        modelos = modelos.filter(nome__icontains=query)
    if marca:
        modelos = modelos.filter(marca__icontains=marca)
    if ano:
        modelos = modelos.filter(ano=ano)
    modelos = modelos.order_by('marca', 'nome', 'ano')
    marcas = Modelo.objects.values_list('marca', flat=True).distinct().order_by('marca')
    anos = Modelo.objects.values_list('ano', flat=True).distinct().order_by('-ano')
    return render(request, 'core/modelo_list.html', {
        'modelos': modelos,
        'title': 'Modelos de Veículos',
        'query': query,
        'marca': marca,
        'ano': ano,
        'marcas': marcas,
        'anos': anos,
    })

@login_required
def modelo_create(request):
    from .models import Modelo
    from django import forms
    class ModeloForm(forms.ModelForm):
        class Meta:
            model = Modelo
            fields = ['nome', 'marca', 'ano']
            widgets = {
                'nome': forms.TextInput(attrs={'class': 'form-control'}),
                'marca': forms.TextInput(attrs={'class': 'form-control'}),
                'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            }
    if request.method == 'POST':
        form = ModeloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo cadastrado com sucesso!')
            return redirect('core:modelo_list')
    else:
        form = ModeloForm()
    return render(request, 'core/modelo_form.html', {'form': form, 'title': 'Novo Modelo'})

@login_required
def modelo_update(request, pk):
    from .models import Modelo
    from django import forms
    class ModeloForm(forms.ModelForm):
        class Meta:
            model = Modelo
            fields = ['nome', 'marca', 'ano']
            widgets = {
                'nome': forms.TextInput(attrs={'class': 'form-control'}),
                'marca': forms.TextInput(attrs={'class': 'form-control'}),
                'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            }
    modelo = Modelo.objects.get(pk=pk)
    if request.method == 'POST':
        form = ModeloForm(request.POST, instance=modelo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo atualizado com sucesso!')
            return redirect('core:modelo_list')
    else:
        form = ModeloForm(instance=modelo)
    return render(request, 'core/modelo_form.html', {'form': form, 'title': 'Editar Modelo'})

@login_required
def modelo_delete(request, pk):
    from .models import Modelo
    modelo = Modelo.objects.get(pk=pk)
    if request.method == 'POST':
        modelo.delete()
        messages.success(request, 'Modelo excluído com sucesso!')
        return redirect('core:modelo_list')
    return render(request, 'core/modelo_confirm_delete.html', {'modelo': modelo})

@user_passes_test(lambda u: u.is_superuser)
def configuracao_logo(request):
    config = Configuracao.objects.first()
    if not config:
        config = Configuracao.objects.create()
    if request.method == 'POST':
        form = ConfiguracaoForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Logo atualizada com sucesso!')
            return redirect('core:configuracao_logo')
    else:
        form = ConfiguracaoForm(instance=config)
    return render(request, 'core/configuracao_logo.html', {'form': form, 'config': config, 'title': 'Logo do Sistema'})

def get_logo_context(request):
    from .models import Configuracao
    return {'CONFIG_LOGO': Configuracao.objects.first()}
