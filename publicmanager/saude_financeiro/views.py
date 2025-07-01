import tempfile
import weasyprint
from django.conf import settings
from django.utils import timezone
from collections import defaultdict
from datetime import datetime as dt
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from PyPDF2 import PdfReader, PdfWriter
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Sum, Q, Count
from django.db.models.functions import TruncDay

from publicmanager.comum.utils import CheckUserTypeMixin
from publicmanager.saude_cadastro.models import Profissional
from publicmanager.dashboard.utils import SaudeCheckHasPermission
from publicmanager.saude_atendimento.models import ProcedimentoAtendimento, AtendimentoMedico, ClassificacaoRisco

class RelatorioProcedimentosTemplateView(LoginRequiredMixin, CheckUserTypeMixin, SaudeCheckHasPermission, TemplateView):
    required_permissions = [settings.DESENVOLVEDOR, settings.ENFERMEIRO, settings.TECNICO_ENFERMAGEM]
    template_name = 'saude_financeiro/gerar_relatorio_procedimentos_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_date = dt.now()
        current_year = new_date.year

        context['month'] = new_date.strftime("%m")
        context['years'] = list(range(2024, current_year + 1))
        context['current_year'] = new_date.strftime("%Y")
        context['current_month'] = new_date.strftime("%m")
        context['unidade_saude'] = self.request.user.get_unidade_login().unidade

        context['crumbs'] = [
            {'label': 'Relatório Geral', 'url': "#", 'active': False},
        ]
        return context

class RelatorioConsolidadoDetalhadoPDFView(LoginRequiredMixin, CheckUserTypeMixin, View):
    def get(self, request, *args, **kwargs):
        data_atual = timezone.now()
        mes = int(request.GET.get('mes', 1))
        ano = int(request.GET.get('ano', data_atual.year))
        unidade_saude = self.request.user.get_unidade_login().unidade

        atendimentos = AtendimentoMedico.objects.filter(
            unidade_saude=unidade_saude,
            created_at__year=ano,
            created_at__month=mes,
        )

        procedimentos_atendimentos = ProcedimentoAtendimento.objects.filter(
            atendimento__unidade_saude=unidade_saude,
            created_at__year=ano,
            created_at__month=mes,
            situacao=ProcedimentoAtendimento.CONCLUIDO,
            tipo_solicitacao=ProcedimentoAtendimento.INTERNO,
        )

        lista_atendimentos = []
        atendimentos_dict = {}

        if atendimentos:
            for atendimento in atendimentos:
                codigo = '0301060096'
                nome = 'ATENDIMENTO MÉDICO'
                idade = atendimento.paciente.calcular_idade('numero')
                
                for profissional in atendimento.profissionais.all():
                    cbo = profissional.cbo

                    key = (codigo, cbo, idade)

                    if key in atendimentos_dict:
                        atendimentos_dict[key]['quantidade'] += 1
                    else:
                        atendimentos_dict[key] = {
                            'codigo': codigo,
                            'nome': nome,
                            'cbo': cbo if cbo else '-----',
                            'idade': idade,
                            'quantidade': 1
                        }

        lista_atendimentos = list(atendimentos_dict.values())

        lista_procedimentos = []
        procedimentos_dict = {}
        if procedimentos_atendimentos:
            procedimentos_agrupados = procedimentos_atendimentos.order_by('created_at', 'procedimento__codigo')

            for procedimento in procedimentos_agrupados:
                idade = procedimento.atendimento.paciente.calcular_idade('numero')
                cbo = procedimento.profissional_responsavel.cbo if procedimento.profissional_responsavel else '-----'
                codigo = procedimento.procedimento.codigo
                quantidade = procedimento.quantidade
                
                key = (codigo, cbo, idade)

                if key in procedimentos_dict:
                    procedimentos_dict[key]['quantidade'] += quantidade
                else:
                    procedimentos_dict[key] = {
                        'codigo': codigo,
                        'nome': procedimento.procedimento.nome,
                        'cbo': cbo if cbo else '-----',
                        'idade': idade,
                        'quantidade': quantidade,
                    }
            lista_procedimentos += list(procedimentos_dict.values())
        
        lista_total = lista_atendimentos + lista_procedimentos

        paginator = Paginator(lista_total, 18)

        paginated_data = []
        for i in range(1, paginator.num_pages + 1):
            page_objects = paginator.page(i).object_list

            total_geral = sum(item['quantidade'] for item in page_objects)

            paginated_data.append({'pagina': i, 'objects': page_objects, 'total_geral': total_geral})
        
        html_string = render(request, 'exportacao/relatorio_procedimentos_pdf.html', {
            'paginated_data': paginated_data,
            'data_atual': data_atual.strftime("%d/%m/%Y"),
            'mes_ano_selecionado': f'{mes}/{ano}',
            'unidade_saude': self.request.user.get_unidade_login().unidade,
        })

        html = weasyprint.HTML(string=html_string.content.decode(), base_url=request.build_absolute_uri('/media/'))
        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=pdf_file.name)

        pdf_reader = PdfReader(pdf_file.name)
        pdf_writer = PdfWriter()

        pdf_reader = PdfReader(pdf_file.name)
        pdf_writer = PdfWriter()

        num_pages = len(pdf_reader.pages)
        if num_pages > 1:
            for i in range(num_pages - 1):
                pdf_writer.add_page(pdf_reader.pages[i])

            output_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            with open(output_pdf.name, 'wb') as output_file:
                pdf_writer.write(output_file)

            with open(output_pdf.name, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="relatorio_procedimentos_{data_atual.strftime("%Y_%m_%d")}.pdf"'
                return response
        else:
            with open(pdf_file.name, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="relatorio_procedimentos_{data_atual.strftime("%Y_%m_%d")}.pdf"'
                return response

class RelatorioConsolidadoResumidoPDFView(LoginRequiredMixin, CheckUserTypeMixin, View):
    def formatar_codigo(self, codigo):
        codigo = str(codigo)
        if len(codigo) == 10:
            return f"{codigo[:2]}.{codigo[2:4]}.{codigo[4:6]}.{codigo[6:9]}-{codigo[9]}"
        if len(codigo) == 9:
            return f"{codigo[:2]}.{codigo[2:4]}.{codigo[4:6]}.{codigo[6:9]}"
        
        return codigo 

    def get(self, request, *args, **kwargs):
        data_atual = timezone.now()
        mes = int(request.GET.get('mes', 1))
        ano = int(request.GET.get('ano', data_atual.year))
        unidade_saude = self.request.user.get_unidade_login().unidade

        classificacoes_por_dia = defaultdict(lambda: defaultdict(int))
        procedimentos_por_dia = defaultdict(lambda: defaultdict(int))
        atendimentos_por_dia = defaultdict(int)

        atendimentos = AtendimentoMedico.objects.filter(
            unidade_saude=unidade_saude,
            created_at__year=ano,
            created_at__month=mes,
        )

        procedimentos_atendimentos = ProcedimentoAtendimento.objects.filter(
            atendimento__unidade_saude=unidade_saude,
            created_at__year=ano,
            created_at__month=mes,
            situacao=ProcedimentoAtendimento.CONCLUIDO,
            tipo_solicitacao=ProcedimentoAtendimento.INTERNO,
        )

        classificacoes_risco = ClassificacaoRisco.objects.filter(
            Q(status=ClassificacaoRisco.ATIVO),
            Q(boletim__unidade_saude=unidade_saude),
            Q(setor=ClassificacaoRisco.TRIAGEM),
            Q(created_at__year=ano),
            Q(created_at__month=mes),
            Q(
                Q(presao_arterial__isnull=False)|
                Q(temperatura__isnull=False) |
                Q(spo2__isnull=False)
            )
        )

        for classificacao in classificacoes_risco:
            dia = classificacao.created_at.day
            
            if classificacao.presao_arterial is not None:
                classificacoes_por_dia['presao_arterial'][dia] += 1
            if classificacao.temperatura is not None:
                classificacoes_por_dia['temperatura'][dia] += 1
            if classificacao.spo2 is not None:
                classificacoes_por_dia['spo2'][dia] += 1

        lista_classificacoes = []
        for tipo, dias in classificacoes_por_dia.items():
            lista_dias = [(dia, dias[dia]) for dia in range(1, 32)]
            total_dias = sum(dias.values())

            if tipo == 'presao_arterial':
                lista_classificacoes.append({'codigo': self.formatar_codigo('0301100039'), 'nome': 'AFERIÇÃO DE PRESSÃO ARTERIAL', 'dias': lista_dias, 'total': total_dias})
            elif tipo == 'temperatura':
                lista_classificacoes.append({'codigo': self.formatar_codigo('0301100250'), 'nome': 'AFERIÇÃO DE TEMPERATURA', 'dias': lista_dias, 'total': total_dias})
            elif tipo == 'spo2':
                lista_classificacoes.append({'codigo': self.formatar_codigo('0214010015'), 'nome': 'TESTE DE GLICEMIA CAPILAR', 'dias': lista_dias, 'total': total_dias})

        lista_procedimentos = []
        if procedimentos_atendimentos:
            procedimentos_agrupados = procedimentos_atendimentos.annotate(
                dia=TruncDay('created_at')
            ).values('dia', 'procedimento__codigo', 'procedimento__nome').annotate(
                total_quantidade=Sum('quantidade')
            ).order_by('dia', 'procedimento__codigo')

            for atendimento in procedimentos_agrupados:
                dia = atendimento['dia'].day
                codigo = atendimento['procedimento__codigo']
                nome = atendimento['procedimento__nome']
                procedimentos_por_dia[(codigo, nome)][dia] += atendimento['total_quantidade']

            for chave, dias in procedimentos_por_dia.items():
                codigo, nome = chave
                lista_dias = [(dia, dias[dia]) for dia in range(1, 32)]
                total_dias = sum(dias.values())
                lista_procedimentos.append({'codigo': self.formatar_codigo(codigo), 'nome': nome, 'dias': lista_dias, 'total': total_dias})

        lista_atendimentos = []
        if atendimentos:
            for atendimento in atendimentos:
                dia = atendimento.created_at.day
                atendimentos_por_dia[dia] += 1
            
            lista_dias = [(dia, atendimentos_por_dia[dia]) for dia in range(1, 32)]
            total_atendimentos = sum(atendimentos_por_dia.values())
            lista_atendimentos.append({'codigo': self.formatar_codigo('0301060096'), 'nome': 'ATENDIMENTO MÉDICO', 'dias': lista_dias, 'total': total_atendimentos})

        meses_em_portugues = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]

        # Combinar todas as listas
        lista_completa = lista_atendimentos + lista_classificacoes + lista_procedimentos

        html_index = render_to_string('exportacao/relatorio_consolidado_resumido_pdf.html', {
            'data_atual': data_atual,
            'lista_completa': lista_completa,
            'mes_atual_nome': meses_em_portugues[mes - 1],
            'ano_selecionado': ano,
            'range': range(1, 32),
            'unidade_saude': self.request.user.get_unidade_login().unidade,
            'data_impressao': data_atual.strftime("%d/%m/%Y %H:%m"),
        })
        
        html = weasyprint.HTML(string=html_index, base_url=request.build_absolute_uri('/media/'))
        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=pdf_file.name)

        with open(pdf_file.name, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="relatorio_procedimentos_{data_atual.strftime("%Y_%m_%d")}.pdf"'
            return response
    
class BoletimProducaoIndividualizados(LoginRequiredMixin, CheckUserTypeMixin, View):
    def get(self, request, *args, **kwargs):
        data_atual = timezone.now()
        mes = int(request.GET.get('mes', 1))
        ano = int(request.GET.get('ano', data_atual.year))
        mes_formatado = f"{mes:02}" 
        unidade_saude = self.request.user.get_unidade_login().unidade
        profissional_id = request.GET.get('profissional')

        atendimentos = AtendimentoMedico.objects.filter(unidade_saude=unidade_saude, created_at__year=ano, created_at__month=mes,)

        profissional = None
        if profissional_id:
            profissional = get_object_or_404(Profissional, pk=profissional_id)
            atendimentos = atendimentos.filter(profissionais=profissional)

        listagem = defaultdict(lambda: defaultdict(list))

        for atendimento in atendimentos:
            for profissional in atendimento.profissionais.all():
                procedimentos = ProcedimentoAtendimento.objects.filter(atendimento=atendimento, medico_solicitante=profissional)
                
                paciente_id = atendimento.paciente.id
                if paciente_id not in listagem[profissional]:
                    listagem[profissional][paciente_id] = {'paciente': atendimento.paciente, 'procedimentos': []}

                listagem[profissional][paciente_id]['procedimentos'].extend(procedimentos)

        resultado_final = [
            {
                'profissional': profissional,
                'pacientes': [
                    {
                        'paciente': paciente['paciente'],
                        'procedimentos': paciente['procedimentos']
                    }
                    for paciente in pacientes.values()
                ]
            }
            for profissional, pacientes in listagem.items()
        ]
        
        
        meses_em_portugues = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]

        html_index = render_to_string('exportacao/boletimproducao_dados_individualizados.html', {
            'data_atual': data_atual,
            'mes_atual_nome': meses_em_portugues[mes - 1],
            'ano_selecionado': ano,
            'mes_formatado': mes_formatado,
            'unidade_saude': self.request.user.get_unidade_login().unidade,
            'data_impressao': data_atual.strftime("%d/%m/%Y %H:%m"),
            'profissional': profissional,
            'atendimentos': atendimentos,
            'resultado_final': resultado_final,
        })
        
        html = weasyprint.HTML(string=html_index, base_url=request.build_absolute_uri('/media/'))
        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        html.write_pdf(target=pdf_file.name)

        with open(pdf_file.name, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="relatorio_procedimentos_{data_atual.strftime("%Y_%m_%d")}.pdf"'
            return response                 