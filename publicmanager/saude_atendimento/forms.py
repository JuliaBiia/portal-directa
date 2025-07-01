from django import forms
from dal import autocomplete

from publicmanager.saude_cadastro.models import UnidadeSaude
from publicmanager.saude_farmacia.models import Medicamento, PrincipioAtivo
from publicmanager.saude_atendimento.models import JustificativaProcedimentoAtendimento
from publicmanager.saude_cadastro.models import Profissao, Estado, CID, Profissional
from .models import AgendamentoConsultorio, BloqueioAgenda, Feriado, HorarioMedico, Paciente, PreAtendimentoMedico, TipoAltaHospitalar, AnamnesePaciente, BoletimPaciente, ClassificacaoRisco, AtestadoAtendimento, FichaReferenciaAtendimento


class PacienteCriarForm(forms.ModelForm):
    profissao = forms.ModelChoiceField(queryset=Profissao.objects.all(), empty_label="Selecione a Profissão", required=False)
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), empty_label="Selecione a UF")
   
    class Meta:
        model = Paciente
        fields = '__all__'

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        if not cpf:
            return cpf

        if cpf:
            cpf_sem_caracteres = ''.join(filter(str.isdigit, cpf))
        
            if Paciente.objects.filter(cpf=cpf_sem_caracteres).exists():
                raise forms.ValidationError("Este CPF já existe.")

        return cpf
    
    def clean_cartao_sus(self):
        cartao_sus = self.cleaned_data.get('cartao_sus')

        if not cartao_sus:
            return cartao_sus

        if cartao_sus:
            cartao_sus_sem_caracteres = ''.join(filter(str.isdigit, cartao_sus))

            if Paciente.objects.filter(cartao_sus=cartao_sus_sem_caracteres).exists():
                raise forms.ValidationError("Este Cartão Sus já existe.")
        
        return cartao_sus

class PacienteAtualizarForm(forms.ModelForm):
   
    class Meta:
        model = Paciente
        fields = '__all__'
        exclude = ('unidade_saude', 'anamnese_paciente')

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        if not cpf:
            return cpf

        if self.instance and cpf:
            cpf_sem_caracteres = ''.join(filter(str.isdigit, cpf))
        
            if Paciente.objects.exclude(id=self.instance.id).filter(cpf=cpf_sem_caracteres).exists():
                raise forms.ValidationError("Este CPF já existe.")

        return cpf
    
    def clean_cartao_sus(self):
        cartao_sus = self.cleaned_data.get('cartao_sus')

        if not cartao_sus:
            return cartao_sus

        if self.instance and cartao_sus:
            cartao_sus_sem_caracteres = ''.join(filter(str.isdigit, cartao_sus))

            if Paciente.objects.exclude(id=self.instance.id).filter(cartao_sus=cartao_sus_sem_caracteres).exists():
                raise forms.ValidationError("Este Cartão Sus já existe.")
        
        return cartao_sus

class PacienteFilterForm(forms.ModelForm):
    nome_paciente = forms.CharField(label='Nome do Paciente', max_length=200, required=False)

    class Meta:
        model = Paciente
        fields = ('nome_paciente', 'cpf', 'cartao_sus', 'rg')

class AnamnesePacienteForm(forms.ModelForm):
    class Meta:
        model = AnamnesePaciente
        exclude = ['alergias_medicamentosas', 'antecedentes_patologicos_pessoais', 'antecedentes_patologicos_familiares']


class ClassificacaoRiscoCriarForm(forms.ModelForm):
  
    class Meta:
        model = ClassificacaoRisco
        exclude = ('setor', 'status', 'reclassificacao')

class ClassificacaoRiscoAtualizarForm(forms.ModelForm):
    class Meta:
        model = ClassificacaoRisco
        exclude = ('paciente', 'boletim', 'tipo_atendimento', 'numero_atendimento', 'setor', 'status', 'profissional', 'reclassificacao')

class TipoAltaHospitalarForm(forms.ModelForm):
    class Meta:
        model = TipoAltaHospitalar
        fields = '__all__'

class TipoAltaHospitalarFilterForm(forms.ModelForm):
    tipo_de_alta_hospitalar = forms.CharField(label='Tipo de alta hospitalar', max_length=50, required=False)

    class Meta:
        model = TipoAltaHospitalar
        fields = '__all__'
        
class PacienteNovoBoletimCreateForm(forms.ModelForm):
    class Meta:
        model = BoletimPaciente
        exclude = ['situacao',]

class PacienteNovoBoletimUpdateForm(forms.ModelForm):
    class Meta:
        model = BoletimPaciente
        fields = ('nome_responsavel', 'rg_responsavel', 'tipo')

class AtestadoAtendimentoForm(forms.ModelForm):
    class Meta:
        model = AtestadoAtendimento
        fields = '__all__'

class FichaReferenciaAtendimentoForm(forms.ModelForm):
    exames = forms.BooleanField(required=False)
    tratamentos = forms.BooleanField(required=False)
    diagnosticos = forms.BooleanField(required=False)
    class Meta:
        model = FichaReferenciaAtendimento
        fields = ('resumo_clinico', 'atendimento', 'exames', 'tratamentos', 'diagnosticos')

class HorarioMedicoForm(forms.ModelForm):
    medico_horariomedico = forms.ModelChoiceField(queryset=Profissional.objects.filter(tipo_profissional=Profissional.MEDICO))

    class Meta:
        model = HorarioMedico
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        medico_horariomedico = cleaned_data.get('medico_horariomedico')
        dia_semana_horariomedico = cleaned_data.get('dia_semana_horariomedico')
        hora_inicial_horariomedico = cleaned_data.get('hora_inicial_horariomedico')
        hora_final_horariomedico = cleaned_data.get('hora_final_horariomedico')

        if hora_inicial_horariomedico > hora_final_horariomedico:
            raise forms.ValidationError("Horário final deve ser posterior ao horário inicial.")
        else:
            """
            Dois ou mais médicos diferentes podem ter horários que sejam no mesmo dia da semana e no mesmo horário. Também vale caso tenham horário que sejam no mesmo dia da semana e em horários que possuam intersecção. Porém, não deve ter possível cadastrar para um médico um horário que seja no mesmo dia e horário que outro já cadastrado para o mesmo. O mesmo vale se for no mesmo dia e em um horário que tenha intersecção com algum dos horários do médico para o mesmo dia. Por este motivo, abaixo há lançamentos de exceções para impossibilitar fazer algo assim.

            Existem 3 situações nas quais isto pode acontecer. Nos comentários abaixo, é explicado melhor quais são estas situações.
            """

            instance = self.instance

            # Situação 01: O horário inicial que será cadastrado está entre o horário inicial e o horário final de algum dos horários médicos já cadastrados. Para esta situação, independente qual o horário final.
            horarios_medico = HorarioMedico.objects.filter(
                medico_horariomedico__id__exact=medico_horariomedico.id,
                dia_semana_horariomedico__exact=dia_semana_horariomedico,
                hora_inicial_horariomedico__lte=hora_inicial_horariomedico, 
                hora_final_horariomedico__gte=hora_inicial_horariomedico
            )

            if instance:
                horarios_medico = horarios_medico.exclude(id__exact=instance.id)

            
            if horarios_medico:
                raise forms.ValidationError("Este horário entra em conflito com os outros horários cadastrados para este médico! Por favor verifique os horários do médico e tente novamente.")
            else:
                # Situação 02: Se chegou aqui, o horário inicial que será cadastrado não está entre o horário inicial e o horário final de nenhum dos horários médicos já cadastrados. Porém, o horário final do mesmo pode está e a horário inicial está antes do horário inicial do mesmo horário médico cadastrado.
                horarios_medico = HorarioMedico.objects.filter(
                    medico_horariomedico__id__exact=medico_horariomedico.id,
                    dia_semana_horariomedico__exact=dia_semana_horariomedico,
                    hora_inicial_horariomedico__lte=hora_final_horariomedico,
                    hora_final_horariomedico__gte=hora_final_horariomedico
                )

                if instance:
                    horarios_medico = horarios_medico.exclude(id__exact=instance.id)

                if horarios_medico:
                    raise forms.ValidationError("Este horário entra em conflito com os outros horários cadastrados para este médico! Por favor verifique os horários do médico e tente novamente.")
                else:
                    # Situação 03: Se chegou aqui, ainda existe a possibilidade de que algum dos feriados esteja entre os dias do feriado que será cadastrado. Por exemplo, o feriado que será cadastrado é 10/10/2023 - 17/10/2023 e tem um feriado já cadastrado é 13/10/2023 - 15/10/2023.
                    horarios_medico = HorarioMedico.objects.filter(
                        medico_horariomedico__id__exact=medico_horariomedico.id,
                        dia_semana_horariomedico__exact=dia_semana_horariomedico,
                        hora_inicial_horariomedico__gt=hora_inicial_horariomedico,
                        hora_final_horariomedico__lt=hora_final_horariomedico
                    )

                    if instance:
                        horarios_medico = horarios_medico.exclude(id__exact=instance.id)

                    if horarios_medico:
                        raise forms.ValidationError("Este horário entra em conflito com os outros horários cadastrados para este médico! Por favor verifique os horários do médico e tente novamente.")

        return cleaned_data

class AgendaMedicaFiltroForm(forms.Form):
    medico_filtragem_agendamentos = forms.ModelChoiceField(queryset=Profissional.objects.none(), required=False)

class AgendaMedicaForm(forms.ModelForm):
    PRIMEIRO_ATENDIMENTO = 1
    EXTRA_ENCAIXE = 2
    RETORNO = 3
    TIPO_ATENDIMENTO_CHOICES = (
        (PRIMEIRO_ATENDIMENTO, 'Primeiro atendimento'),
        (EXTRA_ENCAIXE, 'Extra encaixe'),
        (RETORNO, 'Retorno'),
    )

    medico = forms.ModelChoiceField(queryset=Profissional.objects.filter(tipo_profissional=Profissional.MEDICO), required=False)
    tipo_atendimento = forms.ChoiceField(
        choices=TIPO_ATENDIMENTO_CHOICES,
        widget=forms.RadioSelect,
        label='Selecione uma opção'
    )

    class Meta:
        model = AgendamentoConsultorio
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

class RelatorioAgendamentoForm(forms.Form):
    data_inicial_relatorio = forms.DateField(required=False)
    data_final_relatorio = forms.DateField(required=False)
    paciente_relatorio = forms.ModelChoiceField(queryset=AgendamentoConsultorio.objects.values_list('nome_paciente',flat=True).order_by('nome_paciente').distinct(), empty_label="TODOS", required=False)
    cpf_paciente_relatorio = forms.ModelChoiceField(queryset=AgendamentoConsultorio.objects.values_list('cpf_paciente',flat=True).filter(cpf_paciente__isnull=False).order_by('cpf_paciente').distinct(), empty_label="TODOS", required=False)
    medico_relatorio = forms.ModelChoiceField(queryset=Profissional.objects.filter(tipo_profissional=Profissional.MEDICO), empty_label="TODOS", required=False)

class FeriadoForm(forms.ModelForm):
    class Meta:
        model = Feriado
        fields = '__all__'

class FeriadoFilterForm(forms.Form):
    nome_feriado = forms.CharField(label='Nome do Feriado', max_length=200, required=False)

    class Meta:
        model = Feriado
        fields = ('nome_feriado',)

class BloqueioAgendaForm(forms.ModelForm):
    class Meta:
        model = BloqueioAgenda
        fields = '__all__'

class BloqueioAgendaFilterForm(forms.ModelForm):
    motivo = forms.CharField(label='Nome do Feriado', max_length=200, required=False)
    class Meta:
        model = BloqueioAgenda
        fields = ('motivo',)

class BuscarAgendamentosForm(forms.ModelForm):
    nome_paciente = forms.CharField(label='Nome do Paciente', max_length=200, required=False)
    medico = forms.ModelChoiceField(queryset=Profissional.objects.none(), required=False)

    class Meta:
        model = AgendamentoConsultorio
        fields = ('nome_paciente', 'cpf_paciente', 'medico', 'data_atendimento')

class PreAtendimentoMedicoCreateForm(forms.ModelForm):
    class Meta:
        model = PreAtendimentoMedico
        fields = '__all__'

class PreAtendimentoMedicoUpdateForm(forms.ModelForm):
    class Meta:
        model = PreAtendimentoMedico
        fields = '__all__'
        exclude = ('paciente', 'agendamento_atendimento')

class JustificativaProcedimentoCreateForm(forms.ModelForm):
    diagnostico = forms.ModelChoiceField(
        queryset=CID.objects.all(),
        widget=autocomplete.ModelSelect2(url='saude_cadastro:api_cid_autocomplete'),
        empty_label="Selecione um Diagnostico",
        required=True
    )

    cid_10_principal = forms.ModelChoiceField(
        queryset=CID.objects.all(),
        widget=autocomplete.ModelSelect2(url='saude_cadastro:api_cid_autocomplete'),
        empty_label="Selecione um Diagnóstico",
        required=True
    )

    cid_10_secundario = forms.ModelChoiceField(
        queryset=CID.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='saude_cadastro:api_cid_autocomplete',
            attrs={
                'data-placeholder': 'Selecione um CID 10 Secundário',
                'data-allow-clear': 'true',
            }
        ),
        empty_label="Selecione um CID 10 Secundário",
        required=False
    )

    cid_10_causa_associada = forms.ModelChoiceField(
        queryset=CID.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='saude_cadastro:api_cid_autocomplete',
            attrs={
                'data-placeholder': 'Selecione um CID 10 Causa Associada',
                'data-allow-clear': 'true',
            }
        ),
        empty_label="Selecione um CID 10 Causa Associada",
        required=False
    )
    class Meta:
        model = JustificativaProcedimentoAtendimento
        fields = '__all__'

class JustificativaProcedimentoUpdateForm(forms.ModelForm):
    diagnostico = forms.ModelChoiceField(
        queryset=CID.objects.all(),
        widget=autocomplete.ModelSelect2(url='saude_cadastro:api_cid_autocomplete'),
        empty_label="Selecione um Diagnostico",
        required=True
    )

    cid_10_principal = forms.ModelChoiceField(
        queryset=CID.objects.all(),
        widget=autocomplete.ModelSelect2(url='saude_cadastro:api_cid_autocomplete'),
        empty_label="Selecione um Diagnóstico",
        required=True
    )

    cid_10_secundario = forms.ModelChoiceField(
        queryset=CID.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='saude_cadastro:api_cid_autocomplete',
            attrs={
                'data-placeholder': 'Selecione um CID 10 Secundario',
                'data-allow-clear': 'true',
            }
        ),
        empty_label="Selecione um CID 10 Secundario",
        required=False
    )

    cid_10_causa_associada = forms.ModelChoiceField(
        queryset=CID.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='saude_cadastro:api_cid_autocomplete',
            attrs={
                'data-placeholder': 'Selecione um CID 10 Causa Associada',
                'data-allow-clear': 'true',
            }
        ),
        empty_label="Selecione um CID 10 Causa Associada",
        required=False
    )
    
    class Meta:
        model = JustificativaProcedimentoAtendimento
        exclude = ('atendimento', 'profissional')

class RelatorioAtendimentosForm(forms.Form):
    data_inicial = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_final = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    unidade_saude = forms.ModelChoiceField(queryset=UnidadeSaude.objects.all())