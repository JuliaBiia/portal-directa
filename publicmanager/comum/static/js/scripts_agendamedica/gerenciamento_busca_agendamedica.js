const acaoEditarAgendamento = document.querySelectorAll(".link-editar-agendamento");


acaoEditarAgendamento.forEach(elemento => {
    elemento.addEventListener('click', async () => {
        agendamentoID = parseInt(elemento.getAttribute("data-id-agendamento"));
        renderizarModalEdicaoAgendamentoAtendimento(parseInt(elemento.getAttribute("data-id-agendamento")));
    })
})