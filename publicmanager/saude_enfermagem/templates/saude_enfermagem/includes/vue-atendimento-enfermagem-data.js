paciente: {
    id: '{{object.atendimento.paciente.id}}',
    nome: '{{object.atendimento.paciente.nome_paciente}}',
    cpf: '{{object.atendimento.paciente.cpf}}',
    sus: '{{object.atendimento.paciente.cartao_sus}}',
    idade: '{{object.atendimento.paciente.calcular_idade}}',
    situacao: '{{object.atendimento.lista_chamada.get_situacao_display}}',
    foto: '{% if object.atendimento.paciente.foto_paciente %}{{object.atendimento.paciente.foto_paciente.url}}{% endif %}',
    sexo: '{% if object.atendimento.paciente.sexo == "M" %} MASCULINO {% elif object.atendimento.paciente.sexo == "F" %} FEMININO {% endif %} ',
    classificacaoRisco: '{{object.atendimento.lista_chamada.classificacao_risco.tipo_classificacao_risco.tipo}}',
    atendimentoPK: '{{object.atendimento.pk}}',
},
ultimoAtendimento: {
    data: '{{ultimo_atendimento.created_at}}',
    classificacaoTipo: '{% if ultimo_atendimento.boletim_classificacao_risco_set %}{{ultimo_atendimento.boletim_classificacao_risco_set.tipo_classificacao_risco.tipo}}{% endif %}',
    queixa: '{% if ultimo_atendimento.boletim_classificacao_risco_set %}{{ultimo_atendimento.boletim_classificacao_risco_set.queixa_principal}}{% endif %}',
    boletimSituacao: '{{ultimo_atendimento.get_situacao_display}}',
    profissionais: [
        {% if ultimo_atendimento.boletim_classificacao_risco_set.classificacao_risco_atendimento_medico_set.first %}
            {% for profissional in ultimo_atendimento.boletim_classificacao_risco_set.classificacao_risco_atendimento_medico_set.first.profissionais.all %}
                {nome: '{{profissional.nome_profissional}}'},
            {% endfor %}
        {% endif %}
    ],
},
objectPk: '{{object.pk}}',
listagemAplicacoes: [],
detalhesTimeLine: null