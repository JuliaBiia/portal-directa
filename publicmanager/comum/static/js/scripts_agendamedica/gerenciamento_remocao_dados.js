// const acaoRemoverAgendamento = document.querySelectorAll('.link-remover-dado');


// acaoRemoverAgendamento.forEach(elemento => {
//     elemento.addEventListener('click', e => {
//         const mensagemConfirmacao = "Deseja realmente remover este feriado?";

//         const callbackConfirmacao = () => {
//             document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-footer > #confirmacao-remocao").removeEventListener('click', () => {

//             })

//             document.getElementById('modal-confirmacao-remocao').style.display = "none";

//             location.reload = elemento.getAttribute("data-url-remocao");
//         }
        
//         confirmarRemocao(mensagemConfirmacao, callbackConfirmacao);
//     })
// })



const removerDado = () => {
    const mensagemConfirmacaoRemocao = document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-body > #mensagem-confirmacao").innerHTML
    const remocaoDadoForm = document.getElementById("remover-dado-form")

    const acaoRemoverDado = document.querySelectorAll('.link-remover-dado');

    acaoRemoverDado.forEach(elemento => {        
        elemento.addEventListener('click', e => {
            const callbackConfirmacao = () => {
                document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-body #confirmacao-remocao").removeEventListener('click', () => {

                })

                document.getElementById('modal-confirmacao-remocao').style.display = "none";

                const dadoID = elemento.getAttribute("data-id-dado");
                remocaoDadoForm.action = remocaoDadoForm.action.replace("1234", dadoID);
                
                remocaoDadoForm.submit();
            }
            
            confirmarRemocao(mensagemConfirmacaoRemocao, callbackConfirmacao);
        })
    })
}

removerDado();