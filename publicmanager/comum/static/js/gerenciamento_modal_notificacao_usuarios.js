const mostrarNotificaoErro = (mensagemErro) => {
    document.querySelector("#modal-mensagem-erro > .br-modal > .br-modal-body > p").innerHTML = mensagemErro;

    document.getElementById('modal-mensagem-erro').style.display = "block";
}

const mostrarNotificaoSucesso = (mensagemSucesso, callbackSucesso) => {
    document.querySelector("#modal-mensagem-sucesso > .br-modal > .br-modal-body > p").innerHTML = mensagemSucesso;

    // document.querySelector("#modal-mensagem-sucesso > .br-modal > .br-modal-footer button").addEventListener('click', callbackSucesso)
    document.querySelector("#modal-mensagem-sucesso > .br-modal > .br-modal-body > button").addEventListener('click', callbackSucesso)

    document.getElementById('modal-mensagem-sucesso').style.display = "block";
}

const mostrarNotificaoImpossibilidade = (mensagemImpossibilidade) => {
    document.querySelector("#modal-mensagem-impossibilidade > .br-modal > .br-modal-body > p").innerHTML = mensagemImpossibilidade;

    document.getElementById('modal-mensagem-impossibilidade').style.display = "block";
}

const confirmarRemocao = (mensagemConfirmacao, callbackConfirmacao) => {
    document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-body > p").innerHTML = mensagemConfirmacao;

    // document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-footer > #confirmacao-remocao").addEventListener('click', callbackConfirmacao)
    // document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-body #confirmacao-remocao").addEventListener('click', callbackConfirmacao)
    document.querySelector("#modal-confirmacao-remocao > .br-modal > .br-modal-body #confirmacao-remocao").addEventListener('click', callbackConfirmacao)

    document.getElementById('modal-confirmacao-remocao').style.display = "block";
}

const confirmarOperacao = (tituloOperacao, mensagemConfirmacao, callbackConfirmacao) => {
    const elementoModal = document.getElementById('modal-confirmacao-operacao');

    const elementoTituloDoModal = document.querySelector('#modal-confirmacao-operacao > .br-modal > .br-modal-body > .container-icone-atencao > p');
    const elementoMensagemConfirmacao = document.querySelector("#modal-confirmacao-operacao > .br-modal > .br-modal-body > p");

    const botaoConfirmarOperacao = document.querySelector("#modal-confirmacao-operacao > .br-modal > .br-modal-body #confirmacao-operacao");
    const botaoNegarOperacao = document.querySelector("#modal-confirmacao-operacao > .br-modal > .br-modal-body #negacao-operacao");


    elementoTituloDoModal.innerHTML = tituloOperacao;
    elementoMensagemConfirmacao.innerHTML = mensagemConfirmacao;

    botaoConfirmarOperacao.addEventListener('click', () => {

        botaoConfirmarOperacao.removeEventListener('click', () => {
            
        })

        callbackConfirmacao();
        
        elementoModal.style.display = "none";
    })
    botaoNegarOperacao.addEventListener('click', () => {

        botaoNegarOperacao.removeEventListener('click', () => {
            
        })

        elementoModal.style.display = "none";
    })

    elementoModal.style.display = "block";
}


document.getElementById('fechar-modal-mensagem-erro').addEventListener('click', () => {
    document.getElementById('modal-mensagem-erro').style.display = "none";
})

document.getElementById('fechar-modal-mensagem-impossibilidade').addEventListener('click', () => {
    document.getElementById('modal-mensagem-impossibilidade').style.display = "none";
})

document.getElementById('negacao-remocao').addEventListener('click', () => {
    document.getElementById('modal-confirmacao-remocao').style.display = "none";
})