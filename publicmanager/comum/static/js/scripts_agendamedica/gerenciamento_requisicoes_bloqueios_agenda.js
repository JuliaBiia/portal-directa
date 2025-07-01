const getFormModalDeCadastroDeBloqueioAgenda = () => {
    const medico = retornarOptionSelected(document.querySelector("#id_bloqueio_agenda_form #id_medico")).value

    const dataInicial = retornarValueCampoData('#id_bloqueio_agenda_form #id_data_inicial');
    const dataFinal = retornarValueCampoData('#id_bloqueio_agenda_form #id_data_final');

    const motivo = document.querySelector('#id_bloqueio_agenda_form #id_motivo').value;

    
    return {
        "medico": medico,
        "data_inicial": dataInicial,
        "data_final": dataFinal,
        "motivo": motivo,
    }
}

const verificarSeExisteUmAgendamentoNoPeriodoDoBloqueioAgenda = async (medicoID, dataInicial, dataFinal) => {
    try{
        const resp = await fetch(`/atendimento/api/agendamedica/buscarporperiododetempo/?medico_id=${medicoID}&data_inicial=${dataInicial}&data_final=${dataFinal}`);
        
        if (resp.status === 404){
            return false;
        }

        return true;
    } catch(error){
        return false;
    }
}


function addBloqueioAgenda(data, bloqueio_agenda_form) {
    var jsonData = JSON.stringify(data);

    $.ajax({
        url: url_api_bloqueio_agenda_add,
        method: 'POST',
        data: jsonData,
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .done(function(msg){
        const mensagemSucesso = "Bloqueio de agenda feito com sucesso!";

        const callbackSucesso = () => {
            document.querySelector(".br-modal-footer button").removeEventListener('click', () => {

            })

            sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda", 1);
            bloqueio_agenda_form.submit();
        }
        
        mostrarNotificaoSucesso(mensagemSucesso, callbackSucesso);

   })
   .fail(function(jqXHR, textStatus, msg){
        mostrarNotificaoErro(jqXHR.responseJSON['non_field_errors']);
   });
}


const updateBloqueioAgenda = (bloqueioAgendaID, data, bloqueio_agenda_form) => {
    const jsonData = JSON.stringify(data);

    $.ajax({
        url: url_api_bloqueio_agenda_update.replace("123", bloqueioAgendaID),
        method: 'PUT',
        data: jsonData,
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .done(function(msg){
        const mensagemSucesso = "Bloqueio de agenda editado com sucesso!";

        const callbackSucesso = () => {
            document.querySelector(".br-modal-footer button").removeEventListener('click', () => {

            })

            sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda", 1);
            bloqueio_agenda_form.submit();
        }
        
        mostrarNotificaoSucesso(mensagemSucesso, callbackSucesso);

   })
   .fail(function(jqXHR, textStatus, msg){
        mostrarNotificaoErro(jqXHR.responseJSON['non_field_errors']);
   });
}


const deleteBloqueioAgenda = (bloqueioAgendaID) => {
    $.ajax({
        // url: `/api/bloqueioagenda/delete/${bloqueioAgendaID}/`,
        url: url_api_bloqueio_agenda_delete.replace("123", bloqueioAgendaID),
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .done(function(msg){
        const mensagemSucesso = "Bloqueio de agenda removido com sucesso!";

        const callbackSucesso = () => {
            document.querySelector(".br-modal-footer button").removeEventListener('click', () => {

            })

            sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda", 1);
            location.reload();
        }
        
        mostrarNotificaoSucesso(mensagemSucesso, callbackSucesso);

   })
   .fail(function(jqXHR, textStatus, msg){
        if(jqXHR.responseJSON['error'] === "BloqueioAgenda matching query does not exist."){
            mostrarNotificaoErro("Não foi possível encontrar o bloqueio da agenda para ser removido. Entre em contato com o suporte para eles verificarem o motivo do problema.");
        }
   });
}