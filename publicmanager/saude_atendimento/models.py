from django_lifecycle import hook
from django.utils import timezone
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta
from django.db import models, transaction
from channels.layers import get_channel_layer
from simple_history.models import HistoricalRecords
from smart_selects.db_fields import ChainedForeignKey

from publicmanager.middleware import get_current_user
from publicmanager.saude.templatetags.saude_extras import tempo_medio_espera_hora

from publicmanager.saude.models import UnidadeSaude
from publicmanager.autenticacao.models import Usuario
from publicmanager.comum.models import BaseModel, Estado, Municipio
from publicmanager.saude_farmacia.models import PrincipioAtivo, Medicamento
from publicmanager.saude_cadastro.models import Profissional, TipoClassificacaoRisco
from publicmanager.saude_enfermagem.models import ListaChamadaSolicitacaoAtendimento

def paciente_avatar_upload_to(instance, filename):
    return f"imagens/pacientes/{instance.nome_paciente}_{datetime.strftime(instance.created_at, '%Y_%m_%d_%H')}_{filename}"

def diagnostico_atendimento_path(instance, filename):
    return f"documentos/diagnosticos/{instance.pk}_{filename}"

def documentacao_paciente_path(instance, filename):
    return f"documentos/documentos_pacientes/{instance.pk}_{filename}"

def exame_atendimento_anexo_path(instance, filename):
    return f"documentos/exames/{instance.pk}_{filename}"

def procedimento_atendimento_anexo_path(instance, filename):
    return f"documentos/procedimentos/{instance.pk}_{filename}" 

class Paciente(BaseModel):
    SIM = 1
    NAO = 2
    SIM_NAO_CHOICES = [
        (SIM, 'Sim'),
        (NAO, 'Não')
    ]

    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de Saúde',on_delete=models.PROTECT, blank=True, null=True)
    cartao_sus = models.CharField('Cartão SUS', max_length=15, unique=True, blank=True, null=True, help_text='Cartão SUS', error_messages={'unique': 'Um paciente com esse número de cartão SUS já foi cadastrado.'})
    cpf = models.CharField(max_length=14, verbose_name="CPF", unique=True, blank=True, null=True, help_text='CPF', error_messages={'unique': 'Uma pessoa física com esse cpf já foi cadastrado.'})
    rg = models.CharField(max_length=20, blank=True, null=True, verbose_name='RG', help_text='RG')
    rg_orgao = models.CharField(max_length=10, blank=True, null=True, help_text='Orgão do RG')
    rg_uf = models.ForeignKey(Estado, blank=True, null=True, related_name='paciente_rg_uf_set', on_delete=models.CASCADE, help_text='UF da emissão do RG')
    rg_data = models.DateField(blank=True, null=True, help_text='Data da emissão do RG')
    situacao = models.CharField('Situação', max_length=7, choices=[['ATIVO', 'ATIVO'], ['INATIVO', 'INATIVO'], ['OBITO', 'ÓBITO']], default='ATIVO')
    
    # Informações Pessoais
    nome_paciente = models.CharField('Nome Paciente', max_length=200, help_text='Nome do paciente')
    data_nascimento = models.DateField(help_text='Data da nascimento')
    nome_social = models.CharField('Nome Social', max_length=200, blank=True, null=True, help_text='Nome social')
    foto_paciente = models.ImageField(blank=True, null=True, upload_to=paciente_avatar_upload_to)
    nome_mae = models.CharField('Nome da Mãe', max_length=100, help_text='Nome da mãe', blank=True, null=True)
    nome_pai = models.CharField('Nome do Pai', max_length=100, blank=True, null=True, help_text='Nome do pai')
    nacionalidade = models.CharField('Nacionalidade', max_length=255, help_text='Naturalidade', blank=True, null=True)
    naturalidade = models.CharField('Naturalidade', max_length=255, blank=True, null=True, help_text='Naturalidade')
    
    sexo = models.CharField(max_length=1, choices=[['M', 'Masculino'], ['F', 'Feminino']], help_text='Sexo')
    PARDA, PRETA, BRANCA, INDIGENA, AMARELA, OUTROS  = range(6)
    RACA_CHOICES = (
         (PARDA, "PARDA"),
         (PRETA, "PRETA"),
         (BRANCA, "BRANCA"),
         (INDIGENA, "INDIGENA"),
         (AMARELA, "AMARELA"),
         (OUTROS, "OUTROS")
    )
    raca = models.SmallIntegerField("Raça", choices=RACA_CHOICES, default=OUTROS, blank=True, null=True)
    SOLTEIRO, CASADO, DIVORCIADO, VIUVO, SEPARADO  = range(5)
    ESTADO_CIVIL_CHOICES = (
         (SOLTEIRO, "SOLTEIRO(A)"),
         (CASADO, "CASADO(A)"),
         (DIVORCIADO, "DIVORCIADO(A)"),
         (VIUVO, "VIÚVO(A)"),
         (SEPARADO, "SEPARADO(A)")
    )
    estado_civil = models.SmallIntegerField("Estado Civil", choices=ESTADO_CIVIL_CHOICES, blank=True, null=True)
    
    CRECHE, PRE_ESCOLA, CLASSE_ALFABETIZACAO, ENSINO_FUNDAMENTAL_PRIMEIRA_FASE, ENSINO_FUNDAMENTAL_SEGUNDA_FASE, \
    ENSINO_FUNDAMENTAL_DURACAO, ENSINO_FUNDAMENTAL_ESPECIAL, ENSINO_MEDIO_SEGUNDO_GRAU, ENSINO_MEDIO_ESPECIAL, ENSINO_FUNDAMENTAL_EJA_INICIAIS, \
    ENSINO_FUNDAMENTAL_EJA_FINAIS, ENSINO_MEDIO_EJA, SUPERIOR, ALFABETIZACAO_ADULTO, NENHUM= range(15)

    GRAU_DE_INSTRUCAO_CHOICES = [
        ['0', 'Creche'], 
        ['1', 'PRÉ-ESCOLA (EXCETO CA)'], 
        ['2', 'Classe de Alfabetização - CA'], 
        ['3', 'Ensino Fundamental 1ª a 4ª séries, Elementar (Primário], Primeira fase do 1º grau'], 
        ['4', 'Ensino Fundamental 5ª a 8ª séries, Médio 1º ciclo (Ginasial], Segunda fase do 1º grau '], 
        ['5', 'Ensino Fundamental (duração 9 anos)'],
        ['6', ' Ensino Fundamental Especial'], 
        ['7', ' Ensino Médio, 2º grau, Médio 2º ciclo (Científico, Clássico, Técnico, Normal) '], 
        ['8', 'Ensino Médio Especial'],
        ['9', 'Ensino Fundamental EJA - séries iniciais (Supletivo 1ª a 4ª) '], 
        ['10', ' Ensino Fundamental EJA - séries finais (Supletivo 5ª a 8ª) '], 
        ['11', ' Ensino Médio EJA (Supletivo)'], 
        ['12', 'Superior, Aperfeiçoamento, Especialização, Mestrado, Doutorado'], 
        ['13', 'Alfabetização para Adultos (Mobral, etc.)'], 
        ['14', 'Nenhum'], 
    ]

    grau_de_instrucao =  models.CharField("Grau de instrução", choices=GRAU_DE_INSTRUCAO_CHOICES, blank=True, null=True)
    profissao = models.ForeignKey('saude_cadastro.Profissao', blank=True, null=True, on_delete=models.CASCADE, help_text='Profissão')
    grupo_sanguineo = models.CharField('Grupo Sanguíneo', max_length=2, blank=True, null=True, choices=[['A', 'A'], ['B', 'B'], ['AB', 'AB'], ['O', 'O']], help_text='Grupo Sanguíneo')
    fator_rh = models.CharField('Fator RH', max_length=8, blank=True, null=True, choices=[['+', '+'], ['-', '-']], help_text='Fator RH')
    doador_sanguineo = models.IntegerField(choices=SIM_NAO_CHOICES, blank=True, null=True)
    doador_de_orgaos = models.IntegerField(choices=SIM_NAO_CHOICES, blank=True, null=True)
    
    # Endereço
    cep = models.CharField(max_length=14, verbose_name="CEP", blank=True, null=True, help_text='CEP')
    endereco = models.CharField('Endereço', max_length=200, help_text='Nome da rua, travessa ou avenida', blank=True, null=True)
    numero = models.CharField('Número', max_length=10, blank=True, null=True)
    complemento = models.CharField('Complemento', blank=True, null=True, max_length=200, help_text='Complemento torre, sala etc')
    bairro = models.CharField('Bairro', max_length=200, help_text='Nome do bairro', blank=True, null=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, help_text='Estado', blank=True, null=True)
    municipio = ChainedForeignKey(Municipio, on_delete=models.CASCADE, chained_field='estado', chained_model_field='estado', show_all=False, auto_choose=False, blank=True, null=True)

    # Contato
    celular = models.CharField('Celular', max_length=15, blank=True, null=True, help_text='Celular')
    telefone_fixo = models.CharField('Telefone Fixo', max_length=14, unique=True, blank=True, null=True, help_text='Telefone Fixo')
    whatsapp = models.CharField('WhatsApp', max_length=15, unique=True, blank=True, null=True, help_text='WhatsApp')
    email = models.EmailField(verbose_name='E-mail', unique=True, blank=True, null=True, help_text='E-mail')
    
    # Responsavel
    nome_responsavel_1 = models.CharField('Nome do Responsável 1', max_length=200, blank=True, null=True, help_text='Nome do Responsável 1')
    parentesco_responsavel_1 = models.CharField('Parentesco do Responsável 1', max_length=300, blank=True, null=True, help_text='Parentesco do Responsável 1')
    cpf_responsavel_1 = models.CharField(max_length=14, verbose_name="CPF do Responsável 1", blank=True, null=True, help_text='CPF do Responsável 1')
    rg_responsavel_1 = models.CharField(max_length=20, null=True, verbose_name='RG', blank=True, help_text='RG do Responsável 1')
    celular_responsavel_1 = models.CharField('Celular do Responsável 1', max_length=15, blank=True, null=True, help_text='Celular do Responsável 1')
    whatsapp_responsavel_1 = models.CharField('WhatsApp do Responsável 1', max_length=15, blank=True, null=True, help_text='WhatsApp do Responsável 1')
    email_responsavel_1 = models.EmailField(verbose_name='E-mail do Responsável 1', blank=True, null=True, help_text='E-mail do Responsável 1')
    nome_responsavel_2 = models.CharField('Nome do Responsável 2', max_length=200, blank=True, null=True, help_text='Nome do Responsável 2')
    parentesco_responsavel_2 = models.CharField('Parentesco do Responsável 2', blank=True, null=True, max_length=300, help_text='Parentesco do Responsável 2')
    cpf_responsavel_2 = models.CharField(max_length=14, verbose_name="CPF do Responsável 2", blank=True, null=True, help_text='CPF do Responsável 1')
    rg_responsavel_2 = models.CharField(max_length=20, verbose_name='RG', blank=True, null=True, help_text='RG do Responsável 2')
    celular_responsavel_2 = models.CharField('Celular do Responsável 2', max_length=15, blank=True, null=True, help_text='Celular do Responsável 2')
    whatsapp_responsavel_2 = models.CharField('WhatsApp do Responsável 2', max_length=15, blank=True, null=True, help_text='WhatsApp do Responsável 1')
    email_responsavel_2 = models.EmailField(verbose_name='E-mail do Responsável 2', blank=True, null=True, help_text='E-mail do Responsável 2')
    
    anamnese_paciente = models.OneToOneField('AnamnesePaciente', null=True, blank=True, on_delete=models.PROTECT)
    historico = HistoricalRecords()

    def __str__(self):
        return f'{self.nome_paciente}'
    
    @property
    def formatar_nome_municipio(self):
        return f'{self.municipio.nome}/{self.municipio.estado.sigla}'
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "1 - Pacientes"

    @hook("before_create")
    def criar_anamnese_paciente(self):
            self.anamnese_paciente = AnamnesePaciente.objects.create()

    def calcular_idade(self, formato=None):
        data_nascimento_str = self.data_nascimento.strftime('%Y-%m-%d')

        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d')
        data_atual = datetime.now()

        idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))
        
        if formato:
            return f"{idade}"
        
        return f"{idade} Anos"
    
    def formatar_grupo_sanguineo(self):
        return f"{self.grupo_sanguineo} {self.fator_rh}"

class AnamnesePaciente(BaseModel):
    tem_doenca_neurologica = models.BooleanField("Tem doença neurológica?", default=False)
    tem_doenca_psicologica = models.BooleanField("Tem doença psicológica?", default=False)
    tem_hipertensao_arterial = models.BooleanField("Tem hipertensão arterial?", default=False)
    tem_doenca_do_sangue = models.BooleanField("Tem doença do sangue?", default=False)
    fez_recebeu_transfusao_ultimos_3_meses = models.BooleanField("Fez ou recebeu transfusão nos últimos 3 meses?", default=False)
    teve_avc_derrame = models.BooleanField("Teve AVC / derrame?", default=False)
    estar_com_tuberculose = models.BooleanField("Está com tuberculose?", default=False)
    estar_com_hanseniase = models.BooleanField("Está com hanseníase?", default=False)
    estar_fumante = models.BooleanField("Está fumante?", default=False)
    faz_uso_alcool = models.BooleanField("Faz uso de álcool?", default=False)
    faz_uso_drogas = models.BooleanField("Faz uso de drogas?", default=False)
    faz_exercicio_fisicos = models.BooleanField("Faz exercício físicos?", default=False)
    ja_sofreu_infarto = models.BooleanField("Já sofreu infarto?", default=False)
    alergias_medicamentosas = models.ManyToManyField(PrincipioAtivo, blank=True, related_name="alergias_medicamentosas")
    antecedentes_patologicos_pessoais = models.ManyToManyField('saude_cadastro.CID', blank=True, related_name="antecedentes_patologicos_pessoais")
    antecedentes_patologicos_familiares = models.ManyToManyField('saude_cadastro.CID', blank=True, related_name="antecedentes_patologicos_familiares")
    
    ABAIXO_PESO, PESO_ADEQUADO, ACIMA_PESO = range(3)
    SITUACAO_PESO_CHOICES = [
        (ABAIXO_PESO, 'Abaixo do peso'),
        (PESO_ADEQUADO, 'Peso adequado'),
        (ACIMA_PESO, 'Acima do peso'),
    ]
    situacao_peso =  models.SmallIntegerField("Situação do Peso", choices=SITUACAO_PESO_CHOICES, blank=True, null=True)
    tem_alguma_deficiencia = models.BooleanField("Acima do peso", default=False)
    descricao_deficiencia = models.CharField('Descrição de deficiência', max_length=200, help_text='Descrição de deficiência', blank=True)
    estar_gestante = models.BooleanField("Está gestante?", default=False)
    periodo_gestacao = models.CharField('Período da gestação?', max_length=200, help_text='Período da gestação?', blank=True)
    tem_diabetes = models.BooleanField("Tem diabetes?", default=False)
    tipo_diabetes = models.CharField('Descrição de diabetes', max_length=200, help_text='Descrição de diabetes', blank=True)
    tem_doenca_respiratoria_cronica_pulmao = models.BooleanField("Tem doença respiratória crônica / no pulmão?", default=False)
    nome_doenca_respiratoria_cronica_pulmao = models.CharField('Descrição de doença respiratória crônica / no pulmão', max_length=200, help_text='Descrição de doença respiratória crônica / no pulmão', blank=True)
    tem_doenca_cardiaca_do_coracao = models.BooleanField("Tem doença nos rins?", default=False)
    nome_doenca_cardiaca_do_coracao = models.CharField('Descrição de doença nos rins', max_length=200, help_text='Descrição de doença nos rins', blank=True)
    tem_doenca_rins = models.BooleanField("Tem doença nos rins?", default=False)
    nome_doenca_rins = models.CharField('Descrição de doença nos rins', max_length=200, help_text='Descrição de doença nos rins', blank=True)
    tem_teve_cancer = models.BooleanField("Tem ou teve câncer?", default=False)
    tipo_cancer = models.CharField('Descrição câncer',max_length=200,help_text='Descrição câncer', blank=True)
    teve_alguma_internacao_ultimos_12_meses = models.BooleanField("Teve alguma internação nos últimos 12 meses?", default=False)
    causa_internacao_ultimos_12_meses = models.CharField('Causa da internação nos últimos 12 meses', max_length=200, help_text='Causa da internação nos últimos 12 meses', blank=True)
    usa_plantas_medicinais = models.BooleanField("Usa plantas medicinais?", default=False)
    nome_planta_medicinal = models.CharField('Descrição plantas medicinais', max_length=200, help_text='Descrição plantas medicinais', blank=True)
    
    # Anamnese respostas humanas sociais
    frequenta_cuidador_tradicional = models.BooleanField("Frequenta cuidador tradicional?",default=False)
    participa_de_algum_grupo_comunitario = models.BooleanField("Participa de algum grupo comunitário?", default=False)
    possui_plano_saude_privado = models.BooleanField("Possui plano de saúde privado?",default=False)
    nome_beneficio = models.CharField('Nome do beneficio recebido', max_length=200, blank=True)
    recebe_algum_beneficio = models.BooleanField("Recebe algum benefício?",default=False)
    eh_membro_povo_comunidade_tradicional = models.BooleanField("É membro de povo ou comunidade tradicional?", default=False)
    nome_povo_comunidade_tradicional = models.CharField('Descrição povo ou comunidade tradicional', max_length=200, help_text='Descrição povo ou comunidade tradicional', blank=True)
    
    # Anamnese respotas humanas em situação de rua
    MENOS_DE_SEIS_MESES, SEIS_A_DOZE_MESES, UM_A_CINCO_ANOS, MAIS_DE_5_ANOS = range(4)
    TEMPO_SITUACAO_DE_RUA_CHOICES = [
        (MENOS_DE_SEIS_MESES, '< 6 meses'),
        (SEIS_A_DOZE_MESES, '6 a 12 meses'),
        (UM_A_CINCO_ANOS, '1 a 5 anos'),
        (MAIS_DE_5_ANOS, '> 5 anos'),
    ]
    tempo_situacao_de_rua = models.SmallIntegerField("Tempo situação de rua", choices=TEMPO_SITUACAO_DE_RUA_CHOICES, blank=True, null=True)
    eh_acompanhado_por_outra_instituicao = models.BooleanField("É acompanhado por outra instituição?", default=False)
    nome_instituicao = models.CharField('Nome da outra instituição', max_length=200, help_text='Nome da outra instituição', blank=True,)
    possui_referencia_familiar = models.BooleanField("Possui referência familiar?", default=False)
    visita_algum_familiar_com_frequencia = models.BooleanField("Visita algum familiar com frequência?", default=False)
    grau_parentesco = models.CharField('Grau de parentesco', max_length=200, help_text='Grau de parentesco', blank=True)
    
    UMA_VEZ, DUAS_OU_TRES_VEZES, MAIS_DE_3_VEZES = range(3)
    FREQUENCIA_DIARIA_ALIMENTACAO_CHOICES = [
        (UMA_VEZ, '1 vez'),
        (DUAS_OU_TRES_VEZES, '2 ou 3 vezes'),
        (MAIS_DE_3_VEZES, 'mais de 3 vezes'),
    ]
    frequencia_diaria_alimentacao = models.SmallIntegerField("Frequência diária alimentação", choices=FREQUENCIA_DIARIA_ALIMENTACAO_CHOICES, blank=True, null=True)
    
    # Restaurante
    restaurante_popular = models.BooleanField("Restaurante popular?",default=False)
    doacao_restaurante = models.BooleanField("Doação de restaurante?",default=False)
    doacao_grupo_religioso = models.BooleanField("Doação de grupo religioso?",default=False)
    doacao_popular = models.BooleanField("Doação popular?",default=False)
    doacao_outros = models.BooleanField("Outras doações?",default=False)
    
    # Higiene Pessoal
    tem_acesso_a_higiene_pessoal = models.BooleanField("Tem acesso a higiene pessoal?",default=False)
    higiene_pessoal_banho = models.BooleanField("Banho?",default=False)
    higiene_pessoal_higiene_bocal = models.BooleanField("Higiene bocal?",default=False)
    higiene_pessoal_acesso_sanitario = models.BooleanField("Acesso sanitário?",default=False)
    higiene_outros = models.BooleanField("Outras higienes?",default=False)
    
    historico = HistoricalRecords()

    class Meta:
        verbose_name = 'Anamnese de paciente'
        verbose_name_plural = '1 - pacientes Anamneses'
    
    def __str__(self):
        return f'{self.paciente_nome} - {self.id} {self.created_at.strftime("%d/%m/%Y %H:%m") }'

    @property
    def paciente_nome(self):
        if Paciente.objects.filter(anamnese_paciente=self).exists():
            return self.paciente.nome_paciente
        
        return None
    
class DocumentoPaciente(BaseModel):
    profissional = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, blank=True, null=True)
    arquivo = models.FileField("Arquivo", upload_to=documentacao_paciente_path, blank=True, null=True)
    nome = models.CharField('Nome', max_length=100, blank=True, null=True)
    descricao = models.TextField('Descrição', blank=True, null=True)

    def __str__(self):
        return f'{self.paciente} - {self.nome}'
    
    class Meta:
        verbose_name = "Documento do Paciente"
        verbose_name_plural = "1 - Pacientes - Documentos"

class BoletimPaciente(BaseModel):
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', null=True, blank=True, on_delete=models.PROTECT)
    profissional = models.ForeignKey('saude_cadastro.Profissional', related_name='profissional_boletim_paciente_set', on_delete=models.PROTECT, blank=True, null=True)
    paciente = models.ForeignKey(Paciente, related_name='paciente_boletim_set', on_delete=models.PROTECT)
    data_entrada = models.DateTimeField("Data de Entrada")
    data_saida = models.DateTimeField("Data de Saída", blank=True, null=True)
    nome_responsavel = models.CharField("Nome do Responsável", max_length=255, blank=True)
    rg_responsavel = models.CharField("RG do Responsável", max_length=255, blank=True)

    EM_ABERTO, EM_ANDAMENTO, CURADO, OBITO, REVELIA, MELHORADO, INALTERADO, \
    TRANSFERENCIA, DECISAO_MEDICA, ENCERRAMENTO_ADMINISTRATIVO, ENCERRADO_SISTEMA = range(11)
    SITUACAO_BOLETIM_CHOICES = (
        (EM_ABERTO, "EM ABERTO"),
        (EM_ANDAMENTO, "EM ANDAMENTO"),
        (CURADO, 'CURADO'),
        (OBITO, 'ÓBITO'),
        (REVELIA, 'REVELIA'),
        (MELHORADO, 'MELHORADO'),
        (INALTERADO, 'INALTERADO'),
        (TRANSFERENCIA, 'TRANSFERÊNCIA'),
        (DECISAO_MEDICA, 'DECISÃO MÉDICA'),
        (ENCERRAMENTO_ADMINISTRATIVO, 'ENCERRAMENTO ADMINISTRATIVO'),
        (ENCERRADO_SISTEMA, 'ENCERRADO PELO SISTEMA'),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_BOLETIM_CHOICES, default=EM_ABERTO)
    
    URGENCIA, MEDICACAO = range(2)
    TIPO_CHOICES = (
        (URGENCIA, "URGÊNCIA"),
        (MEDICACAO, "ADMINISTRAÇÃO MEDICAMENTO"),
    )
    tipo = models.SmallIntegerField("Tipo", choices=TIPO_CHOICES, default=URGENCIA)
    historico = HistoricalRecords()

    def __str__(self):
        return f'{self.id} - {self.paciente}'
    
    class Meta:
        verbose_name = "Boletim do Paciente"
        verbose_name_plural = "1 - Pacientes Boletins"

    @hook("after_create")
    def atualizar_classificacao_risco(self):
        channel_layer = get_channel_layer()

        group_name = f'atualizar_listagem_classificacao'
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'update_listagem',
                'paciente': self.paciente.nome_paciente,
                'tipo_setor': 'classificacao',
            }
        )

class ListaChamadaClassificacaoRisco(BaseModel):
    boletim = models.ForeignKey(BoletimPaciente, verbose_name='Boletim do Paciente',on_delete=models.PROTECT)
    sala = models.ForeignKey('saude_cadastro.Sala', on_delete=models.PROTECT, blank=True, null=True)
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de Saúde',on_delete=models.PROTECT)
    profissional = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    contagem = models.IntegerField('Contagem', default=1, blank=True, null=True)

    CHAMADO, EM_ATENDIMENTO, CLASSIFICADO, CANCELADO = range(4)
    SITUACAO_CHOICES = (
        (CHAMADO, "CHAMADO"),
        (EM_ATENDIMENTO, "EM ATENDIMENTO"),
        (CLASSIFICADO, "CLASSIFICADO"),
        (CANCELADO, "CANCELADO"),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICES, default=CHAMADO)
    historico = HistoricalRecords()
    class Meta:
        verbose_name = '2 - Lista de Espera da Classificação de Risco'
        verbose_name_plural = '2 - Lista de Espera da Classificação de Risco'

    def __str__(self):
        return f'{self.id} - {self.boletim}'
    

    @hook("after_create")
    @hook("after_save", when="contagem", has_changed=True)
    def atualizar_lista_espera(self):
        from publicmanager.saude_cadastro.models import PainelChamada

        channel_layer = get_channel_layer()

        paineis = PainelChamada.objects.filter(unidade_saude=self.unidade_saude, setores__in=[self.sala.unidade_setor])

        for painel in paineis:
            group_name = f'painel_{painel.unidade_saude.slug.replace("-", "_")}_{painel.slug.replace("-", "_")}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'update_panel',
                    'contagem': self.contagem,
                    'paciente': self.boletim.paciente.nome_paciente,
                    'tipo_setor': self.sala.unidade_setor.get_tipo_display(),
                    'sala': self.sala.nome_sala,
                }
            )

class ClassificacaoRisco(BaseModel):
    # Estado Geral
    paciente = models.ForeignKey(Paciente, related_name='paciente_classificacao_risco_set', on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, related_name='profissional_classificacao_risco_set', on_delete=models.PROTECT, blank=True, null=True)
    boletim = models.ForeignKey(BoletimPaciente, verbose_name="Boletim", related_name='boletim_classificacao_risco_set', blank=True, null=True, on_delete=models.CASCADE)
    data_hora_avaliacao = models.DateTimeField('Data da avaliação', help_text='Data e hora da avaliação')
    queixa_principal = models.TextField('Queixa Principal', blank=True, null=True)
    peso = models.DecimalField('Peso', max_digits=9, decimal_places=3, blank=True, null=True)
    altura = models.DecimalField('Altura', max_digits=9, decimal_places=2, blank=True, null=True)

    LEVE, MODERADA, INTENSA, SEM_DOR = range(4)
    ESCALA_COR_CHOICES = (
        (LEVE, "LEVE"),
        (MODERADA, "MODERADA"),
        (INTENSA, 'INTENSA'),
        (SEM_DOR, 'SEM DOR')
    )
    escala_dor = models.SmallIntegerField("Escala de dor", choices=ESCALA_COR_CHOICES)

    TRIAGEM, ATENDIMENTO_MEDICO = range(2)
    TIPO_SETOR_CHOICES = (
        (TRIAGEM, "TRIAGEM"),
        (ATENDIMENTO_MEDICO, "ATENDIMENTO MÉDICO"),
    )
    setor = models.SmallIntegerField("Setor", choices=TIPO_SETOR_CHOICES, default=TRIAGEM)

    ATIVO, DESABILITADO = range(2)
    TIPO_STATUS_CHOICES = (
        (ATIVO, "ATIVO"),
        (DESABILITADO, "DESABILITADO"),
    )
    status = models.SmallIntegerField("Status", choices=TIPO_STATUS_CHOICES, default=ATIVO)
    reclassificacao = models.BooleanField("Reclassificação?", default=False)

    AGITACAO, APARENTEMENTE_BEM, CONSCIENTE, CONVULSAO, DISPNEIA_INTERNA, GRAVE, \
    ORIENTADO, POLITRAUMATIZADO, PRECORDIALGIAS, REGULAR, SINAIS_DE_AGRAVAMENTO= range(11)
    ESTADO_GERAL_CHOICES = (
        (AGITACAO, "AGITAÇÃO"),
        (APARENTEMENTE_BEM, "APARENTEMENTE BEM"),
        (CONSCIENTE, 'CONSCIENTE'),
        (CONVULSAO, "CONVULSÃO"),
        (DISPNEIA_INTERNA, "DISPNEIA INTERNA"),
        (GRAVE, 'GRAVE'),
        (ORIENTADO, 'ORIENTADO'),
        (POLITRAUMATIZADO, "POLITRAUMATIZADO"),
        (PRECORDIALGIAS, "PRECORDIALGIAS"),
        (REGULAR, 'REGULAR'),
        (SINAIS_DE_AGRAVAMENTO, 'SINAIS DE AGRAVAMENTO')
    )
    estado_geral = models.SmallIntegerField("Estado geral", choices=ESTADO_GERAL_CHOICES)
    observacao = models.TextField("Descrição", blank=True, null=True)
    
    # Sinais Vitais
    presao_arterial = models.CharField('Presão arterial', max_length=10, blank=True, null=True)
    frequencia_cardiaca = models.IntegerField('Frequêcia cardiaca', blank=True, null=True)
    frequencia_respiratoria = models.IntegerField('Frequêcia respiratória', blank=True, null=True)
    temperatura = models.DecimalField('temperatura', max_digits=9, decimal_places=2, blank=True, null=True)
    spo2 = models.CharField('SPO2', max_length=255, blank=True, null=True)
    hgt = models.CharField('HGT', max_length=255, blank=True, null=True)
    tipo_classificacao_risco = models.ForeignKey('saude_cadastro.TipoClassificacaoRisco', on_delete=models.PROTECT)
    
    TIPO_NUMERO_CHOICE = (
        ('CON', "ATENDIMENTO AMBULATORIAL"),
        ('BAU', "ATENDIMENTO DE URGÊNCIA"),
        ('AIH', "INTERNAÇÃO"),
        ('ENF', "ATENDIMENTO DE INFERMAGEM")
    )
    tipo_atendimento = models.CharField(choices=TIPO_NUMERO_CHOICE, max_length=3, blank=True, null=True)
    numero_atendimento = models.BigIntegerField('Número Atendimento', blank=True, null=True)

    FLUXO_URGENCIA, FLUXO_PROCEDIMENTO = range(2)
    TIPO_FLUXO_CHOICES = (
        (FLUXO_URGENCIA, "URGÊNCIA"),
        (FLUXO_PROCEDIMENTO, "PROCEDIMENTOS ELETIVO"),
    )
    tipo_fluxo = models.SmallIntegerField("Tipo Fluxo", choices=TIPO_FLUXO_CHOICES, default=FLUXO_URGENCIA)

    historico = HistoricalRecords()
    class Meta:
        verbose_name = 'Classificação de Risco'
        verbose_name_plural = '2 - Classificações de Risco'

    def __str__(self):
        return f'{self.paciente}'
    
    @property
    def formatar_numeros_atendimento(self):
        return f"{self.tipo_atendimento}{str(self.numero_atendimento).zfill(12)}"
    

    @hook("after_create")
    def atualizar_atendiemnto_medico(self):
        channel_layer = get_channel_layer()
        
        group_name = f'atualizar_listagem_medico'
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'update_listagem',
                'paciente': self.paciente.nome_paciente,
                'tipo_setor': 'atendimento_medico',
            }
        )
    

    @transaction.atomic
    @hook("after_create")
    def criar_numero_atendimento(self):
        if not self.reclassificacao:
            ultima_instancia = ClassificacaoRisco.objects.filter(
                tipo_atendimento=self.tipo_atendimento,
                boletim__unidade_saude=self.boletim.unidade_saude,
            ).exclude(id=self.id).order_by('-numero_atendimento').select_for_update().first()

            ultimo_atendimento = ultima_instancia.numero_atendimento if ultima_instancia else 0

            self.numero_atendimento = ultimo_atendimento + 1
            self.save()

class ListaChamada(BaseModel):
    sala = models.ForeignKey('saude_cadastro.Sala', related_name='sala_lista_chamada_set', on_delete=models.PROTECT)
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de Saúde',on_delete=models.PROTECT)
    paciente = models.ForeignKey(Paciente, related_name='paciente_lista_chamada_set', on_delete=models.PROTECT)
    medico = models.ForeignKey('saude_cadastro.Profissional', related_name='medico_lista_chamada_set', on_delete=models.PROTECT, blank=True, null=True)
    classificacao_risco = models.OneToOneField(ClassificacaoRisco, related_name='classificacao_risco_lista_chamada_set', on_delete=models.CASCADE)
    contagem = models.IntegerField('Contagem', default=1, blank=True, null=True)
    
    EM_ESPERA, EM_ATENDIMENTO, EM_PROCEDIMENTO, RETORNO, EM_ATENDIMENTO_RETORNO, ENCERRADO_ATENDIMENTO, ENCERRADO_ALTA, \
    ENCERRADO_RECEPCAO, ENCERRADO_SISTEMA, LISTA_RETORNO, ATENDIMENTO_REABERTO = range(11)
    SITUACAO_CHAMADOS = (
        (EM_ESPERA, "EM ESPERA"),
        (EM_ATENDIMENTO, "EM ATENDIMENTO"),
        (EM_PROCEDIMENTO, "EM PROCEDIMENTO"),
        (RETORNO, "RETORNO"),
        (EM_ATENDIMENTO_RETORNO, "EM ATENDIMENTO DE RETORNO"),
        (ENCERRADO_ATENDIMENTO, 'ENCERRADO PELO ATENDIMENTO'),
        (ENCERRADO_ALTA, 'ENCERRADO PELA ALTA'),   
        (ENCERRADO_RECEPCAO, 'ENCERRADO PELA RECEPÇÃO'),
        (ENCERRADO_SISTEMA, 'ENCERRADO PELO SISTEMA'),
        (LISTA_RETORNO, "LISTA DE RETORNO"),
        (ATENDIMENTO_REABERTO, "ATENDIMENTO REABERTO"),
    )
    situacao = models.SmallIntegerField("Status", choices=SITUACAO_CHAMADOS, default=EM_ESPERA, blank=True, null=True, help_text='situação Atual do Chamado')
    historico = HistoricalRecords()
    class Meta:
        verbose_name = 'Lista de CHamado'
        verbose_name_plural = '3 - Lista de Chamados'

    def __str__(self):
        return f'{self.id} - {self.paciente}'
    
    @hook("before_create")
    @hook("before_save", when="situacao", has_changed=True)
    def save_historico_espera_atendimento(self):
        historico = HistoricoEsperaAtendimento.objects.filter(lista_chamada=self).order_by('-created_at').first()
        
        usuario_logado = get_current_user()
        profissional = Profissional.objects.filter(user=usuario_logado).first()
        
        if historico:
            HistoricoEsperaAtendimento.objects.create(
                lista_chamada=self,
                situacao=self.situacao,
                tempo_espera=tempo_medio_espera_hora(historico.created_at),
                profissional=profissional
            )
        else:
            HistoricoEsperaAtendimento.objects.create(
                lista_chamada=self,
                situacao=self.situacao,
                tempo_espera=tempo_medio_espera_hora(self.classificacao_risco.created_at),
                profissional=profissional
            )
    
    @hook("before_create")
    @hook("before_save", when="contagem", has_changed=True)
    @hook("before_save", when="situacao", was=LISTA_RETORNO, is_now=RETORNO, has_changed=True)
    def save_chamar(self):
        from publicmanager.saude_cadastro.models import PainelChamada

        channel_layer = get_channel_layer()

        paineis = PainelChamada.objects.filter(unidade_saude=self.unidade_saude, setores__in=[self.sala.unidade_setor])

        for painel in paineis:
            group_name = f'painel_{painel.unidade_saude.slug.replace("-", "_")}_{painel.slug.replace("-", "_")}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'update_panel',
                    'contagem': self.contagem,
                    'paciente': self.paciente.nome_paciente,
                    'tipo_setor': 'urgência',
                    'sala': self.sala.nome_sala,
                }
            )

class HistoricoEsperaAtendimento(BaseModel):
    lista_chamada = models.ForeignKey(ListaChamada, on_delete=models.PROTECT)
    situacao = models.SmallIntegerField("Status", choices=ListaChamada.SITUACAO_CHAMADOS, default=ListaChamada.EM_ESPERA, blank=True, null=True, help_text='situação Atual do Chamado')
    tempo_espera = models.DurationField(blank=True, null=True)
    profissional = models.ForeignKey(Profissional, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = 'Histórico de Tempo de Espera do Atendimeto'
        verbose_name_plural = 'Histórico de Tempo de Espera do Atendimeto'

    def __str__(self):
        return f'{self.id} - {self.lista_chamada.paciente}'

class AtendimentoMedico(BaseModel):
    profissionais = models.ManyToManyField('saude_cadastro.Profissional', blank=True)
    paciente = models.ForeignKey(Paciente, related_name='paciente_atendimento_medico_set', on_delete=models.PROTECT)
    classificacao_risco = models.ManyToManyField(ClassificacaoRisco, blank=True)
    lista_chamada = models.OneToOneField(ListaChamada, related_name='lista_chamada_atendimento_medico_set', on_delete=models.PROTECT)
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de Saúde',on_delete=models.PROTECT, blank=True, null=True)
    class Meta:
        verbose_name = 'Atendimento Médico'
        verbose_name_plural = '4 - Atendimentos Médicos'

    def __str__(self):
        return f'{self.paciente}'

class ReaberturaAtendimentoMedico(BaseModel):
    atendimento = models.ForeignKey(AtendimentoMedico, on_delete=models.PROTECT)
    profissional = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT)
    justificativa = models.TextField('justificativa')

    class Meta:
        verbose_name = 'Reabertura Atendimento Médico'
        verbose_name_plural = '4 - Reaberturas Atendimento Médico'

    def __str__(self):
        return f'{self.atendimento.paciente}'

class AtestadoAtendimento(BaseModel):
    atendimento = models.ForeignKey(AtendimentoMedico, on_delete=models.PROTECT)
    profissional = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    quantidade = models.IntegerField('Quantidade')
    cid = models.ForeignKey('saude_cadastro.CID', on_delete=models.PROTECT, blank=True, null=True )

    class Meta:
        verbose_name = 'Atestado Atendimento'
        verbose_name_plural = '5 - Atendimentos Atestados'

    def __str__(self):
        return f'{self.atendimento}'
    
class FichaReferenciaAtendimento(BaseModel):
    atendimento = models.ForeignKey(AtendimentoMedico, on_delete=models.PROTECT)
    profissional = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    resumo_clinico = models.TextField('resumo_clinico', blank=True, null=True)
    diagnosticos = models.ManyToManyField('DiagnosticoAtendimento', blank=True)
    exames = models.ManyToManyField('ExameAtendimento', blank=True)
    medicacoes = models.ManyToManyField('MedicacaoAtendimento', blank=True) 

    class Meta:
        verbose_name = 'Ficha Referência'
        verbose_name_plural = '7 - Fichas de Referência'

    def __str__(self):
        return f'{self.atendimento}'

class EvolucaoAtendimento(BaseModel):
    atendimento = models.ForeignKey(AtendimentoMedico, related_name='atendimento_evolucao_atendimento_set', on_delete=models.PROTECT)
    profissional = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    registro_evolucao = models.TextField('Resgistro da Evolução')
    retorno = models.BooleanField('Com Retorno?', default=False)
    numero_evolucao = models.IntegerField('Numero', blank=True, null=True)

    class Meta:
        verbose_name = 'Evolução Atendimento'
        verbose_name_plural = '4 - Atendimentos Evoluções'

    def __str__(self):
        return f'{self.atendimento}'
    
    @property
    def formatar_numero_evolucao(self):
        numero = self.numero_evolucao if self.numero_evolucao else 0

        return str(numero).zfill(12)
    
    @hook("after_create")
    def criar_numero_evolucao_incremental(self):
        ultima_instancia = EvolucaoAtendimento.objects.filter(
            atendimento=self.atendimento,
            numero_evolucao__isnull=False
        ).exclude(id=self.id).order_by('-numero_evolucao').first()

        ultimo_atendimento = ultima_instancia.numero_evolucao if ultima_instancia else 0

        self.numero_evolucao = int(ultimo_atendimento) + 1
        self.save()  
     
class DiagnosticoAtendimento(BaseModel):
    atendimento = models.ForeignKey(AtendimentoMedico, related_name='atendimento_diagnostico_atendimento_set', on_delete=models.PROTECT)
    profissional = models.ForeignKey('saude_cadastro.Profissional', on_delete=models.PROTECT, blank=True, null=True)
    descricao = models.TextField('Descrição', blank=True, null=True)
    cid = models.ForeignKey('saude_cadastro.CID', related_name='cid_diagnostico_atendimento_set', on_delete=models.PROTECT)
    nome_arquivo =  models.CharField('Nome do Anexo', max_length=255, blank=True, null=True)
    arquivo = models.FileField("Arquivo", upload_to=diagnostico_atendimento_path, blank=True, null=True)
    numero_diagnostico = models.IntegerField('Numero', blank=True, null=True)

    class Meta:
        verbose_name = 'Diagnostico Atendiemnto'
        verbose_name_plural = '4 - Atendimentos Diagnósticos'

    def __str__(self):
        return f'{self.id} - {self.cid}'
    
    @property
    def formatar_numero_diagnostico(self):
        return str(self.numero_diagnostico).zfill(12)
    
    @hook("after_create")
    def criar_numero_diagnostico_incremental(self):
        ultima_instancia = DiagnosticoAtendimento.objects.filter(
            atendimento=self.atendimento,
        ).exclude(id=self.id).order_by('-numero_diagnostico').first()

        ultimo_atendimento = ultima_instancia.numero_diagnostico if ultima_instancia else 0

        self.numero_diagnostico = ultimo_atendimento + 1
        self.save()  

class ExameAtendimento(BaseModel):
    atendimento = models.ForeignKey(AtendimentoMedico, related_name='atendimento_exame_atendimento_set', on_delete=models.PROTECT)
    medico_solicitante = models.ForeignKey('saude_cadastro.Profissional', related_name='medico_solicitante_exame_atendimento_set', on_delete=models.PROTECT, blank=True, null=True)
    profissional_responsavel = models.ForeignKey('saude_cadastro.Profissional', related_name='profissional_responsavel_exame_atendimento_set', on_delete=models.PROTECT, blank=True, null=True)
    exame = models.ForeignKey('saude_cadastro.Exame', on_delete=models.PROTECT)
    observacao = models.TextField('Observação')

    SOLICITADO, ANEXADO, SEM_ANEXO, REABERTURA = range(4)
    SITUACAO_CHOICES = (
        (SOLICITADO, "SOLICITADO"),
        (ANEXADO, "ANEXADO"),
        (SEM_ANEXO, "SEM ANEXO"),
        (REABERTURA, "REABERTURA"),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICES, default=SOLICITADO, blank=True, null=True)
    justificativa = models.TextField('justificativa', blank=True, null=True)
    arquivo = models.FileField("Arquivo", upload_to=exame_atendimento_anexo_path, blank=True, null=True)
    arquivo_nome = models.CharField('Nome', max_length=100, blank=True, null=True)
    lista_chamada_solicitacao = models.ForeignKey(ListaChamadaSolicitacaoAtendimento, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = 'Exame Atendimento'
        verbose_name_plural = '4 - Atendimentos Exames'

    def __str__(self):
        return f'{self.atendimento} - {self.id}'

class ArquivoExameAtendimento(BaseModel):
    exame_atendimento = models.ForeignKey(ExameAtendimento, related_name='arquivos', on_delete=models.PROTECT)
    arquivo = models.FileField("Arquivo", upload_to=exame_atendimento_anexo_path, blank=True, null=True)
    nome = models.CharField('Nome', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Arquivo de Exame Atendimento'
        verbose_name_plural = 'Arquivos de Exame Atendimento'

    def __str__(self):
        return f'{self.nome} - {self.exame_atendimento}'

class ProcedimentoAtendimento(BaseModel):
    atendimento = models.ForeignKey(AtendimentoMedico, related_name='atendimento_procedimento_atendimento_set', on_delete=models.PROTECT)
    medico_solicitante = models.ForeignKey('saude_cadastro.Profissional', related_name='medico_solicitante_procedimento_atendimento_set', on_delete=models.PROTECT, blank=True, null=True)
    profissional_responsavel = models.ForeignKey('saude_cadastro.Profissional', related_name='profissional_responsavel_procedimento_atendimento_set', on_delete=models.PROTECT, blank=True, null=True)
    procedimento = models.ForeignKey('saude_cadastro.Procedimento', on_delete=models.PROTECT)
    quantidade = models.IntegerField('Quantidade')
    arquivo = models.FileField("Arquivo", upload_to=procedimento_atendimento_anexo_path, blank=True, null=True)
    arquivo_nome = models.CharField('Nome', max_length=100, blank=True, null=True)

    PRINCIPAL, SECUNDARIO = range(2)
    CLASSIFICACAO_CHOICES = (
        (PRINCIPAL, "PRINCIPAL"),
        (SECUNDARIO, "SECUNDARIO")
    )
    classificacao = models.SmallIntegerField("Classificação", choices=CLASSIFICACAO_CHOICES)

    SOLICITADO, SUSPENSO, CONCLUIDO, REABERTURA = range(4)
    SITUACAO_CHOICES = (
        (SOLICITADO, "SOLICITADO"),
        (SUSPENSO, "SUSPENSO"),
        (CONCLUIDO, "CONCLUÍDO"),
        (REABERTURA, "REABERTURA"),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICES, default=SOLICITADO)

    INTERNO, EXTERNO = range(2)
    TIPO_SOLICITACAO_CHOICES = (
        (INTERNO, "INTERNO"),
        (EXTERNO, "EXTERNO")
    )
    tipo_solicitacao = models.SmallIntegerField("Tipo da Solicitação", choices=TIPO_SOLICITACAO_CHOICES, default=INTERNO)
    
    ENFERMAGEM, MEDICO = range(2)
    RESPONSAVEL_CHOICES = (
        (ENFERMAGEM, "ENFERMAGEM"),
        (MEDICO, "MÉDICO"),
    )
    realizado_por = models.SmallIntegerField("Realizado por", choices=RESPONSAVEL_CHOICES, default=ENFERMAGEM)
    
    justificativa = models.TextField('justificativa', blank=True, null=True)
    lista_chamada_solicitacao = models.ForeignKey(ListaChamadaSolicitacaoAtendimento, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = 'Procedimento do atendimento'
        verbose_name_plural = '4 - atendimentos Procedimentos'

    def __str__(self):
        return f'{self.atendimento}'

class ArquivoProcedimentoAtendimento(BaseModel):
    procedimento_atendimento = models.ForeignKey(ProcedimentoAtendimento, related_name='arquivos', on_delete=models.PROTECT)
    arquivo = models.FileField("Arquivo", upload_to=procedimento_atendimento_anexo_path, blank=True, null=True)
    nome = models.CharField('Nome', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Arquivo de Procedimento Atendimento'
        verbose_name_plural = 'Arquivos de Procedimento Atendimento'

    def __str__(self):
        return f'{self.nome} - {self.procedimento_atendimento}'
    
class JustificativaProcedimentoAtendimento(BaseModel):
    atendimento = models.ForeignKey(AtendimentoMedico, on_delete=models.PROTECT, blank=True, null=True)
    profissional = models.ForeignKey(Profissional, on_delete=models.PROTECT, blank=True, null=True)
    procedimentos = models.ManyToManyField(ProcedimentoAtendimento, blank=True)
    diagnostico = models.ForeignKey('saude_cadastro.CID', related_name='diagnostico_justificativa_procedimento_set', on_delete=models.PROTECT)
    cid_10_principal = models.ForeignKey('saude_cadastro.CID', related_name='cid_10_principal_justificativa_procedimento_set', on_delete=models.PROTECT)
    cid_10_secundario = models.ForeignKey('saude_cadastro.CID', related_name='cid_10_secundario_justificativa_procedimento_set', on_delete=models.PROTECT, blank=True, null=True)
    cid_10_causa_associada = models.ForeignKey('saude_cadastro.CID', related_name='cid_10_causas_associada_justificativa_procedimento_set', on_delete=models.PROTECT, blank=True, null=True)
    observacao = models.TextField('Observação')

    class Meta:
        verbose_name = 'Justificativa Procedimento Atendimento'
        verbose_name_plural = 'Justificativas Procedimentos Atendimentos'

    def __str__(self):
        return f'{self.atendimento}'

class TipoAltaHospitalar(BaseModel):
    ATIVO = 'ATIVO'
    INATIVO = 'INATIVO'
    SITUACOES_CHOICES = [
        (ATIVO, 'ATIVO'),
        (INATIVO, 'INATIVO'),
    ]

    nome = models.CharField('Nome', unique=True, max_length=50)
    situacao = models.CharField('Situação', max_length=7, choices=SITUACOES_CHOICES, default=ATIVO)

    class Meta:
        verbose_name = 'Tipos de Alta Hospitalar'
        verbose_name_plural = 'Tipo de Alta Hospitalar'

    def __str__(self):
        return f'{self.situacao}'
    
class MedicacaoAtendimento(BaseModel):
    atendimento = models.ForeignKey(AtendimentoMedico, on_delete=models.PROTECT)
    medico = models.ForeignKey('saude_cadastro.Profissional', related_name='medico_medicacao_atendomento_set', on_delete=models.PROTECT, blank=True, null=True)
    
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

    IMEDIATA, POSTERIOR = range(2)
    TIPO_APLICACAO = (
        (IMEDIATA, "IMEDIATA"),
        (POSTERIOR, "POSTERIOR"),
    )
    aplicacao = models.SmallIntegerField("Aplicação", choices=TIPO_APLICACAO, blank=True, null=True)
    dosagem = models.CharField('Dosagem', max_length=30, blank=True, null=True)
    medicacao = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    dose_unica = models.BooleanField('Dose Única?', default=True)
    medicamento_controlado = models.BooleanField('Medicamento Controlado?', default=False)
    posologia = models.CharField('Posologia', blank=True, null=True)

    HORAS, MINUTOS = range(2)
    TIPO_POSOLOGIA = (
        (HORAS, "HORAS"),
        (MINUTOS, "MINUTOS"),
    )
    tipo_posologia = models.SmallIntegerField("Tipo Posologia", choices=TIPO_POSOLOGIA, blank=True, null=True)
    uso_continuo = models.BooleanField('Uso contínuo?', default=False)
    duracao_tratamento = models.IntegerField('Duração do Tratamento', blank=True, null=True)
    observacao = models.TextField('Observação', blank=True, null=True)

    SOLICITADO, PARCIALMENTE_APLICADO, SUSPENSO, CONCLUIDO, REABERTURA = range(5)
    SITUACAO_CHOICES = (
        (SOLICITADO, "SOLICITADO"),
        (PARCIALMENTE_APLICADO, "PARCIALMENTE APLICADO"),
        (SUSPENSO, "SUSPENSO"),
        (CONCLUIDO, "CONCLUÍDO"),
        (REABERTURA, "REABERTURA"),
    )
    situacao = models.SmallIntegerField("Situação", choices=SITUACAO_CHOICES, default=SOLICITADO)
    lista_chamada_solicitacao = models.ForeignKey(ListaChamadaSolicitacaoAtendimento, on_delete=models.PROTECT, blank=True, null=True)
    estoque_zero = models.BooleanField('Confirmar com estoque zerado?', default=False)
    class Meta:
        verbose_name = 'Medicação do Atendimento'
        verbose_name_plural = '4 - Atendimentos Medicações'

    def __str__(self):
        return f'{self.atendimento} - {self.medicacao}'
    

    def calcular_proxima_dosagem(self):
        if self.situacao == MedicacaoAtendimento.SOLICITADO and not self.dose_unica:
            medicacao_com_data_minima = self.situacaomedicacaoatendimento_set.order_by('-data_hora_aplicacao').first()

            if medicacao_com_data_minima:
                posologia_parts = medicacao_com_data_minima.medicacao_atendimento.posologia.split('/')
                intervalo_entre_doses = int(posologia_parts[0])
                
                menor_data_hora_local = timezone.localtime(medicacao_com_data_minima.data_hora_aplicacao)

                if self.tipo_posologia == self.HORAS:
                    proxima_dose_time = menor_data_hora_local + timedelta(hours=intervalo_entre_doses)
                elif self.tipo_posologia == self.MINUTOS:
                    proxima_dose_time = menor_data_hora_local + timedelta(minutes=intervalo_entre_doses)

                return proxima_dose_time
            
            return None 

#Consultório
class HorarioMedico(models.Model):
    medico_horariomedico = models.ForeignKey(Profissional, verbose_name='Médico', on_delete=models.CASCADE)
    
    DOMINGO, SEGUNDA, TERCA, QUARTA, QUINTA, SEXTA, SABADO = range(7)
    DIA_SEMANA_CHOICES = [
        (SEGUNDA, 'Segunda'),
        (TERCA, 'Terça'),
        (QUARTA, 'Quarta'),
        (QUINTA, 'Quinta'),
        (SEXTA, 'Sexta'),
        (SABADO, 'Sábado'),
        (DOMINGO, 'Domingo'),
    ]
    dia_semana_horariomedico = models.IntegerField(choices=DIA_SEMANA_CHOICES, default=SEGUNDA)
    hora_inicial_horariomedico = models.TimeField()
    hora_final_horariomedico = models.TimeField()
    class Meta:
        verbose_name = 'Horário Médico'
        verbose_name_plural = 'Horários Médico'
    
    def __str__(self):
        return f'{self.medico_horariomedico}: {self.dia_semana_horariomedico}({self.hora_inicial_horariomedico} - {self.hora_final_horariomedico})'

class AgendamentoConsultorio(models.Model):
    unidade_saude = models.ForeignKey(UnidadeSaude, verbose_name='Unidade de Saúde',on_delete=models.PROTECT, null=True, blank=True)
    paciente = models.ForeignKey(Paciente, null=True, blank=True, verbose_name='Paciente', on_delete=models.CASCADE)
    nome_paciente = models.CharField('Nome do Paciente', max_length=200, help_text='Nome do Paciente')
    cpf_paciente = models.CharField(max_length=14, verbose_name="CPF", help_text='CPF', blank=True, null=True)
    celular_paciente = models.CharField('Celular', max_length=15, blank=True, null=True, help_text='Celular')
    telefone_fixo_paciente = models.CharField('Telefone Fixo', max_length=14, blank=True, null=True, help_text='Telefone Fixo')
    medico = models.ForeignKey(Profissional, verbose_name='Médico', on_delete=models.CASCADE)
    agendado_por = models.ForeignKey(Usuario, verbose_name='Agendado por', on_delete=models.CASCADE)
    
    PRIMEIRO_ATENDIMENTO, EXTRA_ENCAIXE, RETORNO = range(3)
    TIPO_ATENDIMENTO_CHOICES = [
        (PRIMEIRO_ATENDIMENTO, 'Primeiro atendimento'),
        (EXTRA_ENCAIXE, 'Extra encaixe'),
        (RETORNO, 'Retorno'),
    ]
    
    tipo_atendimento = models.IntegerField(choices=TIPO_ATENDIMENTO_CHOICES, default=PRIMEIRO_ATENDIMENTO)
    data_atendimento = models.DateField(blank=True, null=True, )
    hora_inicio_atendimento = models.TimeField(blank=True, null=True, )
    hora_termino_atendimento = models.TimeField(blank=True, null=True, )
    observacoes = models.TextField(blank=True, null=True, )

    class Meta:
        verbose_name = 'Agenda Médica'
        verbose_name_plural = 'Agenda Médica'

    def __str__(self):
        # nome_paciente - medico - tipo_atendimento - data_atendimento - hora_inicio_atendimento
        return self.nome_paciente
    
class Feriado(models.Model):
    nome_feriado = models.CharField('Nome do Feriado', max_length=200, help_text='Nome do Feriado')
    data_inicial = models.DateField()
    data_final = models.DateField()
    class Meta:
        verbose_name = 'feriado'
        verbose_name_plural = 'feriado'

    def __str__(self):
        return f'{self.nome_feriado}: {self.data_inicial} - {self.data_final}'

class BloqueioAgenda(models.Model):
    medico_bloqueio_agenda = models.ForeignKey(Profissional, verbose_name='Médico', on_delete=models.CASCADE)
    data_inicial = models.DateField()
    data_final = models.DateField()
    motivo = models.TextField()
    class Meta:
        verbose_name = 'Bloqueio Agenda'
        verbose_name_plural = 'Bloqueios Agenda'

    def __str__(self):
        return f'{self.medico}: {self.data_inicial} - {self.data_final}'

class PreAtendimentoMedico(BaseModel):
    # Estado Geral
    paciente = models.ForeignKey(Paciente, related_name='paciente_atendimento_set', on_delete=models.CASCADE)
    agendamento_atendimento = models.OneToOneField(AgendamentoConsultorio, verbose_name="Agendamento de atendimento", related_name='agendamento_atendimento_atendimento_set', blank=True, null=True, on_delete=models.CASCADE)
    data_entrada = models.DateTimeField("Data e hora de entrada", help_text='Data e hora do pré-atendimento')
    queixa_principal = models.TextField('Queixa Principal')
    peso = models.DecimalField('Peso', max_digits=5, decimal_places=3, blank=True, null=True)
    altura = models.DecimalField('Altura', max_digits=3, decimal_places=2, blank=True, null=True)

    escala_dor = models.SmallIntegerField("Escala de cor", choices=ClassificacaoRisco.ESCALA_COR_CHOICES, default=ClassificacaoRisco.LEVE)
    estado_geral = models.SmallIntegerField("Estado geral", choices=ClassificacaoRisco.ESTADO_GERAL_CHOICES, default=ClassificacaoRisco.AGITACAO)
    observacao = models.TextField("Descrição", blank=True)
    
    # Sinais Vitais
    # presao_arterial = models.DecimalField('Presão arterial', max_digits=9, decimal_places=2) #Tem que ser um CharField: 120/80 mm/Hg
    # frequencia_cardiaca = models.DecimalField('Frequêcia cardiaca', max_digits=9, decimal_places=2) # Tem que ser um IntegerField: 90 bpm
    # frequencia_respiratoria = models.DecimalField('Frequêcia respiratória', max_digits=9, decimal_places=2) # Tem que ser um IntegerField: 20 rpm
    # temperatura = models.DecimalField('Presão arterial', max_digits=5, decimal_places=2) # 36,5 °C
    # spo2 = models.CharField('SPO2', max_length=255) # Tem que ser um IntegerField: 95%
    # hgt = models.CharField('HGT', max_length=255, blank=True, null=True) # Tem que ser um IntegerField: 95%
    
    presao_arterial = models.CharField('Pressão arterial', max_length=7, help_text='Pressão arterial', blank=True) # 120/80 mm/Hg
    frequencia_cardiaca = models.PositiveIntegerField('Frequência Cardíaca', help_text='Frequência Cardíaca', blank=True, null=True) # 90 bpm
    frequencia_respiratoria = models.PositiveIntegerField('Frequência Respiratória', help_text='Frequência Respiratória', blank=True, null=True) # 20 rpm
    temperatura = models.DecimalField('Temperatur', max_digits=5, decimal_places=2, blank=True, null=True) # 36,5 °C
    spo2 = models.PositiveIntegerField('SpO2', help_text='SpO2', blank=True, null=True) # 95%
    hgt = models.PositiveIntegerField('hgt', help_text='hgt', blank=True, null=True) # 90mg/dL
    
    tipo_classificacao_risco = models.ForeignKey(TipoClassificacaoRisco, on_delete=models.PROTECT, blank=True, null=True)
    situacao = models.SmallIntegerField("Situação", choices=BoletimPaciente.SITUACAO_BOLETIM_CHOICES, default=BoletimPaciente.EM_ABERTO, blank=True)
    data_saida = models.DateTimeField("Data e hora de saída", help_text='Data e hora do término do atendimento', blank=True, null=True)
    

    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimento'

    def __str__(self):
        return f'{self.paciente} - {self.data_hora_pre_atendimento}'   
