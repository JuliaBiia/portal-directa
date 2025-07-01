import io
import datetime
from uuid import UUID
from urllib.parse import urlencode

from django.urls import reverse
from django.contrib import messages
from django.http import FileResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import View, CreateView, UpdateView, DeleteView, ListView, DetailView

from pytz import timezone
from functools import partial
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus.frames import Frame
from reportlab.platypus.paragraph import Paragraph, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Image, Table, TableStyle

from publicmanager.autenticacao.models import Usuario
from publicmanager.saude_cadastro.models import Profissional
from publicmanager.saude_atendimento.models import (
    BoletimPaciente, Paciente, AgendamentoConsultorio, PreAtendimentoMedico, HorarioMedico, BloqueioAgenda, Feriado
)
from publicmanager.saude_atendimento.forms import (
    PreAtendimentoMedicoCreateForm, PreAtendimentoMedicoUpdateForm, HorarioMedicoForm, BuscarAgendamentosForm,
    AgendaMedicaForm, AgendaMedicaFiltroForm, FeriadoForm, BloqueioAgendaForm, RelatorioAgendamentoForm, FeriadoFilterForm,
    BloqueioAgendaFilterForm
)

class HorarioMedicoView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = HorarioMedico
    template_name = 'saude_atendimento/horario_medico.html'
    form_class = HorarioMedicoForm
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'
    paginate_by=10

    def get(self, request, *args, **kwargs):
        form = HorarioMedicoForm()
        horariosmedico = HorarioMedico.objects.all().order_by("medico_horariomedico__nome_profissional", "dia_semana_horariomedico", "hora_inicial_horariomedico")

        context = {}

        context['form'] = form

        context['horariosmedico'] = horariosmedico

        context['crumbs'] = [
            {'label': 'Listagem de Horários Médicos', 'url': reverse('saude_atendimento:horario_medico_view')}
        ]
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)

        if forms.is_valid():
            medico_id = request.POST.get('medico_horariomedico')

            medico = Profissional.objects.get(id=medico_id)
        
            horario_medico = forms.save(commit=False)
            horario_medico.medico_horariomedico = medico
            horario_medico.dia_semana_horariomedico
            horario_medico.save()

            forms = HorarioMedicoForm()

        horariosmedico = HorarioMedico.objects.all()

        context = {'form': forms, 'horariosmedico': horariosmedico}
        return render(request, self.template_name, context)

class HorarioMedicoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = HorarioMedico
    template_name = 'saude_atendimento/horario_medico_create_update_form.html'
    form_class = HorarioMedicoForm
    success_url = reverse_lazy('saude_atendimento:horario_medico_view')
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['crumbs'] = [
            {'label': 'Listagem de Horários Médicos', 'url': reverse('saude_atendimento:horario_medico_view')},
            {'label': 'Editar dados do Horário', 'url': reverse('saude_atendimento:horario_medico_update', kwargs={'pk': self.object.pk})}
        ]

        return context

    def form_valid(self, form):
        medico_id = self.request.POST.get('medico_horariomedico')
        medico = Profissional.objects.get(id=medico_id)

        horario_medico = form.save(commit=False)
        horario_medico.medico_horariomedico = medico
        horario_medico.save()

        return super().form_valid(form)

class HorarioMedicoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = HorarioMedico
    template_name = "saude_atendimento/horario_medico.html"
    success_url = reverse_lazy('saude_atendimento:horario_medico_view')
    success_message = 'Seus dados foram deletados conforme solicitado.'



class MinhaAgendaMedicaView(LoginRequiredMixin, ListView):
    model = AgendamentoConsultorio
    template_name = 'saude_atendimento/minhaagendamedica.html'
    context_object_name = 'agendamentos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = Usuario.objects.get(id=self.request.user.id)

        business_hours = []
        lista_agendamentos = []

        try:
            medico = Profissional.objects.get(user__id=user.id)

            horarios_medico_selecionado = HorarioMedico.objects.filter(medico_horariomedico__id__exact=medico.id)

            for horario in horarios_medico_selecionado:
                dia = horario.dia_semana_horariomedico
                hora_inicial = horario.hora_inicial_horariomedico
                hora_final = horario.hora_final_horariomedico

                business_hours.append({
                    'daysOfWeek': [dia],
                    'startTime': hora_inicial.strftime('%H:%M'),
                    'endTime': hora_final.strftime('%H:%M'),
                })

            agendamentos = AgendamentoConsultorio.objects.filter(
                    medico__id=medico.id)

            for agendamento in agendamentos:
                consulta_medico_id = agendamento.medico.id

                consulta_medico_user_id = agendamento.medico.user_id
                consulta_medico_user_id_str = str(consulta_medico_user_id)

                cor_marcacao = "#"+hex(int(consulta_medico_user_id_str+(7-len(consulta_medico_user_id_str))*"0"))[2:]

                lista_agendamentos.append(
                    {
                        "id": agendamento.id,
                        "title": agendamento.nome_paciente,
                        "start": agendamento.data_atendimento.strftime("%Y-%m-%d")+"T"+agendamento.hora_inicio_atendimento.strftime("%H:%M"),
                        "end": agendamento.data_atendimento.strftime("%Y-%m-%d")+"T"+agendamento.hora_termino_atendimento.strftime("%H:%M"),
                        "backgroundColor": cor_marcacao,
                        "borderColor": cor_marcacao,
                    }
                )

        except Profissional.DoesNotExist:
            pass
        
        
        context["consultas"] = lista_agendamentos
        context["business_hours"] = business_hours

        context['crumbs'] = [
            {'label': 'Minha Agenda Médica', 'url': reverse('saude_atendimento:minha_agenda_medica')}
        ]

        return context


class AgendaMedicaView(LoginRequiredMixin, View):
    template_name = "saude_atendimento/agendamedica.html"
    form_class = AgendaMedicaForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()

        agenda_medica_url = reverse('saude_atendimento:agenda_medica_view')

        medico_id = request.GET.get('medico')

        agenda_medica_filtro_form = AgendaMedicaFiltroForm()
        agenda_medica_filtro_form.fields['medico_filtragem_agendamentos'].queryset = Profissional.objects.filter(tipo_profissional=Profissional.MEDICO).order_by("nome_profissional")
        
        feriado_form = FeriadoForm()
        feriado_filter_form = FeriadoFilterForm()

        bloqueio_agenda_form = BloqueioAgendaForm(instance=None)
        bloqueio_agenda_filter_form = BloqueioAgendaFilterForm()

        editar_feriado = [0]
        editar_bloqueio_agenda = [0]

        if 'alvoupdate' in kwargs.keys():
            if kwargs["alvoupdate"] == "feriado":
                feriado_update = Feriado.objects.get(id=kwargs["id"])
                feriado_form = FeriadoForm(instance=feriado_update)

                editar_feriado = [1, kwargs["id"]]
            elif kwargs["alvoupdate"] == "bloqueioagenda":
                bloqueio_agenda_update = BloqueioAgenda.objects.get(id=kwargs["id"])
                bloqueio_agenda_form = BloqueioAgendaForm(instance=bloqueio_agenda_update)

                editar_bloqueio_agenda = [1, kwargs["id"]]

                medico_id = bloqueio_agenda_update.medico.id
        elif 'medico_id' in kwargs.keys():
            medico_id = kwargs['medico_id']

        relatorio_agendamento_form = RelatorioAgendamentoForm()

        feriados = Feriado.objects.all()
        bloqueios_agenda = BloqueioAgenda.objects.all()
        agendamentos = AgendamentoConsultorio.objects.all()

        um_medico_foi_selecionado = 0

        business_hours_estrutura_fullcalendar = []
        business_hours = {}
        
        if medico_id:
            medico = Profissional.objects.get(id=medico_id)

            if medico.tipo_profissional == Profissional.MEDICO:
                agenda_medica_url = reverse('saude_atendimento:agenda_medica_medico_view', kwargs={'medico_id': medico.id})

                forms = AgendaMedicaForm(initial={'agendado_por': request.user}, instance=medico)
                
                agenda_medica_filtro_form.fields['medico_filtragem_agendamentos'].initial = medico.id
                forms.fields['paciente'].queryset = Paciente.objects.all().order_by('nome_paciente')
                relatorio_agendamento_form['medico_relatorio'].initial = medico.id

                if not(editar_bloqueio_agenda[0]):
                    bloqueio_agenda_form = BloqueioAgendaForm(instance=medico)

                agendamentos = AgendamentoConsultorio.objects.filter(
                    medico__id=medico.id)
                bloqueios_agenda = BloqueioAgenda.objects.filter(
                    medico_bloqueio_agenda__id=medico.id)
                
                um_medico_foi_selecionado = 1

                horarios_medico_selecionado = HorarioMedico.objects.filter(medico_horariomedico__id__exact=medico.id)

                for horario in horarios_medico_selecionado:
                    dia = horario.dia_semana_horariomedico
                    hora_inicial = horario.hora_inicial_horariomedico
                    hora_final = horario.hora_final_horariomedico

                    business_hours_estrutura_fullcalendar.append({
                        'daysOfWeek': [dia],
                        'startTime': hora_inicial.strftime('%H:%M'),
                        'endTime': hora_final.strftime('%H:%M'),
                    })

                    if dia in business_hours:
                        business_hours[dia].append([hora_inicial.strftime('%H:%M'), hora_final.strftime('%H:%M')])
                    else:
                        business_hours[dia] = [[hora_inicial.strftime('%H:%M'), hora_final.strftime('%H:%M')]]
            else:
                medico_id = ""

                messages.error(request, 'Não é possível selecionar um profissional que não seja um médico')

        if request.GET.get("operacao_dados_feriado") == "pesquisar_feriado":
            nome_feriado = request.GET.get("nome_feriado")

            if nome_feriado:
                feriados = Feriado.objects.filter(
                nome_feriado__icontains=nome_feriado)
        elif request.GET.get("operacao_dados_bloqueio_agenda") == "pesquisar_bloqueio_agenda":
            motivo_bloqueio_agenda = request.GET.get("motivo")

            if motivo_bloqueio_agenda:
                bloqueios_agenda = BloqueioAgenda.objects.filter(medico__id__exact=medico.id,
                motivo__icontains=motivo_bloqueio_agenda)

        lista_agendamentos = []

        for agendamento in agendamentos:
            consulta_medico_user_id = agendamento.medico.user_id
            consulta_medico_user_id_str = str(consulta_medico_user_id)

            cor_marcacao = "#"+hex(int(consulta_medico_user_id_str+(7-len(consulta_medico_user_id_str))*"0"))[2:]

            tipo_atendimento_abreviatura = ""
            if agendamento.tipo_atendimento == 0:
                tipo_atendimento_abreviatura = "(1°) "
            elif agendamento.tipo_atendimento == 1:
                tipo_atendimento_abreviatura = "(EE) "
            elif agendamento.tipo_atendimento == 2:
                tipo_atendimento_abreviatura = "(RT) "

            lista_agendamentos.append(
                {
                    "id": agendamento.id,
                    "title": tipo_atendimento_abreviatura+agendamento.nome_paciente,
                    "start": agendamento.data_atendimento.strftime("%Y-%m-%d")+"T"+agendamento.hora_inicio_atendimento.strftime("%H:%M"),
                    "end": agendamento.data_atendimento.strftime("%Y-%m-%d")+"T"+agendamento.hora_termino_atendimento.strftime("%H:%M"),
                    "backgroundColor": cor_marcacao,
                    "borderColor": cor_marcacao,
                }
            )
    
        matriz_feriados = []

        for feriado in feriados:
            matriz_feriados.append([
                [feriado.data_inicial.year, feriado.data_inicial.month, feriado.data_inicial.day], [feriado.data_final.year, feriado.data_final.month, feriado.data_final.day]
            ])
        
        matriz_bloqueios_agenda = []

        for bloqueio_agenda in bloqueios_agenda:
            quantidade_de_dias_bloqueados = abs((bloqueio_agenda.data_inicial - bloqueio_agenda.data_final).days)+1

            matriz_bloqueios_agenda.append([
                [bloqueio_agenda.data_inicial.year, bloqueio_agenda.data_inicial.month, bloqueio_agenda.data_inicial.day],
                [bloqueio_agenda.data_final.year, bloqueio_agenda.data_final.month, bloqueio_agenda.data_final.day],
                quantidade_de_dias_bloqueados
            ])
        
        indices_matriz_bloqueios_agenda = list(range(0, len(matriz_bloqueios_agenda)))
        
        context = {}

        context['crumbs'] = [
            {'label': 'Agenda Médica', 'url': agenda_medica_url}
        ]

        context['form'] = forms
        context["agenda_medica_filtro_form"] = agenda_medica_filtro_form
        context["consultas"] = lista_agendamentos
        context["business_hours_estrutura_fullcalendar"] = business_hours_estrutura_fullcalendar
        context["business_hours"] = business_hours
        context["feriado_form"] = feriado_form
        context["feriado_filter_form"] = feriado_filter_form
        context["editar_feriado"] = editar_feriado
        context["editar_bloqueio_agenda"] = editar_bloqueio_agenda
        context["bloqueio_agenda_form"] = bloqueio_agenda_form
        context["bloqueio_agenda_filter_form"] = bloqueio_agenda_filter_form
        context["relatorio_agendamento_form"] = relatorio_agendamento_form
        context["feriados"] = feriados
        context["bloqueios_agenda"] = bloqueios_agenda
        context["matriz_feriados"] = matriz_feriados
        context["matriz_bloqueios_agenda"] = matriz_bloqueios_agenda
        context["indices_matriz_bloqueios_agenda"] = indices_matriz_bloqueios_agenda
        context["um_medico_foi_selecionado"] = um_medico_foi_selecionado
        context["medico_id"] = medico_id
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        medico_id = request.POST.get('medico')

        redirect_url = reverse('saude_atendimento:agenda_medica_medico_view', kwargs={'medico_id': medico_id})
        return redirect(redirect_url)

class AgendamentoConsultorioCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AgendamentoConsultorio
    template_name = 'saude_atendimento/agendamedica.html'
    form_class = AgendaMedicaForm
    success_url = reverse_lazy('saude_atendimento:agenda_medica_view')
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def form_valid(self, form):
        form.instance.unidade_saude = self.request.user.profissional_set.first().unidadelogin.unidade
        return super().form_valid(form)

class AgendamentoConsultorioDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AgendamentoConsultorio
    template_name = "saude_atendimento/buscar_agendamentos_consultorio.html"
    success_url = reverse_lazy('saude_atendimento:buscar_agendamentos_view')

def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.topMargin)
    # content.drawOn(canvas, 30, doc.height + doc.bottomMargin + doc.topMargin - h)
    content.drawOn(canvas, 27, 485)
    canvas.restoreState()
def footer(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.bottomMargin) # h = 18
    # content.drawOn(canvas, 30, h)
    content.drawOn(canvas, 30, 25)
    canvas.restoreState()
def header_and_footer(canvas, doc, header_content, footer_content):
    header(canvas, doc, header_content)
    footer(canvas, doc, footer_content)

def pdf_relatorio_agendamento(request):
    data_inicial_relatorio = request.GET.get("data_inicial_relatorio")
    data_final_relatorio = request.GET.get("data_final_relatorio")
    paciente_relatorio = request.GET.get("paciente_relatorio")
    cpf_paciente_relatorio = request.GET.get("cpf_paciente_relatorio")
    medico_relatorio = request.GET.get("medico_relatorio")



    agendamentos = AgendamentoConsultorio.objects.all()

    if data_inicial_relatorio:
        data_inicial_relatorio = data_inicial_relatorio.split("/")

        agendamentos = agendamentos.filter(data_atendimento__gte=datetime.date(int(data_inicial_relatorio[2]), int(data_inicial_relatorio[1]), int(data_inicial_relatorio[0])))
    if data_final_relatorio:
        data_final_relatorio = data_final_relatorio.split("/")

        agendamentos = agendamentos.filter(data_atendimento__lte=datetime.date(int(data_final_relatorio[2]), int(data_final_relatorio[1]), int(data_final_relatorio[0])))
    if paciente_relatorio:
        agendamentos = agendamentos.filter(nome_paciente__exact=paciente_relatorio)
    if cpf_paciente_relatorio:
        agendamentos = agendamentos.filter(cpf_paciente__exact=cpf_paciente_relatorio)
    if medico_relatorio:
        agendamentos = agendamentos.filter(medico__id__exact=UUID(medico_relatorio))

    agendamentos = agendamentos.order_by('data_atendimento','hora_inicio_atendimento')

    row_heights = [0.7*inch, 0.2*inch]

    data = [["","","","",""]]

    data.append(["Paciente", "CPF", "Telefone", "Profissional", "Data"])

    for agendamento in agendamentos:
        data_agendamento = []

        data_agendamento.append(str(agendamento.nome_paciente))
        data_agendamento.append(str(agendamento.cpf_paciente if agendamento.cpf_paciente else ""))

        if agendamento.celular_paciente:
            data_agendamento.append(str(agendamento.celular_paciente))
        else:
            data_agendamento.append(str(agendamento.telefone_fixo_paciente if agendamento.telefone_fixo_paciente else ""))

        data_agendamento.append(str(agendamento.medico.nome_profissional))

        data_agendamento.append(f'{agendamento.data_atendimento.strftime("%d/%m/%Y")} {agendamento.hora_inicio_atendimento.strftime("%H:%M")}')

        data.append(data_agendamento)

        row_heights.append(0.2*inch)
    
    row_heights = tuple(row_heights)



    buf = io.BytesIO()

    pdf_relatorio = BaseDocTemplate(buf, pagesize=(838,593))

    frame = Frame(pdf_relatorio.leftMargin, pdf_relatorio.bottomMargin, pdf_relatorio.width, pdf_relatorio.height, id='normal')


    logo_1gov_url = 'publicmanager/comum/static/img/logo-1gov.png'
    # os.path.join(settings.STATIC_URL, 'img/logo-1gov.png')
    
    header_content = Table(
        [
            [
                Paragraph("RELATÓRIO DE AGENDAMENTOS<br/>AGENDAMENTOS REALIZADOS", ParagraphStyle("paragráfo estilização", alignment=1)),
                Image(logo_1gov_url, width=2.2*inch, height=0.7*inch)
            ]
        ], colWidths=(8.2*inch, 2.7*inch), rowHeights=(1.1*inch)
    )

    header_content.setStyle(TableStyle(
            [
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]
        )
    )


    stylePrimeiroParagrafoRodape = ParagraphStyle("paragráfo rodapé", fontSize=8)
    styleSegundoParagrafoRodape = ParagraphStyle("paragráfo rodapé", fontSize=8, alignment=2)

    footer_content = Table([
        [
            Paragraph("<i>Sistema 1gov</i>", stylePrimeiroParagrafoRodape),
            Paragraph(f'<i><1gov> Impresso em {datetime.datetime.now().astimezone(timezone("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")}</i>', styleSegundoParagrafoRodape)
        ]
    ], colWidths=(8.6*inch, 2.3*inch))

    footer_content.setStyle(TableStyle(
            [
                ('LINEABOVE', (0,0), (-1,-1), 0.25, colors.black),
                ('LEFTPADDING', (0,0), (0,0), 0),
                ('LEFTPADDING', (1,0), (1,0), 0),
                ('ALIGN', (1,0), (1,0), "RIGHT"),
            ]
        )
    )

    template = PageTemplate(id='test', frames=frame, onPage=partial(header_and_footer, header_content=header_content, footer_content=footer_content))

    pdf_relatorio.addPageTemplates([template])

    Story = []

    tabela_agendamentos = Table(data, colWidths=(3.42*inch, 1.35*inch, 1.35*inch, 3.43*inch, 1.35*inch), rowHeights=row_heights, repeatRows=2)

    tabela_agendamentos.setStyle(TableStyle(
            [
                ('TOPPADDING', (0,0), (-1,0), 20),
                ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
                ('FONTSIZE', (0,2), (-1,-1), 8),
                ('ALIGN',(0,1),(-1,1),'CENTER'),
                ('VALIGN',(0,1),(-1,1),'MIDDLE'),
                ('VALIGN',(0,2),(-1,2),'MIDDLE'),
                ('LEFTPADDING', (0,1), (-1,-1), 3),
                ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
                ('BOX', (0,1), (-1,-1), 0.25, colors.black),
                ('VALIGN',(0,2), (-1,-1),'MIDDLE'),
            ]
        )
    )

    Story.append(tabela_agendamentos)

    pdf_relatorio.build(Story)

    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="RelatorioAgendaMedicaPDF.pdf")
def pdf_relatorio_bloqueios_agenda(request):
    medico_id = request.POST.get("id_medico")
    
    bloqueios_agenda = BloqueioAgenda.objects.filter(medico__id__exact=medico_id)
    bloqueios_agenda = bloqueios_agenda.order_by('data_inicial')

    row_heights = [0.7*inch, 0.2*inch]

    data = [["","","",""]]

    data.append(["Profissional", "Período Afastamento", "Quantidade Dias", "Motivo"])

    for bloqueio_agenda in bloqueios_agenda:
        quantidade_de_dias_bloqueados = abs((bloqueio_agenda.data_inicial - bloqueio_agenda.data_final).days)+1

        data_bloqueio_agenda = []

        data_bloqueio_agenda.append(str(bloqueio_agenda.medico.nome_profissional))
        data_bloqueio_agenda.append(f'{bloqueio_agenda.data_inicial.strftime("%d/%m/%Y")} a {bloqueio_agenda.data_final.strftime("%d/%m/%Y")}')
        data_bloqueio_agenda.append(str(quantidade_de_dias_bloqueados))
        data_bloqueio_agenda.append(str(bloqueio_agenda.motivo))

        data.append(data_bloqueio_agenda)

        row_heights.append(0.2*inch)
    
    row_heights = tuple(row_heights)



    buf = io.BytesIO()

    pdf_relatorio_bloqueios = BaseDocTemplate(buf, pagesize=(838,593))

    frame = Frame(pdf_relatorio_bloqueios.leftMargin, pdf_relatorio_bloqueios.bottomMargin, pdf_relatorio_bloqueios.width, pdf_relatorio_bloqueios.height, id='normal')


    logo_1gov_url = 'publicmanager/comum/static/img/logo-1gov.png'
    # os.path.join(settings.STATIC_URL, 'img/logo-1gov.png')
    
    header_content = Table(
        [
            [
                Paragraph("RELATÓRIO DE BLOQUEIOS DE AGENDA<br/>BLOQUEIOS DE AGENDA INSERIDOS", ParagraphStyle("paragráfo estilização", alignment=1)),
                Image(logo_1gov_url, width=2.2*inch, height=0.7*inch)
            ]
        ], colWidths=(8.2*inch, 2.7*inch), rowHeights=(1.1*inch)
    )

    header_content.setStyle(TableStyle(
            [
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]
        )
    )

    stylePrimeiroParagrafoRodape = ParagraphStyle("paragráfo rodapé", fontSize=8)
    styleSegundoParagrafoRodape = ParagraphStyle("paragráfo rodapé", fontSize=8, alignment=2)

    footer_content = Table([
        [
            Paragraph("<i>Sistema 1gov</i>", stylePrimeiroParagrafoRodape),
            Paragraph(f'<i><1gov> Impresso em {datetime.datetime.now().astimezone(timezone("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")}</i>', styleSegundoParagrafoRodape)
        ]
    ], colWidths=(8.6*inch, 2.3*inch))

    footer_content.setStyle(TableStyle(
            [
                ('LINEABOVE', (0,0), (-1,-1), 0.25, colors.black),
                ('LEFTPADDING', (0,0), (0,0), 0),
                ('LEFTPADDING', (1,0), (1,0), 0),
                ('ALIGN', (1,0), (1,0), "RIGHT"),
            ]
        )
    )


    template = PageTemplate(id='test', frames=frame, onPage=partial(header_and_footer, header_content=header_content, footer_content=footer_content))

    pdf_relatorio_bloqueios.addPageTemplates([template])

    Story = []

    tabela_bloqueios_agenda = Table(data, colWidths=(3.3*inch, 1.7*inch, 1.20*inch, 4.7*inch), rowHeights=row_heights, repeatRows=2)

    tabela_bloqueios_agenda.setStyle(TableStyle(
            [
                ('TOPPADDING', (0,0), (-1,0), 20),
                ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
                ('FONTSIZE', (0,2), (-1,-1), 8),
                ('ALIGN',(0,1),(-1,1),'CENTER'),
                ('ALIGN',(1,2),(1,-1),'CENTER'),
                ('ALIGN',(2,2),(2,-1),'CENTER'),
                ('VALIGN',(0,1),(-1,1),'MIDDLE'),
                ('VALIGN',(0,2), (-1,-1),'MIDDLE'),
                ('LEFTPADDING', (0,2), (0,-1), 3),
                ('LEFTPADDING', (3,2), (3,-1), 3),
                ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
                ('BOX', (0,1), (-1,-1), 0.25, colors.black),
            ]
        )
    )

    Story.append(tabela_bloqueios_agenda)

    pdf_relatorio_bloqueios.build(Story)

    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="RelatorioBloqueioAgendaPDF.pdf")

class FeriadoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Feriado
    form_class = FeriadoForm
    success_url = reverse_lazy('saude_atendimento:agenda_medica_view')


class BuscarAgendamentosView(LoginRequiredMixin, ListView):
    model = AgendamentoConsultorio
    context_object_name = 'agendamentos'
    template_name = 'saude_atendimento/buscar_agendamentos_consultorio.html'
    form_class = BuscarAgendamentosForm
    paginate_by=10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-data_atendimento', 'hora_inicio_atendimento')

        if self.request.GET.get("nome_paciente_filtro"):
            queryset = queryset.filter(nome_paciente__icontains=self.request.GET.get("nome_paciente_filtro"))
        if self.request.GET.get("cpf_paciente_filtro"):
            queryset = queryset.filter(cpf_paciente__exact=self.request.GET.get("cpf_paciente_filtro").replace(".", "").replace("-",""))
        if self.request.GET.get("medico_filtro"):
            queryset = queryset.filter(medico__id__exact=self.request.GET.get("medico_filtro"))
        if self.request.GET.get("data_atendimento_filtro"):
            data_atendimento_filtro = self.request.GET.get("data_atendimento_filtro")

            data_atendimento_filtro = data_atendimento_filtro.split("/")
            data_atendimento_filtro = data_atendimento_filtro[2]+"-"+data_atendimento_filtro[1]+"-"+data_atendimento_filtro[0]

            queryset = queryset.filter(data_atendimento=data_atendimento_filtro)
        if self.request.GET.get("hora_atendimento_filtro"):
            hora_atendimento_filtro = self.request.GET.get("hora_atendimento_filtro")

            hora_atendimento_filtro = hora_atendimento_filtro.split(":")
            hora_atendimento_filtro = hora_atendimento_filtro[0]+":"+hora_atendimento_filtro[1]+":00"

            queryset = queryset.filter(hora_inicio_atendimento=hora_atendimento_filtro)

        return queryset

    def get_context_data(self, **kwargs):
        medico_id = self.request.GET.get('medico_filtro', '')

        agenda_medica_url = reverse('saude_atendimento:agenda_medica_view')
        buscar_agendamentos_url = reverse('saude_atendimento:buscar_agendamentos_view')


        context = super().get_context_data(**kwargs)


        context['nome_paciente_filtro'] = self.request.GET.get('nome_paciente_filtro', '')
        context['cpf_paciente_filtro'] = self.request.GET.get('cpf_paciente_filtro', '')

        context['medico_filtro'] = ""

        if medico_id:
            medico_id = UUID(medico_id)

            agenda_medica_url = reverse('saude_atendimento:agenda_medica_medico_view', kwargs={'medico_id': medico_id})

            query_string = urlencode({'medico_filtro': self.request.GET.get('medico_filtro', "")})
            buscar_agendamentos_url = f'{buscar_agendamentos_url}?{query_string}'

            context['medico_filtro'] = medico_id
        
        context['medicos'] = Profissional.objects.filter(tipo_profissional=Profissional.MEDICO)

        context['data_atendimento_filtro'] = self.request.GET.get('data_atendimento_filtro', '')
        context['hora_atendimento_filtro'] = self.request.GET.get('hora_atendimento_filtro', '')

        context['data_atual'] = datetime.date.today()

        context["form"] = AgendaMedicaForm
        context["medico_id"] = medico_id


        context['crumbs'] = [
            {'label': 'Agenda Médica', 'url': agenda_medica_url},
            {'label': 'Busca de Agendamentos', 'url': buscar_agendamentos_url}
        ]


        return context



class PreAtendimentoMedicoDetailView(LoginRequiredMixin, DetailView):
    model = Paciente
    context_object_name = "paciente"
    template_name = "saude_atendimento/pre_atendimento.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_atual'] = datetime.datetime.now()
        context['tipos_classificacao_risco'] = TipoClassificacaoRisco.objects.filter(situacao='ATIVO').order_by('ordem')

        context['pre_atendimentos_abertos'] = PreAtendimentoMedico.objects.filter(situacao=BoletimPaciente.ABERTO)

        if self.request.GET.get('pre_atendimento'):
            context['pre_atendimento_edicao'] = PreAtendimentoMedico.objects.get(pk=self.request.GET.get('pre_atendimento'))

            context['form'] = PreAtendimentoMedicoUpdateForm(instance=PreAtendimentoMedico.objects.get(pk=self.request.GET.get('pre_atendimento')))
        else:
            context['form'] = PreAtendimentoMedicoCreateForm()


        return context
    
class PreAtendimentoMedicoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PreAtendimentoMedico
    template_name = 'saude_atendimento/pre_atendimento.html'
    form_class = PreAtendimentoMedicoCreateForm
    success_message = 'Seus dados foram cadastrados conforme preenchimento do formulário.'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form_is_valid = form.is_valid()
        if form_is_valid:
            self.object = form.save(commit=False)
            self.object.save()
            return redirect('saude_atendimento:agenda_medica_view')
        else:
            paciente = form.cleaned_data.get('paciente')
            return redirect(reverse('saude_atendimento:pre_atendimento_listagem', kwargs={'pk': paciente.pk}))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return redirect('saude_atendimento:agenda_medica_view')

class PreAtendimentoMedicoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PreAtendimentoMedico
    template_name = 'saude_atendimento/pre_atendimento.html'
    form_class = PreAtendimentoMedicoUpdateForm
    success_message = 'Seus dados foram alterados conforme preenchimento do formulário.'

    def get_success_url(self):
        if self.request.GET.get('paciente'):
            return reverse('saude_atendimento:pre_atendimento_listagem', kwargs={'pk': self.request.GET.get('paciente')})

class PreAtendimentoMedicoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PreAtendimentoMedico
    template_name = 'includes/confirmar_cancelar_remocao.html'

    def get_success_url(self):
        if self.request.GET.get('paciente'):
            return reverse('saude_atendimento:pre_atendimento_listagem', kwargs={'pk': self.request.GET.get('paciente')})