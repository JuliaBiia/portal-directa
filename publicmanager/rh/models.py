from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.
from publicmanager.comum.models import Estado, Nacionalidade, Deficiencia, EstadoCivil, Banco, Pais, Raca, Municipio

from publicmanager.autenticacao.models import Usuario


class PessoaFisica(models.Model):
    user = models.OneToOneField(Usuario, null=True, blank=True, on_delete=models.CASCADE)
    nome_usual = models.CharField('Nome Usual', max_length=30, blank=True,
                                  help_text='O nome apresentado no crachá')
    nome_social = models.CharField('Nome Social', max_length=200, blank=True)
    nome_registro = models.CharField('Nome de Registro', max_length=200, blank=True)
    email = models.EmailField(blank=True, verbose_name='E-mail Principal', unique=True,
                              error_messages={'unique': 'Uma email idêntico já foi cadastrado.'})
    email_secundario = models.EmailField(blank=True, verbose_name='E-mail Secundário',
                                         help_text='E-mail utilizado para recuperação de senha.')
    website = models.URLField(blank=True)
    cpf = models.CharField(max_length=14, verbose_name="CPF", unique=True,
                           error_messages={'unique': 'Uma pessoa física com esse cpf já foi cadastrado.'})
    sexo = models.CharField(max_length=1, null=True, choices=[['M', 'Masculino'], ['F', 'Feminino']])
    grupo_sanguineo = models.CharField('Grupo Sanguíneo', max_length=2, null=True, blank=True,
                                       choices=[['A', 'A'], ['B', 'B'], ['AB', 'AB'], ['O', 'O']])
    fator_rh = models.CharField('Fator RH', max_length=8, null=True, blank=True, choices=[['+', '+'], ['-', '-']])
    titulo_numero = models.CharField(max_length=13, null=True, blank=True)
    titulo_zona = models.CharField(max_length=3, null=True, blank=True)
    titulo_secao = models.CharField(max_length=4, null=True, blank=True)
    titulo_uf = models.ForeignKey(Estado, related_name='estado_titulo_uf_set', on_delete=models.CASCADE)
    titulo_data_emissao = models.DateField(null=True)
    rg = models.CharField(max_length=20, null=True, verbose_name='RG')
    rg_orgao = models.CharField(max_length=10, null=True)
    rg_data = models.DateField(null=True)
    rg_uf = models.ForeignKey(Estado, related_name='estado_rg_uf_set', on_delete=models.CASCADE)
    nascimento_municipio = models.ForeignKey(Municipio, null=True, blank=True, verbose_name='Município',
                                             on_delete=models.CASCADE)
    nascimento_data = models.DateField('Data de Nascimento', null=True)
    nome_mae = models.CharField('Nome da Mãe', max_length=100, null=True)
    nome_pai = models.CharField('Nome do Pai', max_length=100, null=True, blank=True)
    """foto = ImageWithThumbsField(storage=OverwriteStorage(), use_id_for_name=True, upload_to='fotos', sizes=((75, 100), (150, 200)), null=True, blank=True)"""
    cnh_registro = models.CharField(max_length=10, null=True, blank=True)
    cnh_categoria = models.CharField(max_length=10, null=True, blank=True)
    cnh_emissao = models.DateField(null=True, blank=True)
    cnh_uf = models.ForeignKey(Estado, related_name='estado_cnh_uf_set', on_delete=models.CASCADE)
    cnh_validade = models.DateField(null=True, blank=True)
    ctps_numero = models.CharField(max_length=20, null=True, blank=True)
    ctps_uf = models.ForeignKey(Estado, related_name='estado_ctps_uf_set', on_delete=models.CASCADE)
    ctps_data_prim_emprego = models.DateField(null=True, blank=True)
    ctps_serie = models.CharField(max_length=10, null=True, blank=True)
    pis_pasep = models.CharField(max_length=20, null=True, blank=True, verbose_name='PIS / PASEP')
    pagto_banco = models.ForeignKey(Banco, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Banco')
    pagto_agencia = models.CharField(max_length=20, null=True, blank=True, verbose_name='Agência')
    pagto_ccor = models.CharField(max_length=20, null=True, blank=True, verbose_name='Conta')
    pagto_ccor_tipo = models.CharField(max_length=2, blank=True, null=True, verbose_name='Tipo')
    estado_civil = models.ForeignKey(EstadoCivil, null=True, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, null=True, on_delete=models.CASCADE)

    nacionalidade = models.IntegerField('Nacionalidade', choices=Nacionalidade.get_choices(), null=True)
    pais_origem = models.ForeignKey(Pais, verbose_name='País de Origem', null=True,
                                    on_delete=models.CASCADE)  # para estrangeiro

    deficiencia = models.ForeignKey(Deficiencia, verbose_name='Deficiência', blank=True, null=True, on_delete=models.CASCADE)
    lattes = models.URLField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.cpf, self.nome_social)


class PessoaJuridica(models.Model):
    razao_social = models.CharField('Razão Social', max_length=200, help_text='Nome da razão social')
    nome_fantasia = models.CharField('Nome Fantasia', max_length=200, help_text='Nome Fantasia do fornecedor')

    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", unique=True,
                            error_messages={'unique': 'Uma pessoa jurídica com esse cnpj já foi cadastrado.'})

    ramo_de_atividade = models.CharField('Ramo de atividade', max_length=200, help_text='Ramo de atividade')

    nome_do_representante_legal = models.CharField('Nome do representante legal', max_length=200)

    email = models.EmailField(blank=True, verbose_name='E-mail Principal da Empresa', unique=True,
                              error_messages={'unique': 'Uma email idêntico já foi cadastrado.'})

    inscricao_estadual = models.CharField('Inscrição Estadual', max_length=9)

    website = models.URLField()

    nome_contato_1 = models.CharField('Nome Contato 1', max_length=200, help_text='Descrição do contato 1')
    telefone_contato_1 = models.CharField('Telefone Contato 1', max_length=15,
                                          help_text='Número do telefone do contato 1')
    email_contato_1 = models.EmailField(blank=True, verbose_name='E-mail Contato 1', unique=True,
                                        error_messages={'unique': 'Uma email idêntico já foi cadastrado.'})
    funcao_contato_1 = models.CharField('Função Contato 1', max_length=200, help_text='Exemplo: Diretor de Marketing')

    nome_contato_2 = models.CharField('Nome Contato 2', max_length=200, help_text='Descrição do contato 2')
    telefone_contato_2 = models.CharField('Telefone Contato 2', max_length=15,
                                          help_text='Número do telefone do contato 2')
    email_contato_2 = models.EmailField(blank=True, verbose_name='E-mail Contato 2', unique=True,
                                        error_messages={'unique': 'Uma email idêntico já foi cadastrado.'})
    funcao_contato_2 = models.CharField('Função Contato 2', max_length=200, help_text='Exemplo: Diretor de Marketing')

    descricao = models.CharField('Descrição', max_length=200,
                                 help_text='Nome filial, unidade para identificação de mais um endereço')
    cep = models.CharField(max_length=14, verbose_name="CEP", unique=True)
    municipio = models.ForeignKey(Municipio, verbose_name='Município',
                                  on_delete=models.CASCADE)
    uf = models.ForeignKey(Estado, related_name='estado_pessoajuridica_uf_set', on_delete=models.CASCADE)
    endereco = models.CharField('Endereço', max_length=200, help_text='Nome da rua, travessa ou avenida')
    numero = models.PositiveIntegerField('Número', blank=True, null=True,  help_text='Número', validators=[MaxValueValidator(9999999999999)])
    complemento = models.CharField('Complemento', blank=True, null=True,  max_length=200, help_text='complemento torre, sala etc')
    bairro = models.CharField('Bairro', max_length=200, help_text='nome do barro')

    def __str__(self):
        return '{}'.format(self.nome_fantasia)


class CargoEmprego(models.Model):
    codigo = models.CharField(max_length=10, null=True, unique=True)
    descricao =models.CharField(max_length=40)
    nome_amigavel = models.CharField('Nome amigável', max_length=40, blank=True, null=False)
    descricao_sumaria = models.TextField(verbose_name="Descrição Sumária do Cargo", blank=True)
    excluido = models.BooleanField(default=False)

    class Meta:
        db_table = 'cargo_emprego'
        ordering = ['descricao']
        verbose_name = 'Cargo Emprego'
        verbose_name_plural = 'Cargos de Emprego'

    def __str__(self):
        return '{} - {}'.format(self.codigo, self.descricao)


class  Situacao(models.Model):
    codigo = models.CharField(max_length=10, null=True, unique=True)
    descricao =models.CharField(max_length=40)

    class Meta:
        db_table = 'situacao'
        verbose_name = 'Situação'
        verbose_name_plural = 'Situações'
        ordering = ['descricao']

    def __str__(self):
        return "{} - {}".format(self.descricao, self.codigo)


class JornadaTrabalho(models.Model):
    codigo = models.CharField(max_length=10, null=True, unique=True)
    descricao = models.CharField(max_length=40)
    carga_horaria = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.codigo} - {self.descricao} - {self.carga_horaria} HORAS'


class Funcao(models.Model):
    codigo = models.CharField(max_length=10, null=True, unique=True)
    descricao =models.CharField(max_length=40)

    class Meta:
        db_table = 'funcao'
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'

    def __str__(self):
        return self.descricao


class RegimeJuridico(models.Model):
    codigo_regime = models.CharField(max_length=2, null=True, db_index=True)
    sigla = models.CharField(max_length=10, null=True, unique=True)
    descricao =models.CharField(max_length=40)

    class Meta:
        db_table = 'regime_juridico'

    def __str__(self):
        return self.descricao


class NivelEscolaridade(models.Model):
    descricao =models.CharField(max_length=45)
    codigo = models.CharField(max_length=10, null=True, unique=True)

    class Meta:
        db_table = 'nivel_escolaridade'
        verbose_name = 'Nível de Escolaridade'
        verbose_name_plural = 'Níveis de Escolaridade'

    def __str__(self):
        return self.descricao

class SetorUnidade(models.Model):

    # Relacionamentos
    unidade_saude = models.ForeignKey('saude.UnidadeSaude', verbose_name='Unidade de saúde', on_delete=models.PROTECT)
    setor_superior = models.ForeignKey('self', null=True, blank=True, verbose_name='Setor Superior', on_delete=models.PROTECT)

    ATIVO, INATIVO = range(2)
    SITUACAO_CHOICES = (
        (ATIVO, "ATIVO"),
        (INATIVO, "INATIVO"),
    )
    situacao_setor = models.SmallIntegerField('Situação', choices=SITUACAO_CHOICES, default=ATIVO)

    recebe_paciente = models.BooleanField(verbose_name='Recebe paciente', default=False)

    # Informações sobre o setor
    nome_setor = models.CharField('Nome', unique=True, error_messages={'unique': 'Um setor com esse nome já existe.'}, max_length=200)
    sigla_setor = models.CharField('Sigla', unique=True, error_messages={'unique': 'Um setor com essa sigla já existe.'}, max_length=15)
    codigo_setor = models.CharField('Código', unique=True, error_messages={'unique': 'Um setor com esse código já existe.'}, max_length=20)

    # recebe_paciente = models.BooleanField(verbose_name='Recebe paciente', default=False, help_text='Setores excluídos não farão parte das buscas e não devem possuir servidores')

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'

    def __str__(self):
        return '{} - {}'.format(self.nome_setor, self.codigo_setor)

class Servidor(models.Model):
    pessoa_fisica = models.ForeignKey(
        PessoaFisica,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Pessoa Física',

    )
    setor = models.ForeignKey(
        SetorUnidade,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='funcionarios',
        verbose_name='Setor em que está lotado',
    )

    matricula = models.CharField('Matrícula', max_length=20, unique=True, db_index=True)
    num_processo_aposentadoria = models.CharField(max_length=30, null=True, blank=True)
    numerador_prop_aposentadoria = models.CharField(max_length=20, null=True, blank=True)
    denominador_prop_aposentadoria = models.CharField(max_length=20, null=True, blank=True)

    data_inicio_servico_publico = models.DateField(null=True, blank=True)
    data_inicio_exercicio_na_instituicao = models.DateField(null=True, blank=True)
    data_posse_na_instituicao = models.DateField(null=True, blank=True)
    data_posse_no_cargo = models.DateField(null=True, blank=True)
    data_inicio_exercicio_no_cargo = models.DateField(null=True, blank=True)

    data_fim_servico_na_instituicao = models.DateField(null=True, blank=True)

    email_institucional = models.EmailField('Email Institucional', blank=True)

    alterado_em = models.DateTimeField(auto_now=True)

    cargo_emprego = models.ForeignKey(CargoEmprego, null=True, blank=True, on_delete=models.CASCADE)

    cargo_emprego_data_ocupacao = models.DateField(null=True, blank=True)
    cargo_emprego_data_saida = models.DateField(null=True, blank=True)
    situacao = models.ForeignKey(Situacao, null=False, verbose_name='Situação', on_delete=models.CASCADE)
    jornada_trabalho = models.ForeignKey(JornadaTrabalho, null=True, blank=True, on_delete=models.CASCADE)
    funcao = models.ForeignKey(Funcao, null=True, blank=True, on_delete=models.CASCADE)

    funcao_data_ocupacao = models.DateField(null=True, blank=True)
    funcao_data_saida = models.DateField(null=True, blank=True)
    regime_juridico = models.ForeignKey(RegimeJuridico, null=True, blank=True, on_delete=models.CASCADE)
    nivel_escolaridade = models.ForeignKey(NivelEscolaridade, null=True, blank=True, on_delete=models.CASCADE)
    setor_lotacao_data_ocupacao = models.DateField(null=True)

    setor_exercicio = models.ForeignKey(
        SetorUnidade, null=True, blank=True, on_delete=models.CASCADE, related_name='servidores_exercicio',
        verbose_name='Setor de Exercício'
    )

    titulo_secao = models.CharField(max_length=4, null=True, blank=True)