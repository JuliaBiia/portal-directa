//Formulário de cadastro de feriado
// const botaoAbrirModalCadastrarFeriado = document.getElementById('abrir-modal-inserir-feriado');
const botaoFecharModalCadastrarFeriado = document.getElementById('fechar-modal-cadastrar-feriado');


const modalFeriado = document.getElementById("modal-feriado");


const acaoEditarFeriado = document.querySelectorAll("#link-editar-feriado");

const acaoRemoverFeriado = document.querySelectorAll('#link-remover-feriado');
const botaoConfirmacaoRemocaoFeriado = document.getElementById('confirmacao-remocao-feriado');
const botaoNegacaoRemocaoFeriado = document.getElementById('negacao-remocao-feriado');


const feriadoForm = document.getElementById('id_feriado_form');

const botaoCadastrarFeriado = document.getElementById('cadastrar-feriado');
const botaoEditarFeriado = document.getElementById('editar-feriado');
// const botaoLimparFormFeriado = document.getElementById('limpar-form-feriado');
const botaoPesquisarFormFeriado = document.getElementById('pesquisar-grid-feriado');



botaoAbrirModalCadastrarFeriado.addEventListener('click', () => {
    document.querySelector("#modal-feriado > .br-modal > .header > .titulo-modal-feriado > span").innerHTML = "INSERIR FERIADO";
    modalFeriado.style.display = "block"
});

botaoFecharModalCadastrarFeriado.addEventListener('click', () => {
    modalFeriado.style.display = "none"
});


const editarFeriado = JSON.parse(document.getElementById('editar-feriado-data').textContent);

if (editarFeriado[0]){
    document.querySelector("#modal-feriado > .br-modal > .header > .titulo-modal-feriado > span").innerHTML = "EDITAR FERIADO";
    
    botaoCadastrarFeriado.style.display = 'none';
    botaoEditarFeriado.style.display = 'block';
} else{
    botaoCadastrarFeriado.style.display = 'block';
    botaoEditarFeriado.style.display = 'none';
}


acaoEditarFeriado.forEach(elemento => {
    elemento.addEventListener('click', () => {
        sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarFeriado", 1);
    })
})

acaoRemoverFeriado.forEach(elemento => {
    elemento.addEventListener('click', e => {
        const mensagemConfirmacao = "Deseja realmente remover este feriado?";

        const callbackConfirmacao = () => {
            document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-body #confirmacao-remocao").removeEventListener('click', () => {

            })


            document.getElementById('modal-confirmacao-remocao').style.display = "none";

            const feriadoId = elemento.getAttribute("data-id-feriado");
            deleteFeriado(feriadoId);
        }
        
        confirmarRemocao(mensagemConfirmacao, callbackConfirmacao);
    })
})


feriadoForm.addEventListener('submit', async e => {
    e.preventDefault();

    document.getElementById('operacao_dados_feriado').value = editarFeriado[0] ? "editar_feriado" : "cadastrar_feriado"

    const dadosForm = getFormModalDeCadastroDeFeriado();

    if (editarFeriado[0]){
        updateFeriado(editarFeriado[1], dadosForm, feriadoForm);
    } else{
        addFeriado(dadosForm, feriadoForm);
    }
});

// botaoLimparFormFeriado.addEventListener('click', () => {
//     sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarFeriado", 1);
// });

botaoPesquisarFormFeriado.addEventListener('click', () => {
    sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarFeriado", 1);

    document.getElementById('operacao_dados_feriado').value = "pesquisar_feriado"

    feriadoForm.submit();
});