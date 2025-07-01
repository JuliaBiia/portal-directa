const containerCamposTipoInsumo = document.getElementById("container-campos-tipo-insumo")
const containerCamposTipoMedicamento = document.getElementById("container-campos-tipo-medicamento")
const containerCamposTipoProduto = document.getElementById("container-campos-tipo-produto")


const esconderContainerCamposTipoInsumo = () => {
    containerCamposTipoInsumo.style.display = "none";

    $("#id_insumo").val("").trigger('change');
    $("#id_quantidade_insumo").val("");
    $("#id_unidade_insumo").val("").trigger('change');
    $("#id_numero_lote_insumo").val("");
    $("#id_data_vencimento_insumo").val(""); // Ainda não sei se está funcionando
}

const esconderContainerCamposTipoMedicamento = () => {
    containerCamposTipoMedicamento.style.display = "none";

    $("#id_medicamento").val("").trigger('change');
    $("#id_quantidade_medicamento").val("");
    $("#id_unidade_medicamento").val("").trigger('change');
    $("#id_numero_lote_medicamento").val("");
    $("#id_data_vencimento_medicamento").val(""); // Ainda não sei se está funcionando
}

const esconderContainerCamposTipoProduto = () => {
    containerCamposTipoProduto.style.display = "none";

    $("#id_produto").val("").trigger('change');
    $("#id_quantidade_produto").val("");
    $("#id_unidade_produto").val("").trigger('change');
    $("#id_numero_lote_produto").val("");
    $("#id_data_vencimento_produto").val(""); // Ainda não sei se está funcionando
}

const abrirModalVisualizacaoMaterial = (dadosMaterial) => {
    Swal.fire({
        html: `
            <div class="swal2-title swal2-title-custom text-left" id="swal2-title" style="display: block; height: 48px; margin-top: -32px;">
                <h2 class="ml-3">
                    <i class="fas fa-list-ul text-color-blue-1gov" style="font-size: 25px; margin-right: 5px;"></i>
                    <label class="text-color-blue-1gov custom-text" style="font-size: var(--font-size-scale-up-02) !important; font-weight: 700 !important;">INFORMAÇÕES DO MATERIAL</label>
                    <button type="button" class="close mr-2" aria-label="Close" onclick="Swal.close()" style="border: 0px; color: var(--blue-vivid-60); background-color: var(--lt-color-gray-100) !important;">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </h2>
            </div>

            <div class="container" style="padding: 25px;">
                <div class="row br-input justify-content-center mt-2">
                    <div class="col-11 br-input">
                        <label class="text-color-blue-1gov custom-text">Material:</label>
                        <input class="input-highlight-labeless capslock custom-input-info" value="${dadosMaterial[0]}" type="text" readonly disabled>
                    </div>
                </div>
                <div class="row br-input justify-content-center mt-2">
                    <div class="col-11 br-input">
                        <label class="text-color-blue-1gov custom-text">Tipo de Material:</label>
                        <input class="input-highlight-labeless capslock custom-input-info" value="${dadosMaterial[1]}" type="text" readonly disabled>
                    </div>
                </div>
                <div class="row br-input justify-content-center mt-2">
                    <div class="col-11 br-input">
                        <label class="text-color-blue-1gov custom-text">Quantidade:</label>
                        <input class="input-highlight-labeless capslock custom-input-info" value="${dadosMaterial[2]}" type="text" readonly disabled>
                    </div>
                </div>
                <div class="row br-input justify-content-center mt-2">
                    <div class="col-11 br-input">
                        <label class="text-color-blue-1gov custom-text">Unidade do Material:</label>
                        <input class="input-highlight-labeless capslock custom-input-info" style="width: 100%;" value="${dadosMaterial[3]}" type="text" readonly disabled>
                    </div>
                </div>
                <div class="row br-input justify-content-center mt-2">
                    <div class="col-11 br-input">
                        <label class="text-color-blue-1gov custom-text">N° do Lote:</label>
                        <input class="input-highlight-labeless capslock custom-input-info" style="width: 100%;" value="${dadosMaterial[4]}" type="text" readonly disabled>
                    </div>
                </div>
                <div class="row br-input justify-content-center mt-2">
                    <div class="col-11 br-input">
                        <label class="text-color-blue-1gov custom-text">Data de Vencimento:</label>
                        <input class="input-highlight-labeless capslock custom-input-info" style="width: 97%;" value="${dadosMaterial[5]}" type="text" readonly disabled>
                    </div>
                </div>
            </div>
        `,
        showCancelButton: false,
        showConfirmButton: false,
        allowOutsideClick: true,
        cancelButton: 'custom-left-button',
        showClass: {popup: 'animated fadeInDown faster',},
        hideClass: {popup: 'animated fadeOutUp faster',},
        customClass: {popup: 'custom-popup-view-material-farmacia-entrada',},
    });
}

const adicionarEventListenerParaVisualizacaoMaterial = element => {
    element.addEventListener("click", event => {
        let dadosMaterial = []

        if(event.target.id === "visualizar-material"){
            dadosMaterial = Array.from(event.target.parentNode.parentNode.children).slice(2, 8).map( element => element.innerHTML.trim());
        } else{
            dadosMaterial = Array.from(event.target.parentNode.parentNode.parentNode.children).slice(2, 8).map( element => element.innerHTML.trim());
        }

        abrirModalVisualizacaoMaterial(dadosMaterial)
    })
}



$('#id_tipos_materiais').on('change', function(event) {
    const tipoMaterialSelecionado = retornarOptionSelected(event.currentTarget).value

    if(tipoMaterialSelecionado === "tipo-produto-medico"){
        esconderContainerCamposTipoInsumo();
        esconderContainerCamposTipoMedicamento();


        containerCamposTipoProduto.style.display = "block";
    }
    else if(tipoMaterialSelecionado === "tipo-medicamento"){
        esconderContainerCamposTipoInsumo();
        esconderContainerCamposTipoProduto();

        containerCamposTipoMedicamento.style.display = "block";
    }
    else if(tipoMaterialSelecionado === "tipo-insumo-farmaceutico"){
        esconderContainerCamposTipoMedicamento();
        esconderContainerCamposTipoProduto();

        containerCamposTipoInsumo.style.display = "block";
    }
})


Array.from(document.querySelectorAll("#visualizar-material")).forEach(function (element){
    adicionarEventListenerParaVisualizacaoMaterial(element);
});

$('#id_produto').on('change', async function (event) {
    let produtoID = this.options[this.selectedIndex].value;
    
    if(produtoID){
        try{
            dadosProduto = await getProdutoMedico(produtoID);
        } catch (error){
            if(Object.keys(error).find(element => element === "status-code")){
                if(error["status-code"] === 400 || error["status-code"] === 404){
                    // mostrarNotificaoErro(error['status-message']);
                    ModalMensagemErro.fire({
                        text: `${error['status-message']}`
                    });
                } else{
                    // mostrarNotificaoErro(error);
                    ModalMensagemErro.fire({
                        text: `${error}`
                    });
                }
            } else{
                // mostrarNotificaoErro(error);
                ModalMensagemErro.fire({
                    text: `${error}`
                });
            }
        }
    }
})

$('#id_medicamento').on('change', async function(event) {
    let medicamentoID = this.options[this.selectedIndex].value;
    
    if(medicamentoID){
        try{
            dadosMedicamento = await getMedicamento(medicamentoID);
        } catch (error){
            if(Object.keys(error).find(element => element === "status-code")){
                if(error["status-code"] === 400 || error["status-code"] === 404){
                    // mostrarNotificaoErro(error['status-message']);
                    ModalMensagemErro.fire({
                        text: `${error['status-message']}`
                    });
                } else{
                    // mostrarNotificaoErro(error);
                    ModalMensagemErro.fire({
                        text: `${error}`
                    });
                }
            } else{
                // mostrarNotificaoErro(error);
                ModalMensagemErro.fire({
                    text: `${error}`
                });
            }
        }
    }
})

$('#id_insumo').on('change', async function(event) {
    let insumoID = this.options[this.selectedIndex].value;
    
    if(insumoID){
        try{
            dadosInsumo = await getInsumo(insumoID);
        } catch (error){
            if(Object.keys(error).find(element => element === "status-code")){
                if(error["status-code"] === 400 || error["status-code"] === 404){
                    // mostrarNotificaoErro(error['status-message']);
                    ModalMensagemErro.fire({
                        text: `${error['status-message']}`
                    });
                } else{
                    // mostrarNotificaoErro(error);
                    ModalMensagemErro.fire({
                        text: `${error}`
                    });
                }
            } else{
                // mostrarNotificaoErro(error);
                ModalMensagemErro.fire({
                    text: `${error}`
                });
            }
        }
    }
})

const adicionarMaterial = (dadosMaterial) => {
    if (dadosMaterial["quantidade"] == "" || dadosMaterial["unidade"] == "" || dadosMaterial["id"] == "" || dadosMaterial["data_vencimento"] == "" || dadosMaterial["numero_lote"] == "") {
        ModalMensagemErro.fire({
            text: `Para ser possível adicionar um(a) ${dadosMaterial["tipo"].toLowerCase()}, você deve selecionar um(a), informar a quantidade, n° de lote, data de vencimento e selecionar a unidade.`
        });

        return;
    }
    
    
    const quantidadeAtualMateriaisAdicionados = Array.from(document.querySelectorAll("#container-materiais-adicionados .form-group")).length-1

    const elementoContainerMateriaisAdicionados = `
        <div id="id_material_container_campos_${quantidadeAtualMateriaisAdicionados+1}" class='form-group'>
            <select
                name="material" 
                for="basic-default-fullname" 
                class="campo-select" 
                id="id_material_${quantidadeAtualMateriaisAdicionados+1}"
                readonly='readonly'
            >
                <option
                    value='${dadosMaterial["id"]}'
                    selected
                >
                    ${dadosMaterial["valor"]}
                </option>
            </select>
            <input
                type='search'
                class='br-input' 
                name='tipo_material'
                id='id_tipo_material' 
                value='${dadosMaterial["tipo"]}' 
                readonly='readonly'
            >
            <input
                type='search'
                class='br-input'
                name='quantidade_material' id='id_quantidade_material'
                value='${dadosMaterial["quantidade"]}' 
                readonly='readonly'
            >
            <input
                type='search'
                class='br-input'
                name='unidade_material' 
                id='id_unidade_material'
                value='${dadosMaterial["unidade"]}' 
                readonly='readonly'
            >
            <input
                type='search'
                class='br-input'
                name='numero_lote_material' 
                id='id_numero_lote_material'
                value='${dadosMaterial["numero_lote"]}' 
                readonly='readonly'
            >
            <input
                type='search'
                class='br-input'
                name='data_vencimento_material' 
                id='id_data_vencimento_material'
                value='${dadosMaterial["data_vencimento"]}' 
                readonly='readonly'
            >
        </div>`;

    const elementoGrid = `
        <tr id="id_material_grid_${quantidadeAtualMateriaisAdicionados+1}">
            <td style="position: relative; bottom: 1px;">
                <a href="javascript:void(0)" class="br-button circle">
                    <i class="fas fa-eye" aria-hidden="true"></i>
                </a>
            </td>
            <td style="position: relative; bottom: 1px;">
                <a href="javascript:void(0)" class="br-button circle btnDetele" onclick="confirmarRemocaoMaterial(${quantidadeAtualMateriaisAdicionados+1})">
                    <i class="fas fa-trash-alt" aria-hidden="true"></i>
                </a>
            </td>
            <td style="position: relative; top: 4px;">
                ${dadosMaterial["valor"].trim().split(" - ")[0]}
            </td>
            <td style="position: relative; top: 4px;">${dadosMaterial["tipo"]}</td>
            <td style="position: relative; top: 4px;">
                ${dadosMaterial["quantidade"]}
            </td>
            <td style="position: relative; top: 4px;">
                ${dadosMaterial["unidade"]}
            </td>
            <td style="position: relative; top: 4px;">
                ${dadosMaterial["numero_lote"]}
            </td>
            <td style="position: relative; top: 4px;">
                ${dadosMaterial["data_vencimento"]}
            </td>
        </tr>`;
    
    $("#container-materiais-adicionados").append(elementoContainerMateriaisAdicionados);
    $("#tabela_materiais").append(elementoGrid);

    document.getElementById(`id_material_grid_${quantidadeAtualMateriaisAdicionados+1}`).children[0].children[0].setAttribute("id", "visualizar-material")

    adicionarEventListenerParaVisualizacaoMaterial(document.getElementById(`id_material_grid_${quantidadeAtualMateriaisAdicionados+1}`).children[0].children[0]);
}

document.getElementById("botao-adicionar-material").addEventListener("click", event => {
    dadosMaterial = {};


    const tipoMaterialSelecionado = retornarOptionSelected($('#id_tipos_materiais')[0]).value;

    if(tipoMaterialSelecionado === "tipo-produto-medico"){
        dadosMaterial["id"] = $("#id_produto").val();
        dadosMaterial["valor"] = $("#id_produto option:selected").text();
        dadosMaterial["tipo"] = "Produto";
        dadosMaterial["unidade"] = $("#id_unidade_produto").val();
        dadosMaterial["quantidade"] = $("#id_quantidade_produto").val();
        dadosMaterial["numero_lote"] = $("#id_numero_lote_produto").val();
        dadosMaterial["data_vencimento"] = $('#id_data_vencimento_produto').val();
    }
    else if(tipoMaterialSelecionado === "tipo-medicamento"){
        dadosMaterial["id"] = $("#id_medicamento").val();
        dadosMaterial["valor"] = $("#id_medicamento option:selected").text();
        dadosMaterial["tipo"] = "Medicamento";
        dadosMaterial["unidade"] = $("#id_unidade_medicamento").val();
        dadosMaterial["quantidade"] = $("#id_quantidade_medicamento").val();
        dadosMaterial["numero_lote"] = $("#id_numero_lote_medicamento").val();
        dadosMaterial["data_vencimento"] = $('#id_data_vencimento_medicamento').val();
    }
    else if(tipoMaterialSelecionado === "tipo-insumo-farmaceutico"){
        dadosMaterial["id"] = $("#id_insumo").val();
        dadosMaterial["valor"] = $("#id_insumo option:selected").text();
        dadosMaterial["tipo"] = "Insumo";
        dadosMaterial["unidade"] = $("#id_unidade_insumo").val();
        dadosMaterial["quantidade"] = $("#id_quantidade_insumo").val();
        dadosMaterial["numero_lote"] = $("#id_numero_lote_insumo").val();
        dadosMaterial["data_vencimento"] = $('#id_data_vencimento_insumo').val();
    };


    adicionarMaterial(dadosMaterial);
})


const confirmarRemocaoMaterial = indexMaterial => {
    /*
    const callbackConfirmacaoRemocaoMaterial = () => {
        document.getElementById("tabela_materiais").removeChild(
            document.getElementById(`id_material_grid_${indexMaterial}`)
        )

        document.querySelector("#container-materiais-adicionados").removeChild(
            document.getElementById(`id_material_container_campos_${indexMaterial}`)
        )
    }
    
    confirmarOperacao(
        "Remoção de material",
        "Deseja realmente remover este material?",
        callbackConfirmacaoRemocaoMaterial
    )
    */

    ModalConfirmacaoRemocao.fire({
        text: `Deseja realmente remover este material?`,
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById("tabela_materiais").removeChild(
                document.getElementById(`id_material_grid_${indexMaterial}`)
            )
    
            document.querySelector("#container-materiais-adicionados").removeChild(
                document.getElementById(`id_material_container_campos_${indexMaterial}`)
            )
        }
    });
}


const habilitarCampos = () => {
    document.getElementById("id_numero_pedido").removeAttribute("disabled");
    // document.getElementById("id_farmaceutico_solicitante").removeAttribute("disabled");
}

document.getElementById("botao-salvar").addEventListener("click", event => {
    habilitarCampos();

    document.getElementById("id_entrada_material_farmacia_form").submit();
})