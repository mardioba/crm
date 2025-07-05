from django import forms
from .models import Cliente, Atendimento, Contato, Orcamento, Veiculo, Acessorio, Configuracao

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'cpf', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['cliente', 'veiculo', 'status', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['tipo', 'descricao']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ['veiculo', 'acessorios', 'valor_veiculo', 'valor_acessorios']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'acessorios': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'valor_veiculo': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_acessorios': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar acessórios baseado no veículo selecionado
        if 'veiculo' in self.data:
            try:
                veiculo_id = int(self.data.get('veiculo'))
                veiculo = Veiculo.objects.get(id=veiculo_id)
                self.fields['acessorios'].queryset = Acessorio.objects.filter(modelo=veiculo.modelo)
            except (ValueError, Veiculo.DoesNotExist):
                self.fields['acessorios'].queryset = Acessorio.objects.none()
        elif self.instance.pk and self.instance.veiculo:
            self.fields['acessorios'].queryset = Acessorio.objects.filter(modelo=self.instance.veiculo.modelo)
        else:
            self.fields['acessorios'].queryset = Acessorio.objects.none()

class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracao
        fields = ['logo']
        widgets = {
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        } 