const modalDeAgendamentoAtendimento = document.querySelector('#modal-agendamento-atendimento');

const botaoFecharAgendamentoAtendimento = document.getElementById('fechar-modal-agendamento-atendimento');

const botaoAgendarAtendimento = document.getElementById('agendar-atendimento');
const cancelarAgendamentoAtendimento = document.getElementById('cancelar-agendamento-atendimento');
const preAtendimento = document.getElementById('pre-atendimento')

const agendamentoForm = document.getElementById('agendamento_form');

const selectHoraInicioAtendimento = document.getElementById('inicio_hora');
const selectMinutoInicioAtendimento = document.getElementById('inicio_minuto');
const selectHoraTerminoAtendimento = document.getElementById('termino_hora');
const selectMinutoTerminoAtendimento = document.getElementById('termino_minuto');

let dataCelulaInicioAtendimento = new Date();
let dataCelulaTerminConsulta = new Date();




const verificarSeADataDaCelulaEhAnteriorADataAtualSemConsiderarHora = (dataAtual, dataDaCelula) => { //
    if (dataDaCelula.getFullYear() < dataAtual.getFullYear()) {
        return true;
    } else if (dataDaCelula.getFullYear() > dataAtual.getFullYear()) {
        return false;
    } else { // dataDaCelula.getFullYear() === dataAtual.getFullYear()
        if (dataDaCelula.getMonth() < dataAtual.getMonth()) {
            return true;
        } else if (dataDaCelula.getMonth() > dataAtual.getMonth()) {
            return false;
        } else { // dataDaCelula.getMonth() === dataAtual.getMonth()
            if (dataDaCelula.getDate() < dataAtual.getDate()) {
                return true
            } else {
                return false
            }
        }
    }
}

const preencherSelectsDoHorarioInicioAtendimento = (dataCelulaInicioAtendimento, selects) => {
    const [ selectHoraInicioAtendimento, selectMinutoInicioAtendimento ] = selects;


    const horario_inicio = {
        hora: String(dataCelulaInicioAtendimento.getHours()).padStart(2, 0),
        minuto: String(dataCelulaInicioAtendimento.getMinutes()).padStart(2, 0)
    }

    mudarOptionSelected(
        selectHoraInicioAtendimento,
        horario_inicio.hora
    )
    mudarOptionSelected(
        selectMinutoInicioAtendimento,
        horario_inicio.minuto
    )
}

const retornarDataCelulaTerminoAtendimento = dataCelulaInicioAtendimento => { //
    const dataCelulaTerminoAtendimento = new Date(dataCelulaInicioAtendimento);
    dataCelulaTerminoAtendimento.setMinutes(dataCelulaInicioAtendimento.getMinutes() + 20);

    return dataCelulaTerminoAtendimento;
}

const preencherSelectsDoHorarioTerminoAtendimento = (dataCelulaTerminoAtendimento, selects) => {
    const [ selectHoraTerminoAtendimento, selectMinutoTerminoAtendimento ] = selects;


    const horario_termino = {
        hora: String(dataCelulaTerminoAtendimento.getHours()).padStart(2, 0),
        minuto: String(dataCelulaTerminoAtendimento.getMinutes()).padStart(2, 0)
    }
    
    mudarOptionSelected(
        selectHoraTerminoAtendimento,
        horario_termino.hora
    )
    mudarOptionSelected(
        selectMinutoTerminoAtendimento,
        horario_termino.minuto
    )
}

const ajustarSelectMedicoModalAgendamentoConsultorio = () => {
    $("#agendamento_form #id_medico").select2({
        "language": "pt",
        dropdownParent: $('.br-scrim-util')
    });
    
    aplicarEstilizacaoPadraoSelec2()
}

const atualizarDataCelulaInicioAtendimento = () => {
    dataCelulaInicioAtendimento.setHours(retornarOptionSelected(document.getElementById("inicio_hora")).value)
    dataCelulaInicioAtendimento.setMinutes(retornarOptionSelected(document.getElementById("inicio_minuto")).value)
}
const atualizarSelectsHorarioTermino = () => {
    atualizarDataCelulaInicioAtendimento()

    dataCelulaTerminoAtendimento = retornarDataCelulaTerminoAtendimento(dataCelulaInicioAtendimento);

    const selectsHorarioTerminoAtendimento = [selectHoraTerminoAtendimento, selectMinutoTerminoAtendimento];
    preencherSelectsDoHorarioTerminoAtendimento(dataCelulaTerminoAtendimento, selectsHorarioTerminoAtendimento);

    $("#select2-termino_hora-container")[0].innerHTML = String(dataCelulaTerminoAtendimento.getHours()).padStart(2, 0);
    $("#select2-termino_minuto-container")[0].innerHTML = String(dataCelulaTerminoAtendimento.getMinutes()).padStart(2, 0);
}


$('#inicio_hora').on("change", function () {
    atualizarSelectsHorarioTermino();
});
$('#inicio_minuto').on("change", function () {
    atualizarSelectsHorarioTermino();
});


botaoFecharAgendamentoAtendimento.addEventListener('click', () => {
    document.getElementById("modal-agendamento-atendimento").style.display = "none";
});

const habilitarCamposModalAgendamentos = () => {
    document.querySelector('#agendamento_form #id_medico').removeAttribute('disabled', 'disabled');
    document.getElementById('id_agendado_por').removeAttribute('disabled', 'disabled');
    document.getElementById('termino_hora').removeAttribute('disabled', 'disabled');
    document.getElementById('termino_minuto').removeAttribute('disabled', 'disabled');

    document.getElementById('id_nome_paciente').removeAttribute('disabled', 'disabled');
    document.getElementById('id_cpf_paciente').removeAttribute('disabled', 'disabled');
    document.getElementById('id_celular_paciente').removeAttribute('disabled', 'disabled');
    document.getElementById('id_telefone_fixo_paciente').removeAttribute('disabled', 'disabled');
    document.getElementById('id_tipo_atendimento').removeAttribute('disabled', 'disabled');
    document.getElementById('id_data_atendimento').removeAttribute('disabled', 'disabled');
    document.getElementById('inicio_hora').removeAttribute('disabled', 'disabled');
    document.getElementById('inicio_minuto').removeAttribute('disabled', 'disabled');
    document.getElementById('id_observacoes').removeAttribute('disabled', 'disabled');
}

document.getElementById("agendamento_form").addEventListener('submit', async e => {
    e.preventDefault();

    // habilitarCamposModalAgendamentos();

    const botaoAcionadorSubmit = e.submitter;

    if(botaoAcionadorSubmit.id === "agendar-atendimento"){
        const dadosForm = getFormModalAgendamentoConsultorio();

        addAgendamentoConsultorio(dadosForm, agendamentoForm);
    } else if(botaoAcionadorSubmit.id === "editar-agendamento"){
        const dadosForm = getFormModalEdicaoAgendamentoConsultorio();

        editAgendamentoConsultorio(agendamentoID, dadosForm, agendamentoForm);
    }
});