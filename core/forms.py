from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import Paciente, Funcionario, Leitura, Relatorio, Dispositivo


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='CPF', widget=forms.TextInput(attrs={'placeholder': 'CPF'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))


class PacienteForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label='Senha de acesso', required=True)

    class Meta:
        model = Paciente
        fields = [
            'nome_completo', 'cpf', 'data_nascimento', 'telefone',
            'email', 'endereco', 'dispositivo',
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        paciente = super().save(commit=False)
        cpf = self.cleaned_data['cpf']
        senha = self.cleaned_data['senha']

        usuario, criado = User.objects.get_or_create(
            username=cpf,
            defaults={'first_name': self.cleaned_data['nome_completo']}
        )
        usuario.set_password(senha)
        usuario.first_name = self.cleaned_data['nome_completo']
        usuario.save()

        paciente.usuario = usuario
        if commit:
            paciente.save()
        return paciente


class FuncionarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label='Senha de acesso', required=True)

    class Meta:
        model = Funcionario
        fields = ['nome_completo', 'cpf', 'cargo', 'telefone', 'email', 'localidade']

    def save(self, commit=True):
        funcionario = super().save(commit=False)
        cpf = self.cleaned_data['cpf']
        senha = self.cleaned_data['senha']

        usuario, criado = User.objects.get_or_create(
            username=cpf,
            defaults={'first_name': self.cleaned_data['nome_completo']}
        )
        usuario.set_password(senha)
        usuario.first_name = self.cleaned_data['nome_completo']
        usuario.is_staff = False
        usuario.save()

        funcionario.usuario = usuario
        if commit:
            funcionario.save()
        return funcionario


class LeituraForm(forms.ModelForm):
    class Meta:
        model = Leitura
        fields = ['paciente', 'dispositivo', 'medicao']


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['observacao', 'assinatura_nome']
        widgets = {
            'observacao': forms.Textarea(attrs={
                'placeholder': 'Observações clínicas sobre o resultado…', 'rows': 4
            }),
            'assinatura_nome': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome completo para confirmar a assinatura'
            }),
        }
