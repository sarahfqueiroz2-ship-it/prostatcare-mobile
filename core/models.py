from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

cpf_validator = RegexValidator(
    regex=r'^\d{11}$',
    message='Informe o CPF apenas com 11 números (sem pontos ou traço).'
)


class Dispositivo(models.Model):
    """Aparelho que faz a leitura do PSA. Equivale à entidade Dispositivo do ER."""
    identificador = models.CharField(
        max_length=20, unique=True,
        help_text='Código do aparelho, ex: A102'
    )
    localidade = models.CharField(max_length=120)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['identificador']

    def __str__(self):
        return f'{self.identificador} — {self.localidade}'


class Paciente(models.Model):
    """Equivale à entidade Paciente do ER. Ligado a um User para login/senha."""
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='paciente'
    )
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True, validators=[cpf_validator])
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=200, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    dispositivo = models.ForeignKey(
        Dispositivo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pacientes', help_text='Dispositivo normalmente usado por este paciente'
    )
     # ← ADICIONE ESTA PROPRIEDADE
    @property
    def id_display(self):
        """Retorna o ID formatado para exibição (ex: PAC-0001)"""
        return f"PAC-{str(self.id).zfill(4)}"
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.id_display})"


    class Meta:
        ordering = ['nome_completo']

    def __str__(self):
        return f'{self.nome_completo} ({self.cpf})'


class Funcionario(models.Model):
    """Equivale à entidade Funcionario (sob o Admin, no rascunho do ER)."""
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='funcionario'
    )
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True, validators=[cpf_validator])
    cargo = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    localidade = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['nome_completo']

    def __str__(self):
        return f'{self.nome_completo} — {self.cargo}'


class Leitura(models.Model):
    """
    Equivale à entidade Leitura do ER:
    Paciente (1,1) -- Rel -- (1,n) Leitura (1,n) -- Rel -- (1,1) Dispositivo
    """
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='leituras')
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.PROTECT, related_name='leituras')
    funcionario = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='leituras', help_text='Quem realizou/registrou a leitura'
    )
    data_hora = models.DateTimeField(auto_now_add=True)
    medicao = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text='Valor de PSA em ng/mL'
    )

    class Meta:
        ordering = ['-data_hora']

    def __str__(self):
        return f'{self.paciente.nome_completo} — {self.medicao} ng/mL em {self.data_hora:%d/%m/%Y}'

    @property
    def fora_da_referencia(self):
        # Faixa de referência comum para PSA total: até 4.0 ng/mL.
        return self.medicao > 4


class Classificacao(models.Model):
    """
    Classificação de risco a partir da cor lida na leitura (tira colorimétrica).
    Fica em tabela separada de propósito: facilita buscar todos os pacientes
    de risco alto com um único SELECT/filter, sem precisar varrer Leitura inteira.

    Observação: os valores de R/G/B e o nível de risco são definidos pelo
    sistema/algoritmo externo que faz a leitura de cor do dispositivo (fora
    do escopo deste projeto). Aqui só guardamos e exibimos o resultado.
    """
    RISCO_CHOICES = [
        ('baixo', 'Baixo'),
        ('moderado', 'Moderado'),
        ('alto', 'Alto'),
    ]

    leitura = models.OneToOneField(
        Leitura, on_delete=models.CASCADE, related_name='classificacao'
    )
    cor_r = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(255)],
        help_text='Componente vermelho da cor lida (0-255)'
    )
    cor_g = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(255)],
        help_text='Componente verde da cor lida (0-255)'
    )
    cor_b = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(255)],
        help_text='Componente azul da cor lida (0-255)'
    )
    nivel_risco = models.CharField(max_length=10, choices=RISCO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.leitura.paciente.nome_completo} — risco {self.get_nivel_risco_display()}'

    @property
    def cor_hex(self):
        return f'#{self.cor_r:02X}{self.cor_g:02X}{self.cor_b:02X}'


class Relatorio(models.Model):
    """Relatório emitido a partir de uma leitura, com observação e assinatura."""
    leitura = models.OneToOneField(Leitura, on_delete=models.CASCADE, related_name='relatorio')
    funcionario_responsavel = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True, related_name='relatorios'
    )
    observacao = models.TextField(blank=True)
    assinatura_nome = models.CharField(
        max_length=150, blank=True,
        help_text='Nome de quem assinou o relatório'
    )
    assinado_em = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Relatório de {self.leitura.paciente.nome_completo} ({self.criado_em:%d/%m/%Y})'

    @property
    def assinado(self):
        return bool(self.assinado_em)
