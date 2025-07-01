const botaoAbrirModalRelatorioAgendamento = document.getElementById('abrir-modal-relatorio-agendamento');

const modalRelatorioAgendamento = document.getElementById("modal-relatorio-agendamento");
// const bloqueio_agenda_form = document.getElementById('id_bloqueio_agenda_form');

// const botaoCadastrarBloqueioAgenda = document.getElementById('cadastrar-bloqueio-agenda');
const botaoVoltarParaAgendaMedica = document.getElementById('voltar-relatorio-agendamento');

const fecharModalRelatorioAgendamento = document.getElementById('fechar-modal-relatorio-agendamento')


botaoAbrirModalRelatorioAgendamento.addEventListener('click', () => {
    ajustarSelectModal();
    modalRelatorioAgendamento.style.display = "block";
});

// botaoCadastrarBloqueioAgenda.addEventListener('click', e => {
//     const dadosForm = getFormModalDeCadastroDeBloqueioAgenda();

//     $("#id_bloqueio_agenda_form #id_medico").removeAttr('disabled');
//     addBloqueioAgenda(dadosForm);

//     // location.reload();
// });

botaoVoltarParaAgendaMedica.addEventListener('click', () => {
    modalRelatorioAgendamento.style.display = "none";
});


$("#id_bloqueio_agenda_filtro_form").submit(function () {
    sessionStorage.setItem("precisaDeixarAbertoOModalDeRelatorioAgendamento", 1);
});

fecharModalRelatorioAgendamento.addEventListener('click', () => {
    modalRelatorioAgendamento.style.display = "none";
});


document.getElementById("id_relatorio_agendamento_form").addEventListener('submit', e => {
    e.preventDefault();

    document.getElementById("id_medico_relatorio").removeAttribute("disabled");

    document.getElementById("id_relatorio_agendamento_form").submit();
})