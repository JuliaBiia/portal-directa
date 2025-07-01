const getAgendamentoConsultorio = agendamentoID => {
    return new Promise (async (resolve, reject) => {
        try{
            // const resp = await fetch(`/atendimento/agendamedica/${agendamentoID}/`);
            const resp = await fetch(url_api_detalhe_agendamento.replace("123", agendamentoID))

            if (resp.status === 200){
                const data = await resp.json();

                resolve(data)
            } else if (resp.status === 404){
                reject({'status-code': 404, 'status-message': "Não foi possível encontrar o agendamento para ser removido. Entre em contato com o suporte para eles verificarem o motivo do problema."});
            }
        } catch(err){
            reject({'status-code': 400, 'status-message': `Erro ao obter dados do agendamento de id ${agendamentoID}: ${err}`});
        }
    })
};

const getQuantidadeAgendamentosConsultorioPorTipo = (medicoID, dataAtendimento) => {
    const [ ano, mes, dia ] = dataAtendimento;

    return new Promise (async (resolve, reject) => {
        try{
            const resp = await fetch(`/atendimento/api/agendamedica/obterqtdatendimentodomedicoportipo/?medico_id=${medicoID}&data_atendimento=${dia}-${mes}-${ano}`);

            if (resp.status === 200){
                const data = await resp.json();

                resolve(data)
            } else if (resp.status === 404){
                reject({'status-code': 404, 'status-message': `Não foi possível encontrar agendamentos para a data ${dia}/${mes}/${ano}. Entre em contato com o suporte para eles verificarem o motivo do problema.`});
            }
        } catch(err){
            reject({'status-code': 400, 'status-message': `Erro ao obter agendamentos para a data ${dia}/${mes}/${ano}: ${err}`});
        }
    })
}


const getPaciente = pacienteID => {
    return new Promise (async (resolve, reject) => {
        try{
            const resp = await fetch(url_paciente_detalhes.replace("00000000-0000-0000-0000-000000000000", pacienteID))

            if (resp.status === 200){
                const data = await resp.json();

                resolve(data)
            } else if (resp.status === 404){
                reject({'status-code': 404, 'status-message': "Não foi possível encontrar o paciente. Entre em contato com o suporte para eles verificarem o motivo do problema."});
            }
        } catch(err){
            reject({'status-code': 400, 'status-message': `Erro ao obter dados do paciente de id ${agendamentoID}: ${err}`});
        }
    })
};


const getFormModalAgendamentoConsultorio = () => {
	const medico = retornarOptionSelected(document.querySelector("#agendamento_form #id_medico")).value
	
	let data = document.getElementById("id_data_atendimento").value.split("/");
	data = `${data[2]}-${data[1]}-${data[0]}`

    const radioInputSelecionado = Array.from(document.querySelectorAll("#id_tipo_atendimento > div > label > input")).filter(radioInput => {
            return radioInput.checked === true;
        }
    )[0]
	const tipo_atendimento = radioInputSelecionado.value-1;

	return {
        paciente: document.getElementById("id_paciente").value,
		nome_paciente: document.getElementById("id_nome_paciente").value,
        cpf_paciente: document.getElementById("id_cpf_paciente").value,
		celular_paciente: document.getElementById("id_celular_paciente").value,
		telefone_fixo_paciente: document.getElementById("id_telefone_fixo_paciente").value,
		medico,
        agendado_por: document.getElementById("id_agendado_por").value,
		tipo_atendimento,
		data_atendimento: data,
		hora_inicio_atendimento: document.getElementById("inicio_hora").value + ":" + document.getElementById("inicio_minuto").value,
		hora_termino_atendimento: document.getElementById("termino_hora").value + ":" + document.getElementById("termino_minuto").value,
		observacoes: document.getElementById("id_observacoes").value,
	};
}

const getFormModalEdicaoAgendamentoConsultorio = () => {
	const medico = retornarOptionSelected(document.querySelector("#agendamento_form #id_medico")).value
	
	let data = document.getElementById("id_data_atendimento").value.split("/");
	data = `${data[2]}-${data[1]}-${data[0]}`

    const radioInputSelecionado = Array.from(document.querySelectorAll("#id_tipo_atendimento > div > label > input")).filter(radioInput => {
            return radioInput.checked === true;
        }
    )[0]
	const tipo_atendimento = radioInputSelecionado.value-1;

	return {
		nome_paciente: document.getElementById("id_nome_paciente").value,
		celular_paciente: document.getElementById("id_celular_paciente").value,
		telefone_fixo_paciente: document.getElementById("id_telefone_fixo_paciente").value,
		medico,
		tipo_atendimento,
		data_atendimento: data,
		hora_inicio_atendimento: document.getElementById("inicio_hora").value + ":" + document.getElementById("inicio_minuto").value,
		hora_termino_atendimento: document.getElementById("termino_hora").value + ":" + document.getElementById("termino_minuto").value,
		observacoes: document.getElementById("id_observacoes").value,
	};
}

const addAgendamentoConsultorio = (data, agendamentoForm) => {
    const jsonData = JSON.stringify(data);

    $.ajax({

        // url: `/atendimento/agendamedica/criar/`,
        url: url_api_agendamento_add,
        method: 'POST',
        data: jsonData,
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
	.done(function(msg){
		const mensagemSucesso = "Atendimento agendado com sucesso!";

        const callbackSucesso = () => {
            document.querySelector(".br-modal-footer button").removeEventListener('click', () => {

            })

            // agendamentoForm.submit();
            // agendamentosFiltroForm.submit();
            location.reload();
        }
        
        mostrarNotificaoSucesso(mensagemSucesso, callbackSucesso);
   })
   .fail(function(jqXHR, textStatus, msg){
		mostrarNotificaoErro(jqXHR.responseJSON['non_field_errors']);
   });
}

const editAgendamentoConsultorio = (agendamentoID, data, agendamentoForm) => {
    const jsonData = JSON.stringify(data);

    $.ajax({
        // url: `/atendimento/agendamedica/${agendamentoID}/`,
        url: url_api_detalhe_agendamento.replace('123', agendamentoID),
        method: 'PUT',
        data: jsonData,
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
	.done(function(msg){
		const mensagemSucesso = "Agendamento editado com sucesso!";

        const callbackSucesso = () => {
            document.querySelector(".br-modal-footer button").removeEventListener('click', () => {

            })

            // agendamentoForm.submit();
            // agendamentosFiltroForm.submit();
            location.reload();
        }
        
        mostrarNotificaoSucesso(mensagemSucesso, callbackSucesso);

   })
   .fail(function(jqXHR, textStatus, msg){
		mostrarNotificaoErro(jqXHR.responseJSON['non_field_errors']);
   });
}


const editAgendamentoConsultorioComFetch = (data, agendamentoID) => {
    const jsonData = JSON.stringify(data);

    return new Promise (async (resolve, reject) => {
        try{
            // const resp = await fetch(`/atendimento/agendamedica/${agendamentoID}/`, {
            const resp = await fetch(url_api_detalhe_agendamento.replace('123', agendamentoID), {
                method: "PUT",
                headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': getCookie('csrftoken')
                },
                body: jsonData,
            });

            const result = await resp.json();

            if(resp.ok){
                resolve(result);
            }  else if (resp.status === 400) {
                reject({'status-code': 400, 'status-message': result["non_field_errors"][0]});
            }
        } catch(err){
            reject(err);
        }
    })
}

const deleteAgendamentoConsultorio = (agendamentoID) => {
    $.ajax({
        // url: `/atendimento/agendamedica/${agendamentoID}/`,
        url: url_api_detalhe_agendamento.replace('123', agendamentoID),
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .done(function(msg){
        const mensagemSucesso = "Atendimento removido com sucesso!";

        const callbackSucesso = () => {
            document.querySelector(".br-modal-footer button").removeEventListener('click', () => {

            })

            location.reload();
        }
        
        mostrarNotificaoSucesso(mensagemSucesso, callbackSucesso)
   })
   .fail(function(jqXHR, textStatus, msg){
        if(jqXHR.responseJSON['error'] === "AgendaMedica matching query does not exist."){
            mostrarNotificaoErro("Não foi possível encontrar o agendamento de atendimento para ser removido. Entre em contato com o suporte para eles verificarem o motivo do problema.");
        }
   });
}