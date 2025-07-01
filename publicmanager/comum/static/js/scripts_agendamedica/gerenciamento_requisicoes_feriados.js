const getFormModalDeCadastroDeFeriado = () => {
    const nomeFeriado = document.querySelector('#id_feriado_form #id_nome_feriado').value;

    const dataInicial = retornarValueCampoData('#id_feriado_form #id_data_inicial');
    const dataFinal = retornarValueCampoData('#id_feriado_form #id_data_final');

    
    return {
        "nome_feriado": nomeFeriado,
        "data_inicial": dataInicial,
        "data_final": dataFinal,
    }
}


const addFeriado = (data, feriadoForm) => {
    const jsonData = JSON.stringify(data);

    $.ajax({
        url: url_api_feriado_add,
        method: 'POST',
        data: jsonData,
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .done(function(msg){
        const mensagemSucesso = "Feriado salvo com sucesso!";

        const callbackSucesso = () => {
            document.querySelector(".br-modal-footer button").removeEventListener('click', () => {
                
            })

            sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarFeriado", 1);
            feriadoForm.submit();
        }
        
        mostrarNotificaoSucesso(mensagemSucesso, callbackSucesso)
   })
   .fail(function(jqXHR, textStatus, msg){
        mostrarNotificaoErro(jqXHR.responseJSON['non_field_errors']);
   });
}


const updateFeriado = (feriadoID, data, feriadoForm) => {
    const jsonData = JSON.stringify(data);

    $.ajax({
        url: url_api_feriado_update.replace("123", feriadoID),
        method: 'PUT',
        data: jsonData,
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .done(function(msg){
        const mensagemSucesso = "Feriado editado com sucesso!";

        const callbackSucesso = () => {
            document.querySelector(".br-modal-footer button").removeEventListener('click', () => {

            })

            sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarFeriado", 1);
            feriadoForm.submit();
        }
        
        mostrarNotificaoSucesso(mensagemSucesso, callbackSucesso)
   })
   .fail(function(jqXHR, textStatus, msg){
        mostrarNotificaoErro(jqXHR.responseJSON['non_field_errors']);
   });
}


const deleteFeriado = (feriadoID) => {
    $.ajax({
        url: url_api_feriado_delete.replace("123", feriadoID),
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .done(function(msg){
        const mensagemSucesso = "Feriado removido com sucesso!";

        const callbackSucesso = () => {
            document.querySelector(".br-modal-footer button").removeEventListener('click', () => {

            })

            sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarFeriado", 1);
            location.reload();
        }
        
        mostrarNotificaoSucesso(mensagemSucesso, callbackSucesso)
   })
   .fail(function(jqXHR, textStatus, msg){
        if(jqXHR.responseJSON['error'] === "Feriado matching query does not exist."){
            mostrarNotificaoErro("Não foi possível encontrar o feriado para ser removido. Entre em contato com o suporte para eles verificarem o motivo do problema.");
        }
   });
}