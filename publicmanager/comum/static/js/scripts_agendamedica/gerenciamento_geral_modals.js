const agendamentosFiltroForm = document.getElementById('id_agendamentos_filtro_form');

const umMedicoFoiSelecionado = Boolean(retornarOptionSelected(document.querySelector('.select-medico #id_medico_filtragem_agendamentos')).value);

const botaoAbrirModalCadastrarFeriado = document.getElementById('abrir-modal-inserir-feriado');
const botaoAbrirModalCadastrarBloqueioAgenda = document.getElementById('abrir-modal-inserir-bloqueio-agenda');


// if (umMedicoFoiSelecionado){
//     botaoAbrirModalCadastrarFeriado.remove();
// } else{
//     botaoAbrirModalCadastrarBloqueioAgenda.remove();
// }


$("#id_medico_filtragem_agendamentos").on("change", function () {
    const idMedico = this.options[this.selectedIndex].value;

    if(idMedico){
        location.href=url_agendamedica_medico_selecionado.replace("00000000-0000-0000-0000-000000000000", idMedico);
    } else{
        location.href=url_agendamedica_medico_nao_selecionado
    }
});

window.onbeforeunload = function () {
    sessionStorage.setItem("selectMedicoOptionSelected", $('#id_agendamentos_filtro_form #id_medico').val());
}