from django.contrib import admin

from .models import Dispositivo, Paciente, Funcionario, Leitura, Relatorio, Classificacao


@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'localidade', 'ativo')
    search_fields = ('identificador', 'localidade')


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'email', 'telefone', 'dispositivo')
    search_fields = ('nome_completo', 'cpf')


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'cargo', 'localidade')
    search_fields = ('nome_completo', 'cpf')


class ClassificacaoInline(admin.StackedInline):
    model = Classificacao
    extra = 0


@admin.register(Leitura)
class LeituraAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'dispositivo', 'funcionario', 'medicao', 'data_hora')
    list_filter = ('dispositivo',)
    search_fields = ('paciente__nome_completo', 'paciente__cpf')
    inlines = [ClassificacaoInline]


@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('leitura', 'funcionario_responsavel', 'assinado', 'criado_em')


@admin.register(Classificacao)
class ClassificacaoAdmin(admin.ModelAdmin):
    # list_display já deixa fácil olhar de relance quem está em risco alto;
    # o list_filter por nivel_risco é o "SELECT" fácil que o professor pediu.
    list_display = ('leitura', 'nivel_risco', 'cor_hex', 'criado_em')
    list_filter = ('nivel_risco',)
    search_fields = ('leitura__paciente__nome_completo', 'leitura__paciente__cpf')
