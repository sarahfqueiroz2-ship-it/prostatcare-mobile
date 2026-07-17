import base64
import io

from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from xhtml2pdf import pisa

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from .forms import LoginForm, PacienteForm, FuncionarioForm, RelatorioForm
from .models import Paciente, Leitura, Relatorio, Classificacao
from .permissions import get_role, roles_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:relatorio')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('core:relatorio')

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:login')


@roles_required('admin', 'funcionario')
def cadastro_view(request):
    role = get_role(request.user)
    tipo = request.POST.get('tipo', 'paciente')

    if tipo == 'funcionario' and role != 'admin':
        raise PermissionDenied('Somente o admin pode cadastrar funcionários.')

    paciente_form = PacienteForm()
    funcionario_form = FuncionarioForm()

    if request.method == 'POST':
        if tipo == 'paciente':
            paciente_form = PacienteForm(request.POST)
            if paciente_form.is_valid():
                paciente_form.save()
                messages.success(request, 'Paciente cadastrado com sucesso.')
                return redirect('core:cadastro')
        else:
            funcionario_form = FuncionarioForm(request.POST)
            if funcionario_form.is_valid():
                funcionario_form.save()
                messages.success(request, 'Funcionário cadastrado com sucesso.')
                return redirect('core:cadastro')

    return render(request, 'core/cadastro.html', {
        'paciente_form': paciente_form,
        'funcionario_form': funcionario_form,
        'tipo_ativo': tipo,
        'pode_cadastrar_funcionario': role == 'admin',
        'role': role,
    })


def _montar_grafico(leituras):
    """Calcula as coordenadas SVG do gráfico a partir das leituras (mais antiga -> mais nova)."""
    pontos = list(leituras.order_by('data_hora'))
    if not pontos:
        return None

    valores = [float(p.medicao) for p in pontos]
    minimo = 0
    maximo = max(max(valores), 4) * 1.2

    left, right, top, bottom = 60, 620, 10, 180
    n = len(pontos)
    coords = []
    for i, p in enumerate(pontos):
        x = left + (right - left) * (i / (n - 1) if n > 1 else 0.5)
        y = bottom - (bottom - top) * ((float(p.medicao) - minimo) / (maximo - minimo))
        classificacao = getattr(p, 'classificacao', None)
        coords.append({
            'x': f"{x:.1f}",
            'y': f"{y:.1f}",
            'quad_x': f"{x - 5:.1f}",
            'quad_y': f"{y - 18:.1f}",
            'cor_hex': classificacao.cor_hex if classificacao else None,
            'nivel_risco': classificacao.get_nivel_risco_display() if classificacao else None,
            'label': p.data_hora.strftime('%d/%m/%Y'),
            'valor': p.medicao,
            'alerta': p.fora_da_referencia,
        })

    ref_y_num = bottom - (bottom - top) * ((4 - minimo) / (maximo - minimo))
    ref_y = f"{ref_y_num:.1f}"
    polyline = ' '.join(f"{c['x']},{c['y']}" for c in coords)

    # marcações numéricas do eixo vertical (0 até o máximo, em 5 passos)
    num_marcacoes = 5
    marcacoes_y = []
    for i in range(num_marcacoes):
        valor_marcacao = maximo * i / (num_marcacoes - 1)
        y_pos = bottom - (bottom - top) * ((valor_marcacao - minimo) / (maximo - minimo))
        marcacoes_y.append({
            'valor': f"{valor_marcacao:.1f}",
            'y': f"{y_pos:.1f}",
            'label_y': f"{y_pos + 3:.1f}",
        })

    return {
        'pontos': coords,
        'polyline': polyline,
        'ref_y': ref_y,
        'ref_label_x': f"{right - 90:.1f}",
        'ref_label_y': f"{ref_y_num - 6:.1f}",
        'marcacoes_y': marcacoes_y,
        'eixo_y_label_x': f"{left - 8:.1f}",
        'eixo_x_label_y': f"{bottom + 16:.1f}",
        'titulo_y_pos': f"{top + 80:.1f}",
        'left': left,
        'right': right,
        'top': top,
        'bottom': bottom,
    }


@roles_required('admin', 'funcionario', 'paciente')
def relatorio_view(request):
    role = get_role(request.user)
    paciente = None
    resultados = []

    if role == 'paciente':
        paciente = request.user.paciente
    else:
        termo = request.GET.get('q', '').strip()
        paciente_id = request.GET.get('paciente_id')

        if paciente_id:
            paciente = get_object_or_404(Paciente, pk=paciente_id)
        elif termo:
            resultados = Paciente.objects.filter(
                Q(nome_completo__icontains=termo) |
                Q(cpf__icontains=termo) |
                Q(id__iexact=termo)
            )[:10]
            if resultados.count() == 1:
                paciente = resultados[0]

    leituras = Leitura.objects.filter(paciente=paciente).select_related('classificacao') if paciente else Leitura.objects.none()
    grafico = _montar_grafico(leituras)
    ultima_leitura = leituras.first()
    classificacao_atual = getattr(ultima_leitura, 'classificacao', None) if ultima_leitura else None

    relatorio_form = None
    if ultima_leitura and role in ('admin', 'funcionario'):
        relatorio_existente = getattr(ultima_leitura, 'relatorio', None)
        relatorio_form = RelatorioForm(instance=relatorio_existente)

        if request.method == 'POST' and 'emitir_relatorio' in request.POST:
            relatorio_form = RelatorioForm(request.POST, instance=relatorio_existente)
            if relatorio_form.is_valid():
                relatorio = relatorio_form.save(commit=False)
                relatorio.leitura = ultima_leitura
                relatorio.funcionario_responsavel = getattr(request.user, 'funcionario', None)
                if relatorio.assinatura_nome:
                    relatorio.assinado_em = timezone.now()
                relatorio.save()
                messages.success(request, 'Relatório salvo com sucesso.')
                return redirect('core:relatorio_pdf', paciente_id=paciente.id)

    return render(request, 'core/relatorio.html', {
        'role': role,
        'paciente': paciente,
        'resultados': resultados,
        'leituras': leituras,
        'ultima_leitura': ultima_leitura,
        'classificacao_atual': classificacao_atual,
        'grafico': grafico,
        'relatorio_form': relatorio_form,
        'relatorio_existente': getattr(ultima_leitura, 'relatorio', None) if ultima_leitura else None,
    })


def _gerar_grafico_imagem(leituras):
    """Desenha o gráfico de evolução do PSA como imagem PNG (em base64) para usar no PDF."""
    pontos = list(leituras.order_by('data_hora'))
    if not pontos:
        return None

    datas = [p.data_hora for p in pontos]
    valores = [float(p.medicao) for p in pontos]
    cores = ['#D9564C' if v > 4 else '#4FA3D9' for v in valores]

    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.plot(datas, valores, color='#4FA3D9', linewidth=2, zorder=2)
    ax.scatter(datas, valores, color=cores, zorder=3, s=28)
    ax.axhline(y=4.0, color='#D9564C', linestyle='--', linewidth=1)
    ax.text(datas[-1], 4.15, '4.0 ng/mL (ref.)', color='#D9564C', fontsize=8, ha='right')

    # quadradinho com a cor lida (RGB) acima de cada ponto, indicando o risco
    offset = (max(valores + [4]) * 1.2) * 0.06
    for data, valor, p in zip(datas, valores, pontos):
        classificacao = getattr(p, 'classificacao', None)
        if classificacao:
            ax.scatter(
                [data], [valor + offset],
                marker='s', s=70,
                color=classificacao.cor_hex,
                edgecolors='#1F2D3A', linewidths=0.6, zorder=4,
            )

    ax.set_ylabel('PSA (ng/mL)', fontsize=9, color='#1F2D3A')
    ax.set_ylim(bottom=0, top=max(valores + [4]) * 1.35)
    ax.grid(True, color='#EEF2F5', linewidth=0.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#DCE6EE')
    ax.spines['bottom'].set_color('#DCE6EE')
    ax.tick_params(colors='#6B7A87', labelsize=8)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    fig.autofmt_xdate(rotation=30)

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=160, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    imagem_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{imagem_base64}"


@roles_required('admin', 'funcionario', 'paciente')
def relatorio_pdf_view(request, paciente_id):
    role = get_role(request.user)
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    # paciente só pode baixar o próprio relatório
    if role == 'paciente' and paciente.usuario_id != request.user.id:
        raise PermissionDenied('Você só pode baixar o seu próprio relatório.')

    leituras = Leitura.objects.filter(paciente=paciente).select_related('classificacao').order_by('data_hora')
    ultima_leitura = Leitura.objects.filter(paciente=paciente).select_related('classificacao').order_by('-data_hora').first()
    relatorio = getattr(ultima_leitura, 'relatorio', None) if ultima_leitura else None
    classificacao_atual = getattr(ultima_leitura, 'classificacao', None) if ultima_leitura else None
    grafico_imagem = _gerar_grafico_imagem(leituras)

    html = render_to_string('core/relatorio_pdf.html', {
        'paciente': paciente,
        'leituras': leituras,
        'ultima_leitura': ultima_leitura,
        'relatorio': relatorio,
        'classificacao_atual': classificacao_atual,
        'grafico_imagem': grafico_imagem,
        'gerado_em': timezone.now(),
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{paciente.cpf}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF do relatório.', status=500)
    return response
