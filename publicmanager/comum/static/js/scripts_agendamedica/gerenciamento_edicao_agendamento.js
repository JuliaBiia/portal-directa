const botaoEditarAgendamento = document.getElementById('editar-agendamento');
const removerAgendamento = document.getElementById('remover-agendamento');

let agendamentoID = "";


const preencherModalEdicaoDeAgendamento = dados => {
    document.getElementById("id_nome_paciente").value = dados.nome_paciente;
    document.getElementById("id_cpf_paciente").value = dados.cpf_paciente;
    document.getElementById("id_celular_paciente").value = dados.celular_paciente;
    document.getElementById("id_telefone_fixo_paciente").value = dados.telefone_fixo_paciente;

    mudarOptionSelected(
        document.querySelector('#agendamento_form #id_medico'),
        String(dados.medico_detalhes.id)
    )
    mudarOptionSelected(
        document.getElementById("id_agendado_por"),
        String(dados.agendado_por_detalhes.id)
    )

    document.querySelector(`#id_tipo_atendimento #id_tipo_atendimento_${dados.tipo_atendimento}`).checked = true

    const [inicioHora, inicioMinuto,] = dados.hora_inicio_atendimento.split(":")

    mudarOptionSelected(
        document.getElementById("inicio_hora"),
        inicioHora
    )
    mudarOptionSelected(
        document.getElementById("inicio_minuto"),
        inicioMinuto
    )

    const [terminoHora, terminoMinuto,] = dados.hora_termino_atendimento.split(":")
    mudarOptionSelected(
        document.getElementById("termino_hora"),
        terminoHora
    )
    mudarOptionSelected(
        document.getElementById("termino_minuto"),
        terminoMinuto
    )
    

    const [ano, mes, dia] = dados.data_atendimento.split("-")
    document.getElementById("id_data_atendimento").value = `${dia}/${mes}/${ano}`;
    
    document.getElementById("id_observacoes").value = dados.observacoes;
}

const desabilitarOsCamposModalEdicaoAgendamentoAtendimentoIgualOuPosteriorDataAtual = () => {
    document.getElementById('id_nome_paciente').setAttribute('disabled', 'disabled');
    if(document.getElementById('id_cpf_paciente').value){
        document.getElementById('id_cpf_paciente').setAttribute('disabled', 'disabled');
    } else{
        document.getElementById('id_cpf_paciente').removeAttribute('disabled', 'disabled');
    }

    document.getElementById('id_celular_paciente').removeAttribute('disabled');
    document.getElementById('id_telefone_fixo_paciente').removeAttribute('disabled');
    document.getElementById('id_tipo_atendimento').removeAttribute('disabled');
    document.getElementById('id_data_atendimento').removeAttribute('disabled');
    document.getElementById('inicio_hora').removeAttribute('disabled');
    document.getElementById('inicio_minuto').removeAttribute('disabled');
    document.getElementById('id_observacoes').removeAttribute('disabled');
}
const desabilitarOsCamposModalEdicaoAgendamentoAtendimentoAnteriorDataAtual = () => {
    document.getElementById('id_nome_paciente').setAttribute('disabled', 'disabled');
    document.getElementById('id_cpf_paciente').setAttribute('disabled', 'disabled');
    document.getElementById('id_celular_paciente').setAttribute('disabled', 'disabled');
    document.getElementById('id_telefone_fixo_paciente').setAttribute('disabled', 'disabled');
    document.getElementById('id_tipo_atendimento').setAttribute('disabled', 'disabled');
    document.getElementById('id_data_atendimento').setAttribute('disabled', 'disabled');
    document.getElementById('inicio_hora').setAttribute('disabled', 'disabled');
    document.getElementById('inicio_minuto').setAttribute('disabled', 'disabled');
    document.getElementById('id_observacoes').setAttribute('disabled', 'disabled');
}

const atendimentoOcorreHoje = (dataAtendimento, dataAtual) => dataAtendimento.getTime() === dataAtual.getTime()

const dataDoAtendimentoJaPassou = (dataAtendimento, dataAtual) => dataAtendimento < dataAtual

const renderizarModalEdicaoAgendamentoAtendimento = async agendamentoID => {
    botaoAgendarAtendimento.style.display = 'none';
    botaoEditarAgendamento.style.display = 'block';
    cancelarAgendamentoAtendimento.style.display = 'none';
    removerAgendamento.style.display = 'flex';


    const agendamento = await getAgendamentoConsultorio(agendamentoID);

    document.getElementById('id_remocao_agendamento').value = agendamento.id;

    document.querySelector(".campo-paciente").style.display = 'none';
    preencherModalEdicaoDeAgendamento(agendamento);
    
    ajustarSelectModal();
    ajustarSelectMedicoModalAgendamentoConsultorio();


    let dataAtendimento = agendamento.data_atendimento.split('-');
    dataAtendimento = new Date(dataAtendimento[0], dataAtendimento[1]-1, dataAtendimento[2]);

    const dataAtual = new Date()

    dataAtendimento.setHours(0,0,0,0);
    dataAtual.setHours(0,0,0,0);

    const aDataDaCelulaEhAnteriorADataAtual = verificarSeADataDaCelulaEhAnteriorADataAtualSemConsiderarHora(new Date(), dataAtendimento);

    if (aDataDaCelulaEhAnteriorADataAtual) {
        desabilitarOsCamposModalEdicaoAgendamentoAtendimentoAnteriorDataAtual();
    } else{
        desabilitarOsCamposModalEdicaoAgendamentoAtendimentoIgualOuPosteriorDataAtual();
    }

    const dia = String(dataAtendimento.getDate()).padStart(2, '0');
    const mes = String(dataAtendimento.getMonth() + 1).padStart(2, '0');
    const ano = dataAtendimento.getFullYear();

    const quantidadeAgendamentosConsultorioPorTipo = await getQuantidadeAgendamentosConsultorioPorTipo(agendamento.medico_detalhes.id, [dia, mes, ano]);
    
    document.querySelector("#container-primeiro-atendimento > #valor-primeiro-atendimento").innerHTML = quantidadeAgendamentosConsultorioPorTipo[0];
    document.querySelector("#container-retorno > #valor-retorno").innerHTML = quantidadeAgendamentosConsultorioPorTipo[1];
    document.querySelector("#container-extra-encaixe > #valor-extra-encaixe").innerHTML = quantidadeAgendamentosConsultorioPorTipo[2];
    
    preAtendimento.style.display = atendimentoOcorreHoje(dataAtendimento, dataAtual) ? 'flex' : 'none';

    if(dataDoAtendimentoJaPassou(dataAtendimento, dataAtual)){
        botaoEditarAgendamento.style.display = "none";
        removerAgendamento.style.display = "none";
    } else{
        botaoEditarAgendamento.style.display = "flex";
        removerAgendamento.style.display = "flex";
    }

    modalDeAgendamentoAtendimento.style.display = "block"
}


// botaoEditarAgendamento.addEventListener('click', () => {
//     document.querySelector('#agendamento_form #id_medico').removeAttribute('disabled', 'disabled');
//     document.getElementById('id_agendado_por').removeAttribute('disabled', 'disabled');
//     document.getElementById('termino_hora').removeAttribute('disabled', 'disabled');
//     document.getElementById('termino_minuto').removeAttribute('disabled', 'disabled');

//     document.getElementById('id_nome_paciente').removeAttribute('disabled', 'disabled');
//     document.getElementById('id_cpf_paciente').removeAttribute('disabled', 'disabled');
//     document.getElementById('id_celular_paciente').removeAttribute('disabled', 'disabled');
//     document.getElementById('id_telefone_fixo_paciente').removeAttribute('disabled', 'disabled');
//     document.getElementById('id_tipo_atendimento').removeAttribute('disabled', 'disabled');
//     document.getElementById('id_data_atendimento').removeAttribute('disabled', 'disabled');
//     document.getElementById('inicio_hora').removeAttribute('disabled', 'disabled');
//     document.getElementById('inicio_minuto').removeAttribute('disabled', 'disabled');
//     document.getElementById('id_observacoes').removeAttribute('disabled', 'disabled');

//     const dadosForm = getFormModalEdicaoAgendamentoConsultorio();

//     editAgendamentoConsultorio(agendamentoID, dadosForm, agendamentoForm)
// });

removerAgendamento.addEventListener('click', e => {
    const mensagemConfirmacao = "Deseja realmente remover este agendamento de atendimento?";
    // Sugestão de melhoria: Deseja realmente desagendar este atendimento?

    const callbackConfirmacao = () => {
        document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-body div > #confirmacao-remocao").removeEventListener('click', () => {

        })

        document.getElementById('modal-confirmacao-remocao').style.display = "none";

        const agendamentoID = document.getElementById('id_remocao_agendamento').value;
        deleteAgendamentoConsultorio(agendamentoID);
    }
    
    confirmarRemocao(mensagemConfirmacao, callbackConfirmacao);
})