const botaoFecharModalCadastrarBloqueioAgenda = document.getElementById('fechar-modal-cadastrar-bloqueio-agenda');


const modalBloqueioAgenda = document.getElementById("modal-bloqueio-agenda");


const acaoEditarBloqueioAgenda = document.querySelectorAll("#link-editar-bloqueio-agenda");

const acaoRemoverBloqueioAgenda = document.querySelectorAll('#link-remover-bloqueio-agenda');
const botaoConfirmacaoRemocaoBloqueioAgenda = document.getElementById('confirmacao-remocao-bloqueio-agenda');
const botaoNegacaoRemocaoBloqueioAgenda = document.getElementById('negacao-remocao-bloqueio-agenda');


const bloqueioAgendaForm = document.getElementById('id_bloqueio_agenda_form');
const gerarRelatorioBloqueiosAgendaForm = document.getElementById("gerar-relatorio-bloqueios-agenda-form")

const botaoCadastrarBloqueioAgenda = document.getElementById('cadastrar-bloqueio-agenda');
const botaoEditarBloqueioAgenda = document.getElementById('editar-bloqueio-agenda');
// const botaoLimparFormBloqueioAgenda = document.getElementById('limpar-form-bloqueio-agenda');
const botaoPesquisarFormBloqueioAgenda = document.getElementById('pesquisar-grid-bloqueio-agenda');
const botaoListarBloqueios = document.getElementById("listar-bloqueios")


const preencherSelectMedicoDoModalCadastrarBloqueioAgenda = () => {
    const selectSelecaoMedico = document.querySelector('.select-medico #id_medico_filtragem_agendamentos');
    const selectMedico = document.querySelector('#id_bloqueio_agenda_form #id_medico_bloqueio_agenda');


    mudarOptionSelected(
        selectMedico,
        retornarOptionSelected(selectSelecaoMedico).value
    )

    $("#id_bloqueio_agenda_form #id_medico_bloqueio_agenda").select2({ // -> aqui que ocorre o erro
        "language": "pt",
        dropdownParent: $('.br-scrim-util')
    });
}
botaoAbrirModalCadastrarBloqueioAgenda.addEventListener('click', () => {
    if(retornarOptionSelected(document.querySelector('.select-medico #id_medico_filtragem_agendamentos')).value){
        document.querySelector("#modal-bloqueio-agenda > .br-modal > .header > .titulo-modal-bloqueio-agenda > span").innerHTML = "INSERIR BLOQUEIO DE AGENDA";

        preencherSelectMedicoDoModalCadastrarBloqueioAgenda();
        modalBloqueioAgenda.style.display = "block";
    }
});

botaoFecharModalCadastrarBloqueioAgenda.addEventListener('click', () => {
    modalBloqueioAgenda.style.display = "none";
});

const confirmarInsercaoBloqueioAgenda = (mensagemConfirmacao, dadosBloqueioAgenda, bloqueioAgendaForm) => {
    const tituloOperacao = "Inserção";
    const callbackConfirmacao = () => {
        addBloqueioAgenda(dadosBloqueioAgenda, bloqueioAgendaForm);
    }

    confirmarOperacao(tituloOperacao, mensagemConfirmacao, callbackConfirmacao);
}

const confirmarEdicaoBloqueioAgenda = (mensagemConfirmacao, bloqueioAgendaID, dadosBloqueioAgenda, bloqueioAgendaForm) => {
    const tituloOperacao = "Edição";
    const callbackConfirmacao = () => {
        updateBloqueioAgenda(bloqueioAgendaID, dadosBloqueioAgenda, bloqueioAgendaForm);
    }

    confirmarOperacao(tituloOperacao, mensagemConfirmacao, callbackConfirmacao);
}


const editarBloqueioAgenda = JSON.parse(document.getElementById('editar-bloqueio-agenda-data').textContent);

if (editarBloqueioAgenda[0]){
    document.querySelector("#modal-bloqueio-agenda > .br-modal > .header > .titulo-modal-bloqueio-agenda > span").innerHTML = "EDITAR BLOQUEIO AGENDA";

    botaoCadastrarBloqueioAgenda.style.display = 'none';
    botaoEditarBloqueioAgenda.style.display = 'block';
} else{
    botaoCadastrarBloqueioAgenda.style.display = 'block';
    botaoEditarBloqueioAgenda.style.display = 'none';
}


acaoEditarBloqueioAgenda.forEach(elemento => {
    elemento.addEventListener('click', () => {
        sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda", 1);
    })
})

acaoRemoverBloqueioAgenda.forEach(elemento => {
    elemento.addEventListener('click', e => {
        const mensagemConfirmacao = "Deseja realmente remover este bloqueio da agenda?";

        const callbackConfirmacao = () => {
            document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-body #confirmacao-remocao").removeEventListener('click', () => {

            })

            document.getElementById('modal-confirmacao-remocao').style.display = "none";

            const bloqueioAgendaId = elemento.getAttribute("data-id-bloqueio-agenda");
            deleteBloqueioAgenda(bloqueioAgendaId);
        }
        
        confirmarRemocao(mensagemConfirmacao, callbackConfirmacao);
    })
})


bloqueioAgendaForm.addEventListener('submit', async e => {
    e.preventDefault();

    document.getElementById('operacao_dados_bloqueio_agenda').value = editarBloqueioAgenda[0] ? "editar_bloqueio_agenda" : "cadastrar_bloqueio_agenda"

    const dadosForm = getFormModalDeCadastroDeBloqueioAgenda();

    $("#id_bloqueio_agenda_form #id_medico").removeAttr('disabled');


    const data_inicial = dadosForm.data_inicial;
    const data_final = dadosForm.data_final;

    const existeUmAgendamentoNoPeriodoDoBloqueioAgenda = await verificarSeExisteUmAgendamentoNoPeriodoDoBloqueioAgenda(dadosForm.medico, data_inicial, data_final);


    if (editarBloqueioAgenda[0]){
        if(existeUmAgendamentoNoPeriodoDoBloqueioAgenda){
            const mensagemConfirmacao = "Existe agendamentos marcados para este período. Deseja realmente editar este bloqueio na agenda do médico?";

            confirmarEdicaoBloqueioAgenda(mensagemConfirmacao, editarBloqueioAgenda[1], dadosForm, bloqueioAgendaForm)
        } else{
            updateBloqueioAgenda(editarBloqueioAgenda[1], dadosForm, bloqueioAgendaForm)
        }
    } else{
        if(existeUmAgendamentoNoPeriodoDoBloqueioAgenda){
            const mensagemConfirmacao = "Existe agendamentos marcados para este período. Deseja realmente inserir este bloqueio na agenda do médico?";

            confirmarInsercaoBloqueioAgenda(mensagemConfirmacao, dadosForm, bloqueioAgendaForm)
        } else{
            addBloqueioAgenda(dadosForm, bloqueioAgendaForm);
        }
    }
});

// botaoLimparFormBloqueioAgenda.addEventListener('click', e => {
//     sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda", 1);

//     const selectSelecaoMedico = document.querySelector('.select-medico #id_medico_filtragem_agendamentos');

//     e.preventDefault()
//     location = `http://127.0.0.1:8000${botaoLimparFormBloqueioAgenda.getAttribute("href").replace(1, retornarOptionSelected(selectSelecaoMedico).value)}`;
// });

botaoPesquisarFormBloqueioAgenda.addEventListener('click', () => {
    sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda", 1);
    $("#id_bloqueio_agenda_form #id_medico").removeAttr('disabled');

    document.getElementById('operacao_dados_bloqueio_agenda').value = "pesquisar_bloqueio_agenda"

    bloqueioAgendaForm.submit();
});

botaoListarBloqueios.addEventListener('click', () => {
    document.querySelector("#gerar-relatorio-bloqueios-agenda-form #id_medico").value = document.querySelector("#id_bloqueio_agenda_form #id_medico").value

    gerarRelatorioBloqueiosAgendaForm.submit();
})