from django.db import models
from django.utils import timezone
from django.db import transaction
from django_lifecycle import hook
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from simple_history.models import HistoricalRecords

from publicmanager.comum.models import BaseModel
from publicmanager.saude.templatetags.saude_extras import tempo_medio_espera_hora

def documentacao_administracao_medicamento_path(instance, filename):
    return f"documentos/documentos_administracao_medicamento/{instance.pk}_{filename}"

def documentacao_administracao_procedimento_path(instance, filename):
    return f"documentos/documentos_administracao_procedimento/{instance.pk}_{filename}"

def documentacao_administracao_medicamento_foto_path(instance, filename):
    return f"documentos/documentos_administracao_medicamento_foto/{instance.pk}_{filename}"

def documentacao_administracao_procedimento_foto_path(instance, filename):
    return f"documentos/documentos_administracao_procedimento_foto/{instance.pk}_{filename}"

class SituacaoMedicacaoAtendimento(BaseModel):
    medicacao_atendimento = models.ForeignKey('saude_atendimento.MedicacaoAtendimento', on_delete=models.PROTECT)
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    data_hora_aplicacao = models.DateTimeField(verbose_name='Data e hora da Aplicação', blank=True, null=True)
    cancelado = models.BooleanField('Cancelado?', default=False)
    observacao = models.TextField('Observação', blank=True, null=True)

    class Meta:
        verbose_name = 'Situação Medicação Atendimento'
        verbose_name_plural = '1 - Situações das Medicações dos Atendimentos'

    def __str__(self):
        return f'{self.medicacao_atendimento.lista_chamada_solicitacao} - {self.data_hora_aplicacao}'

class ListaChamadaSolicitacaoAtendimento(BaseModel):
    sala = models.ForeignKey('saude_cadastro.Sala', related_name='sala_lista_chamada_enfermagem_set', on_delete=models.PROTECT, blank=True, null=True)
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de Saúde',on_delete=models.PROTECT)
    atendimento = models.ForeignKey('saude_atendimento.AtendimentoMedico', on_delete=models.PROTECT)
    contagem = models.IntegerField('Contagem', default=0, blank=True, null=True)
    
    SOLICITADO, EM_ESPERA, DESIGNADO, TRANSFERENCIA, OBITO, EM_ATENDIMENTO, CONCLUIDO, REVELIA, REABERTURA = range(9)
    SITUACAO_CHAMADOS = (
        (SOLICITADO, "SOLICITADO"),
        (EM_ESPERA, "EM ESPERA"),
        (DESIGNADO, "DESIGNADO"),
        (TRANSFERENCIA, "TRANSFERÊNCIA"),
        (OBITO, "OBITO"),
        (EM_ATENDIMENTO, "EM ATENDIMENTO"),
        (CONCLUIDO, 'CONCLUIDO'),
        (REVELIA, 'REVELIA'),
        (REABERTURA, 'REABERTURA'),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHAMADOS, default=SOLICITADO, blank=True, null=True, help_text='situação Atual do Chamado')
    
    EXAME_LABORATORIO, EXAME_IMAGEM, PROCEDIMENTO, MEDICACAO = range(4)
    TIPO_CHOICE = (
        (EXAME_LABORATORIO, "EXAME LABORATÓRIO"),
        (EXAME_IMAGEM, "EXAME IMAGEM"),
        (PROCEDIMENTO, "PROCEDIMENTO"),
        (MEDICACAO, "MEDICAÇÃO")
    )
    tipo = models.SmallIntegerField("Tipo", choices=TIPO_CHOICE, default=EXAME_LABORATORIO, blank=True, null=True)
    sequencial = models.IntegerField("Sequencial", blank=True, null=True)
    # tempo_espera = models.TimeField(blank=True, null=True)

    historico = HistoricalRecords()
    class Meta:
        verbose_name = 'Lista de Chamado Solicitação'
        verbose_name_plural = '2 - Lista de Chamados das Solicitações'

    def __str__(self):
        return f'{self.pk} - {self.get_tipo_display()}'
    
    def calcular_dosagem_proxima(self):
        from publicmanager.saude_atendimento.models import MedicacaoAtendimento

        medicacoes = MedicacaoAtendimento.objects.filter(lista_chamada_solicitacao=self, situacao=MedicacaoAtendimento.SOLICITADO)

        if medicacoes:
            dosagens = [medicacao.calcular_proxima_dosagem() for medicacao in medicacoes if medicacao.calcular_proxima_dosagem() is not None]
            
            if dosagens:

                hora_minima = min(dosagens)

                return hora_minima
            return None
            
        return None
    
    @hook("before_save", when="situacao", is_now=CONCLUIDO, has_changed=True)
    @hook("before_save", when="situacao", is_now=TRANSFERENCIA, has_changed=True)
    @hook("before_save", when="situacao", is_now=OBITO, has_changed=True)
    @hook("before_save", when="situacao", is_now=REVELIA, has_changed=True)
    def atualizar_situacao_reabertura(self):
        from publicmanager.saude_atendimento.models import ExameAtendimento

        ExameAtendimento.objects.filter(lista_chamada_solicitacao=self.id, situacao=ExameAtendimento.REABERTURA).update(situacao=ExameAtendimento.ANEXADO)
    
    @hook("before_create")
    @hook("before_save", when="situacao", has_changed=True)
    def save_historico_espera_solicitacao(self):
        historico = HistoricoEsperaSolicitacoes.objects.filter(lista_chamada_solicitacao=self).order_by('-created_at').first()

        if historico:
            HistoricoEsperaSolicitacoes.objects.create(
                lista_chamada_solicitacao=self,
                situacao=self.situacao,
                tempo_espera=tempo_medio_espera_hora(historico.created_at)
            )
        else:
            HistoricoEsperaSolicitacoes.objects.create(
                lista_chamada_solicitacao=self,
                situacao=self.situacao,
                tempo_espera=tempo_medio_espera_hora(timezone.localtime(timezone.now()))
            )

    @hook("after_save")
    @hook("after_update")
    def atualizar_listagem(self):

        if self.situacao == ListaChamadaSolicitacaoAtendimento.EM_ESPERA:
            channel_layer = get_channel_layer()

            group_name = ''
            if self.tipo == 0:
                group_name = f'atualizar_listagem_laboratorio'
            elif self.tipo == 1:
                group_name = f'atualizar_listagem_imagem'
            elif self.tipo == 2:
                group_name = f'atualizar_listagem_procedimento'
            elif self.tipo == 3:
                group_name = f'atualizar_listagem_medicacao'
            
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'update_listagem',
                    'paciente': self.atendimento.paciente.nome_paciente,
                    'tipo_setor': 'enfermaria',
                }
            )
    
    
    @hook("before_save", when="situacao", was=EM_ESPERA, is_now=DESIGNADO, has_changed=True)
    @hook("before_save", when="contagem", has_changed=True)
    def save_chamar(self):
        from publicmanager.saude_cadastro.models import PainelChamada
        paineis = PainelChamada.objects.filter(unidade_saude=self.unidade_saude, setores__in=[self.sala.unidade_setor])

        channel_layer = get_channel_layer()
        
        # tipo_setor = ''
        # if self.tipo == ListaChamadaSolicitacaoAtendimento.EXAME_LABORATORIO:
        #     tipo_setor = 'LABORATÓRIO'
        # elif self.tipo == ListaChamadaSolicitacaoAtendimento.EXAME_IMAGEM:
        #     tipo_setor = 'RADIOLOGIA'
        # elif self.tipo == ListaChamadaSolicitacaoAtendimento.PROCEDIMENTO:
        #     tipo_setor = 'PROCEDIMENTO'
        # elif self.tipo == ListaChamadaSolicitacaoAtendimento.MEDICACAO:
        #     tipo_setor = 'MEDICAÇÃO'

        for painel in paineis:
            group_name = f'painel_{painel.unidade_saude.slug.replace("-", "_")}_{painel.slug.replace("-", "_")}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'update_panel',
                    'contagem': self.contagem,
                    'paciente': self.atendimento.paciente.nome_paciente,
                    'tipo_setor': self.sala.unidade_setor.nome,
                    'sala': self.sala.nome_sala,
                }
            )

class ReaberturaSolicitacaoAtendimento(BaseModel):
    lista_chamada_solicitacao = models.ForeignKey(ListaChamadaSolicitacaoAtendimento, on_delete=models.PROTECT)
    medico_solicitante = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    justificativa = models.TextField('justificativa', blank=True, null=True)
    class Meta:
        verbose_name = 'Reabertura Solicitação Atendimento'
        verbose_name_plural = 'Reaberturas das Solicitações dos Atendimentos'

    def __str__(self):
        return f'{self.id} - {self.lista_chamada_solicitacao.atendimento.paciente}'

class HistoricoEsperaSolicitacoes(BaseModel):
    lista_chamada_solicitacao = models.ForeignKey(ListaChamadaSolicitacaoAtendimento, on_delete=models.PROTECT)
    situacao = models.SmallIntegerField("Situação", choices=ListaChamadaSolicitacaoAtendimento.SITUACAO_CHAMADOS, default=ListaChamadaSolicitacaoAtendimento.SOLICITADO, blank=True, null=True, help_text='situação Atual do Chamado')
    tempo_espera = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name = 'Histórico de Tempo de Espera'
        verbose_name_plural = 'Histórico de Tempo de Espera'

    def __str__(self):
        return f'{self.id} - {self.lista_chamada_solicitacao.atendimento.paciente}'

class RequisicaoSolicitacaoAtendimento(BaseModel):
    atendimento = models.ForeignKey('saude_atendimento.AtendimentoMedico', on_delete=models.PROTECT)
    medico_solicitante = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT)
    listas_chamadas_solicitacoes = models.ManyToManyField(ListaChamadaSolicitacaoAtendimento)
    finalizado = models.BooleanField("Solicitação Finalizado?", default=False)
    class Meta:
        verbose_name = 'Requisição da Solicitação'
        verbose_name_plural = '3 - Requisições das Solicitações'

    def __str__(self):
        return f'{self.pk} - {self.medico_solicitante}'

class SolicitacaoAtendimento(BaseModel):
    lista_chamada_solicitacao = models.OneToOneField(ListaChamadaSolicitacaoAtendimento, on_delete=models.PROTECT)
    enfermeiros = models.ManyToManyField('saude_cadastro.Profissional', blank=True)
    numero_atendimento = models.BigIntegerField('Número Atendimento', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Solicitação Atendimento'
        verbose_name_plural = '4 - Solicitações dos Atendimentos'

    def __str__(self):
        return f'{self.lista_chamada_solicitacao} - {self.numero_atendimento}'
    
    @property
    def numero_solicitacao_formatado(self):

        tipo = ''
        if self.lista_chamada_solicitacao.tipo == ListaChamadaSolicitacaoAtendimento.EXAME_LABORATORIO:
            tipo = "LAB"
        elif self.lista_chamada_solicitacao.tipo == ListaChamadaSolicitacaoAtendimento.EXAME_IMAGEM:
            tipo = "IMA"
        elif self.lista_chamada_solicitacao.tipo == ListaChamadaSolicitacaoAtendimento.PROCEDIMENTO:
            tipo = "PRO"
        elif self.lista_chamada_solicitacao.tipo == ListaChamadaSolicitacaoAtendimento.MEDICACAO:
            tipo = "ENF"
        
        return f"{tipo}{str(self.numero_atendimento).zfill(12)}"
    
    @transaction.atomic
    @hook("after_create")
    def criar_numero_medicacao_atendimento(self):
        ultima_instancia = SolicitacaoAtendimento.objects.filter(
            lista_chamada_solicitacao__unidade_saude=self.lista_chamada_solicitacao.unidade_saude,
            lista_chamada_solicitacao__tipo=self.lista_chamada_solicitacao.tipo,
        ).exclude(id=self.id).order_by('-numero_atendimento').select_for_update().first()

        ultimo_atendimento = ultima_instancia.numero_atendimento if ultima_instancia else 0

        self.numero_atendimento = ultimo_atendimento + 1
        self.save()

#medicamento

class ListaChamadoAdministracaoMedicamento(BaseModel):
    boletim = models.ForeignKey('saude_atendimento.BoletimPaciente', verbose_name='Boletim',on_delete=models.PROTECT)
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de Saúde',on_delete=models.PROTECT)
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    sala = models.ForeignKey('saude_cadastro.Sala', on_delete=models.PROTECT, blank=True, null=True)
    contagem = models.IntegerField('Contagem', default=0, blank=True, null=True)
    
    EM_ESPERA, DESIGNADO, EM_ATENDIMENTO, EM_ATENDIMENTO_RETORNO, CONCLUIDO, OBITO, REVELIA, ENCERRADO_ENFERMAGEM, ENCERRADO_ALTA, ENCERRADO_RECEPCAO, \
    ENCERRADO_SISTEMA, TRANSFERENCIA = range(12)
    SITUACAO_CHAMADOS = (
        (EM_ESPERA, "EM ESPERA"),
        (DESIGNADO, "DESIGNADO"),
        (EM_ATENDIMENTO, "EM ATENDIMENTO"),
        (EM_ATENDIMENTO_RETORNO, "EM ATENDIMENTO DE RETORNO"),
        (CONCLUIDO, 'CONCLUIDO'),
        (OBITO, "OBITO"),
        (REVELIA, 'REVELIA'),
        (ENCERRADO_ENFERMAGEM, 'ENCERRADO PELA ENFERMAGEM'),
        (ENCERRADO_ALTA, 'ENCERRADO PELA ALTA'),   
        (ENCERRADO_RECEPCAO, 'ENCERRADO PELA RECEPÇÃO'),
        (ENCERRADO_SISTEMA, 'ENCERRADO PELO SISTEMA'),
        (TRANSFERENCIA, "TRANSFERÊNCIA"),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHAMADOS, default=EM_ESPERA, blank=True, null=True, help_text='situação Atual do Chamado')
    historico = HistoricalRecords()

    class Meta:
        verbose_name = 'Lista de Chamado Administração Medicamento'
        verbose_name_plural = '5 - Lista de Chamados Administrações de Medicamentos'

    def __str__(self):
        return f'{self.pk} - {self.get_situacao_display()}'
    
    @hook("before_save", when="situacao", was=DESIGNADO, is_now=EM_ATENDIMENTO_RETORNO, has_changed=True)
    @hook("before_save", when="situacao", was=DESIGNADO, is_now=EM_ATENDIMENTO, has_changed=True)
    def save_historico_administracao_medicacao(self):
        HistoricoListaChamadoAdministracaoMedicamento.objects.create(
            lista_chamado_administracao_medicamento=self,
            situacao=self.situacao,
            enfermeiro=self.enfermeiro,
            tempo_espera=tempo_medio_espera_hora(self.boletim.updated_at)
        )
    
    @hook("before_save", when="situacao", was=EM_ESPERA, is_now=DESIGNADO, has_changed=True)
    @hook("before_save", when="contagem", has_changed=True)
    def save_chamar(self):
        from publicmanager.saude_cadastro.models import PainelChamada
        paineis = PainelChamada.objects.filter(unidade_saude=self.unidade_saude, setores__in=[self.sala.unidade_setor])

        channel_layer = get_channel_layer()

        for painel in paineis:
            group_name = f'painel_{painel.unidade_saude.slug.replace("-", "_")}_{painel.slug.replace("-", "_")}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'update_panel',
                    'contagem': self.contagem,
                    'paciente': self.boletim.paciente.nome_paciente,
                    'tipo_setor': 'MEDICAÇÃO',
                    'sala': self.sala.nome_sala,
                }
            )

class HistoricoListaChamadoAdministracaoMedicamento(BaseModel):
    lista_chamado_administracao_medicamento = models.ForeignKey(ListaChamadoAdministracaoMedicamento, on_delete=models.PROTECT)
    situacao = models.SmallIntegerField("Status", choices=ListaChamadoAdministracaoMedicamento.SITUACAO_CHAMADOS, default=ListaChamadoAdministracaoMedicamento.EM_ESPERA, blank=True, null=True, help_text='situação Atual do Chamado')
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    tempo_espera = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name = 'Histórico de Administração de Medicamento'
        verbose_name_plural = 'Históricos de Administrações de Medicamentos'

    def __str__(self):
        return f'{self.id} - {self.lista_chamado_administracao_medicamento.boletim.paciente}'

class ReceitaMedicamento(BaseModel):
    paciente = models.ForeignKey('saude_atendimento.Paciente', on_delete=models.PROTECT)
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    lista_chamada_solicitacao = models.ForeignKey(ListaChamadoAdministracaoMedicamento, on_delete=models.PROTECT, blank=True, null=True)
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de Saúde',on_delete=models.PROTECT)
    arquivo = models.FileField("Arquivo", upload_to=documentacao_administracao_medicamento_path, blank=True, null=True)
    foto_receita = models.ImageField(blank=True, null=True, upload_to=documentacao_administracao_medicamento_foto_path)

    class Meta:
        verbose_name = 'Receita Medicamento'
        verbose_name_plural = '6 - Receitas do Medicamentos'

    def __str__(self):
        return f'{self.paciente}'

class AdministracaoMedicamento(BaseModel):
    receita_medicamento = models.ForeignKey(ReceitaMedicamento, on_delete=models.PROTECT)
    medicacao = models.ForeignKey('saude_farmacia.Medicamento', on_delete=models.PROTECT)
    dosagem = models.CharField('Dosagem', max_length=30, blank=True, null=True)
    forma_farmaceutica = models.CharField('Forma Farmaceutica', max_length=255, blank=True, null=True)

    ORAL, PARENTAL, SUBCUTANIA, NASAL, RETAL, INTRAVESICAL, NEBOLIZACAO, OCULAR, SUBLINGUAL, RESPIRATORIA, TOPICO, DERMATOLOGICA, INALATORIA, OTOLOGICA, TRANSDERMICA, VAGINAL, LOCAL, EPIDURAL = range(18)
    ADMIN_MEDICAMENTOSA_CHOICES = (
        (ORAL, "ORAL"),
        (PARENTAL, "PARENTAL"),
        (SUBCUTANIA, "SUBCUTÂNIA"),
        (NASAL, "NASAL"),
        (RETAL, "RETAL"),
        (INTRAVESICAL, "INTRAVESICAL"),
        (NEBOLIZACAO, "NEBOLIZAÇÃO"),
        (OCULAR, "OCULAR"),
        (SUBLINGUAL, "SUBLINGUAL"),
        (RESPIRATORIA,'RESPIRATÓRIA'),
        (TOPICO, 'TÓPICO'),
        (DERMATOLOGICA, 'DERMATOLÓGICA'),
        (INALATORIA, 'INALATÓRIA'),
        (OTOLOGICA, 'OTOLOGICA'),
        (TRANSDERMICA, 'TRANSDÉRMICA'),
        (VAGINAL, 'VAGINAL'),
        (LOCAL, 'LOCAL'),
        (EPIDURAL, 'EPIDURAL'),
    )
    admin_medicamentosa = models.SmallIntegerField("Via de Administação Medicamentosa", choices=ADMIN_MEDICAMENTOSA_CHOICES)

    INTRAVENOSA, INTRAMUSCULAR, SUBCUTANEA, INTRATECAL = range(4)
    TIPO_PARENTAL_CHOICES = (
        (INTRAVENOSA, "INTRAVENOSA"),
        (INTRAMUSCULAR, "INTRAMUSCULAR"),
        (SUBCUTANEA, "SUBCUTÂNEA"),
        (INTRATECAL, "INTRATECAL"),
    )
    tipo_parenteral = models.SmallIntegerField("Tipo Parental", choices=TIPO_PARENTAL_CHOICES, blank=True, null=True)

    quantidade = models.IntegerField("Quantidade", blank=True, null=True) 
    DOSE_UNICA, SEMANAL, MENSAL, DIARIA = range(4)
    CHOICE_POSOLOGIA = (
        (DOSE_UNICA, "DOSE UNICA"),
        (SEMANAL, "SEMANAL"),
        (MENSAL, "MENSAL"),
        (DIARIA, "DIARIA"),
    )
    periodo = models.SmallIntegerField("Período", choices=CHOICE_POSOLOGIA, blank=True, null=True)
    posologia = models.CharField('Posologia', blank=True, null=True)

    observacao = models.TextField('Observação', blank=True, null=True)

    class Meta:
        verbose_name = 'Administração de Medicamento'
        verbose_name_plural = '6 - Administração de Medicamentos'

    def __str__(self):
        return f'{self.receita_medicamento}'

class SituacaoAdministracaoMedicamento(BaseModel):
    administracao_medicamento = models.ForeignKey(AdministracaoMedicamento, on_delete=models.PROTECT)
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    data_hora_aplicacao = models.DateTimeField(verbose_name='Data e hora da Aplicação', blank=True, null=True)

    SOLICITADO, APLICADO, CANCELADO = range(3)
    SITUACAO_CHOICE = (
        (SOLICITADO, "SOLICITADO"),
        (APLICADO, "APLICADO"),
        (CANCELADO, "CANCELADO"),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICE, default=SOLICITADO)
    sequencial = models.IntegerField('Sequencial', blank=True, null=True)
    observacao = models.TextField('Observação', blank=True, null=True)
    cancelou = models.BooleanField('Cancelou?', default=False)
    aplicou_antes = models.BooleanField('Aplicou antes da hora?', default=False)

    class Meta:
        verbose_name = 'Situação Administração Medicamento'
        verbose_name_plural = '7 - Situações Administrações de Medicametos'

    def __str__(self):
        return f'{self.administracao_medicamento} - {self.data_hora_aplicacao}'

#procedimento

class ListaChamadoAdministracaoProcedimento(BaseModel):
    classificacao_risco = models.OneToOneField('saude_atendimento.ClassificacaoRisco', related_name='classificacao_risco_lista_procedimento_set', on_delete=models.CASCADE, default=0)
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de Saúde',on_delete=models.PROTECT)
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    sala = models.ForeignKey('saude_cadastro.Sala', on_delete=models.PROTECT, blank=True, null=True)
    contagem = models.IntegerField('Contagem', default=0, blank=True, null=True)
    
    EM_ESPERA, DESIGNADO, EM_ATENDIMENTO, EM_ATENDIMENTO_RETORNO, CONCLUIDO, OBITO, REVELIA, ENCERRADO_ENFERMAGEM, ENCERRADO_ALTA, ENCERRADO_RECEPCAO, \
    ENCERRADO_SISTEMA, TRANSFERENCIA = range(12)
    SITUACAO_CHAMADOS = (
        (EM_ESPERA, "EM ESPERA"),
        (DESIGNADO, "DESIGNADO"),
        (EM_ATENDIMENTO, "EM ATENDIMENTO"),
        (EM_ATENDIMENTO_RETORNO, "EM ATENDIMENTO DE RETORNO"),
        (CONCLUIDO, 'CONCLUIDO'),
        (OBITO, "OBITO"),
        (REVELIA, 'REVELIA'),
        (ENCERRADO_ENFERMAGEM, 'ENCERRADO PELA ENFERMAGEM'),
        (ENCERRADO_ALTA, 'ENCERRADO PELA ALTA'),   
        (ENCERRADO_RECEPCAO, 'ENCERRADO PELA RECEPÇÃO'),
        (ENCERRADO_SISTEMA, 'ENCERRADO PELO SISTEMA'),
        (TRANSFERENCIA, "TRANSFERÊNCIA"),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHAMADOS, default=EM_ESPERA, blank=True, null=True, help_text='situação Atual do Chamado')
    historico = HistoricalRecords()

    class Meta:
        verbose_name = 'Lista de Chamado Administração Procedimento'
        verbose_name_plural = '8 - Lista de Chamados Administrações de Procedimento'

    def __str__(self):
        return f'{self.pk} - {self.get_situacao_display()}'
    
    @hook("before_save", when="situacao", was=DESIGNADO, is_now=EM_ATENDIMENTO_RETORNO, has_changed=True)
    @hook("before_save", when="situacao", was=DESIGNADO, is_now=EM_ATENDIMENTO, has_changed=True)
    def save_historico_administracao_procedimento(self):
        HistoricoListaChamadoAdministracaoProcedimento.objects.create(
            lista_chamado_administracao_procedimento=self,
            situacao=self.situacao,
            enfermeiro=self.enfermeiro,
            tempo_espera=tempo_medio_espera_hora(self.classificacao_risco.updated_at)
        )
    
    @hook("before_save", when="situacao", was=EM_ESPERA, is_now=DESIGNADO, has_changed=True)
    @hook("before_save", when="contagem", has_changed=True)
    def save_chamar(self):
        from publicmanager.saude_cadastro.models import PainelChamada
        paineis = PainelChamada.objects.filter(unidade_saude=self.unidade_saude, setores__in=[self.sala.unidade_setor])

        channel_layer = get_channel_layer()

        for painel in paineis:
            group_name = f'painel_{painel.unidade_saude.slug.replace("-", "_")}_{painel.slug.replace("-", "_")}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'update_panel',
                    'contagem': self.contagem,
                    'paciente': self.classificacao_risco.paciente.nome_paciente,
                    'tipo_setor': 'PROCEDIMENTO',
                    'sala': self.sala.nome_sala,
                }
            )

class HistoricoListaChamadoAdministracaoProcedimento(BaseModel):
    lista_chamado_administracao_procedimento = models.ForeignKey(ListaChamadoAdministracaoProcedimento, on_delete=models.PROTECT)
    situacao = models.SmallIntegerField("Status", choices=ListaChamadoAdministracaoProcedimento.SITUACAO_CHAMADOS, default=ListaChamadoAdministracaoProcedimento.EM_ESPERA, blank=True, null=True, help_text='situação Atual do Chamado')
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    tempo_espera = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name = 'Histórico de Administração de Procedimentos'
        verbose_name_plural = 'Históricos de Administrações de Procedimentos'

    def __str__(self):
        return f'{self.id} - {self.lista_chamado_administracao_procedimento.classificacao_risco.paciente}'

class ReceitaAdministracaoProcedimento(BaseModel):
    paciente = models.ForeignKey('saude_atendimento.Paciente', on_delete=models.PROTECT)
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    lista_chamada_solicitacao = models.ForeignKey(ListaChamadoAdministracaoProcedimento, on_delete=models.PROTECT, blank=True, null=True)
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de Saúde',on_delete=models.PROTECT)
    arquivo = models.FileField("Arquivo", upload_to=documentacao_administracao_procedimento_path, blank=True, null=True)
    foto_receita = models.ImageField(blank=True, null=True, upload_to=documentacao_administracao_procedimento_foto_path)
    

    class Meta:
        verbose_name = 'Receita Procedimento'
        verbose_name_plural = '9 - Receitas do Procedimentos'

    def __str__(self):
        return f'{self.paciente}'

class AdministracaoProcedimento(BaseModel):
    receita_procedimento = models.ForeignKey(ReceitaAdministracaoProcedimento, on_delete=models.PROTECT)
    procedimento = models.ForeignKey('saude_cadastro.Procedimento', on_delete=models.PROTECT)
    quantidade = models.IntegerField("Quantidade", blank=True, null=True)
    justificativa = models.TextField('Justificativa', blank=True, null=True) 
    observacao = models.TextField('Observação', blank=True, null=True)

    class Meta:
        verbose_name = 'Administração de Procedimento'
        verbose_name_plural = '10 - Administração de Procedimento'

    def __str__(self):
        return f'{self.receita_procedimento}'

class SituacaoAdministracaoProcedimento(BaseModel):
    administracao_procedimento = models.ForeignKey(AdministracaoProcedimento, on_delete=models.PROTECT)
    enfermeiro = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    data_hora_execucao = models.DateTimeField(verbose_name='Data e hora da Execução', blank=True, null=True)

    SOLICITADO, REALIZADO, CANCELADO = range(3)
    SITUACAO_CHOICE = (
        (SOLICITADO, "SOLICITADO"),
        (REALIZADO, "REALIZADO"),
        (CANCELADO, "CANCELADO"),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICE, default=SOLICITADO)
    sequencial = models.IntegerField('Sequencial', blank=True, null=True)
    justificativa = models.TextField('Justificativa', blank=True, null=True)
    cancelou = models.BooleanField('Cancelou?', default=False)

    class Meta:
        verbose_name = 'Situação Administração Procedimentos'
        verbose_name_plural = '11 - Situações Administrações de Procedimentos'

    def __str__(self):
        return f'{self.administracao_procedimento} - {self.data_hora_execucao}'