const despreencherModalAgendarAtendimento = dados => {
    document.getElementById("id_nome_paciente").value = "";
    document.getElementById("id_cpf_paciente").value = "";
    document.getElementById("id_celular_paciente").value = "";
    document.getElementById("id_telefone_fixo_paciente").value = "";

    document.querySelector("#id_tipo_atendimento #id_tipo_atendimento_0").checked = true;
    
    document.getElementById("id_observacoes").value = "";
}

const habilitarOsCamposModalAgendarAtendimento = () => {
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


// botaoAgendarAtendimento.addEventListener('click', async () => {
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

//     const dadosForm = getFormModalAgendamentoConsultorio();

//     addAgendamentoConsultorio(dadosForm, agendamentoForm)

// })


cancelarAgendamentoAtendimento.addEventListener('click', () => {
    agendamentosFiltroForm.submit();
});

$("#id_paciente").on("change", async function () { // Get the selected value
    let pacienteID = this.options[this.selectedIndex].value;

    if(pacienteID){
        try{
            dadosPaciente = await getPaciente(pacienteID);

            document.getElementById("id_nome_paciente").value = dadosPaciente.nome_paciente;

            if(dadosPaciente.cpf){
                document.getElementById("id_cpf_paciente").value = dadosPaciente.cpf;
            } else{
                document.getElementById("id_cpf_paciente").value = ""
            }

            if(dadosPaciente.celular){
                document.getElementById("id_celular_paciente").value = dadosPaciente.celular;
            } else{
                document.getElementById("id_celular_paciente").value = ""
            }

            if(dadosPaciente.telefone_fixo){
                document.getElementById("id_telefone_fixo_paciente").value = dadosPaciente.telefone_fixo;
            } else{
                document.getElementById("id_telefone_fixo_paciente").value = "";
            }
        } catch (error){
            if(Object.keys(error).find(element => element === "status-code")){
                if(error["status-code"] === 400 || error["status-code"] === 404){
                    mostrarNotificaoErro(error['status-message']);
                } else{
                    mostrarNotificaoErro(error);
                }
            } else{
                mostrarNotificaoErro(error);
            }
        }
    } else{
        document.getElementById("id_nome_paciente").value = "";
        document.getElementById("id_cpf_paciente").value = "";
        document.getElementById("id_celular_paciente").value = "";
        document.getElementById("id_telefone_fixo_paciente").value = "";
    }
}
);