const containerCamposTipoInsumo = document.getElementById("container-campos-tipo-insumo")
const containerCamposTipoMedicamento = document.getElementById("container-campos-tipo-medicamento")
const containerCamposTipoProduto = document.getElementById("container-campos-tipo-produto")

const codigoBarraMaterial = document.getElementById("codigo-barra-material")


const esconderContainerCamposTipoInsumo = () => {
    containerCamposTipoInsumo.style.display = "none";

    $("#id_insumo").val("").trigger('change');
    $("#id_quantidade_insumo").val("");
    $("#id_unidade_insumo").val("").trigger('change');
}

const esconderContainerCamposTipoMedicamento = () => {
    containerCamposTipoMedicamento.style.display = "none";

    $("#id_medicamento").val("").trigger('change');
    $("#id_quantidade_medicamento").val("");
    $("#id_unidade_medicamento").val("").trigger('change');
}

const esconderContainerCamposTipoProduto = () => {
    containerCamposTipoProduto.style.display = "none";

    $("#id_produto").val("").trigger('change');
    $("#id_quantidade_produto").val("");
    $("#id_unidade_produto").val("").trigger('change');
}



$('#id_tipos_materiais').on('change', function(event) {
    const tipoMaterialSelecionado = retornarOptionSelected(event.currentTarget).value

    $("#id_codigo_barra_material").val("");

    if(tipoMaterialSelecionado === "tipo-produto-medico"){
        // containerCamposTipoInsumo.style.display = "none"
        // containerCamposTipoMedicamento.style.display = "none"
        esconderContainerCamposTipoInsumo();
        esconderContainerCamposTipoMedicamento();


        containerCamposTipoProduto.style.display = "block";

        document.querySelector("label[for='id_codigo_barra_material']").innerHTML = "Código de Barras do Produto medico";
    }
    else if(tipoMaterialSelecionado === "tipo-medicamento"){
        // containerCamposTipoInsumo.style.display = "none"
        // containerCamposTipoProduto.style.display = "none"
        esconderContainerCamposTipoInsumo();
        esconderContainerCamposTipoProduto();

        containerCamposTipoMedicamento.style.display = "block";

        document.querySelector("label[for='id_codigo_barra_material']").innerHTML = "Código de Barras do Medicamento";
    }
    else if(tipoMaterialSelecionado === "tipo-insumo-farmaceutico"){
        // containerCamposTipoMedicamento.style.display = "none"
        // containerCamposTipoProduto.style.display = "none"
        esconderContainerCamposTipoMedicamento();
        esconderContainerCamposTipoProduto();

        containerCamposTipoInsumo.style.display = "block";

        document.querySelector("label[for='id_codigo_barra_material']").innerHTML = "Código de Barras do Insumo farmacêutico";
    }
})

$('#id_produto').on('change', async function (event) {
    $("#id_codigo_barra_material").val("");

    let produtoID = this.options[this.selectedIndex].value;
    
    if(produtoID){
        $("#id_codigo_barra_material").val("...");

        try{
            dadosProduto = await getProdutoMedico(produtoID);

            $("#id_codigo_barra_material").val(`${dadosProduto.codigo_de_barra}`);
        } catch (error){
            if(Object.keys(error).find(element => element === "status-code")){
                if(error["status-code"] === 400 || error["status-code"] === 404){
                    mostrarNotificaoErro(error['status-message']);
                } else{
                    mostrarNotificaoErro(error);
                }
            } else{
                mostrarNotificaoErro(error);
            }
        }
    }
})

$('#id_medicamento').on('change', async function(event) {
    $("#id_codigo_barra_material").val("");

    let medicamentoID = this.options[this.selectedIndex].value;
    
    if(medicamentoID){
        $("#id_codigo_barra_material").val("...");

        try{
            dadosMedicamento = await getMedicamento(medicamentoID);

            $("#id_codigo_barra_material").val(`${dadosMedicamento.codigo_de_barra}`);
        } catch (error){
            if(Object.keys(error).find(element => element === "status-code")){
                if(error["status-code"] === 400 || error["status-code"] === 404){
                    mostrarNotificaoErro(error['status-message']);
                } else{
                    mostrarNotificaoErro(error);
                }
            } else{
                mostrarNotificaoErro(error);
            }
        }
    }
})

$('#id_insumo').on('change', async function(event) {
    $("#id_codigo_barra_material").val("");

    let insumoID = this.options[this.selectedIndex].value;
    
    if(insumoID){
        $("#id_codigo_barra_material").val("...");

        try{
            dadosInsumo = await getInsumo(insumoID);
            console.log("dadosInsumo", dadosInsumo.codigo_de_barra)

            $("#id_codigo_barra_material").val(`${dadosInsumo.codigo_de_barra}`);
        } catch (error){
            if(Object.keys(error).find(element => element === "status-code")){
                if(error["status-code"] === 400 || error["status-code"] === 404){
                    mostrarNotificaoErro(error['status-message']);
                } else{
                    mostrarNotificaoErro(error);
                }
            } else{
                mostrarNotificaoErro(error);
            }
        }
    }
})

const adicionarMaterial = (dadosMaterial) => {
    if (dadosMaterial["quantidade"] == 0 || dadosMaterial["unidade"] == 0 || dadosMaterial["id"] == 0) {
        mostrarNotificaoErro(`Para ser possível adicionar um(a) ${dadosMaterial["tipo"].toLowerCase()}, você deve selecionar um(a), informar a quantidade e selecionar a unidade.`)

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
        </div>`;

    const elementoGrid = `
        <tr id="id_material_grid_${quantidadeAtualMateriaisAdicionados+1}">
            <td style="position: relative; bottom: 1px;">
                <a href="javascript:void(0)" class="br-button circle">
                    <i class="fas fa-eye" aria-hidden="true"></i>
                </a>
            </td>
            <td style="position: relative; bottom: 1px;">
                <a href="javascript:void(0)" class="br-button circle btnDetele" onclick="confirmarRemoçãoMaterial(${quantidadeAtualMateriaisAdicionados+1})">
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
                ${dadosMaterial["codigo_de_barra"]}
            </td>
        </tr>`;
    
    $("#container-materiais-adicionados").append(elementoContainerMateriaisAdicionados);
    $("#tabela_materiais").append(elementoGrid);

    // const ultimoFlowGroupAdicionadoNoContainerMateriaisAdicionados = document.querySelector("#container-materiais-adicionados").lastChild;

    // const ultimaLinhaAdicionadaNoGrid = document.querySelector("#tabela_materiais").lastChild;
    // const btnDeleteDoMaterialAdicionado = ultimaLinhaAdicionadaNoGrid.firstElementChild.children[0];

    // btnDeleteDoMaterialAdicionado.addEventListener('click', e => {
    //     document.querySelector("#tabela_materiais").removeChild(ultimaLinhaAdicionadaNoGrid);
    //     document.querySelector("#container-materiais-adicionados").removeChild(ultimoFlowGroupAdicionadoNoContainerMateriaisAdicionados);
    // })
}

document.getElementById("botao-adicionar-material").addEventListener("click", event => {
    dadosMaterial = {};


    const tipoMaterialSelecionado = retornarOptionSelected($('#id_tipos_materiais')[0]).value;

    if(tipoMaterialSelecionado === "tipo-produto-medico"){
        console.log('Tipo - Produto médico');

        dadosMaterial["id"] = $("#id_produto").val();
        dadosMaterial["valor"] = $("#id_produto option:selected").text();
        dadosMaterial["codigo_de_barra"] = $("#id_codigo_barra_material").val();
        dadosMaterial["quantidade"] = $("#id_quantidade_produto").val();
        dadosMaterial["unidade"] = $("#id_unidade_produto").val();
        dadosMaterial["tipo"] = "Produto";
    }
    else if(tipoMaterialSelecionado === "tipo-medicamento"){
        console.log('Tipo - Medicamento');

        dadosMaterial["id"] = $("#id_medicamento").val();
        dadosMaterial["valor"] = $("#id_medicamento option:selected").text();
        dadosMaterial["codigo_de_barra"] = $("#id_codigo_barra_material").val();
        dadosMaterial["quantidade"] = $("#id_quantidade_medicamento").val();
        dadosMaterial["unidade"] = $("#id_unidade_medicamento").val();
        dadosMaterial["tipo"] = "Medicamento";
    }
    else if(tipoMaterialSelecionado === "tipo-insumo-farmaceutico"){
        console.log('Tipo - Insumo farmacêutico');

        dadosMaterial["id"] = $("#id_insumo").val();
        dadosMaterial["valor"] = $("#id_insumo option:selected").text();
        dadosMaterial["codigo_de_barra"] = $("#id_codigo_barra_material").val();
        dadosMaterial["quantidade"] = $("#id_quantidade_insumo").val();
        dadosMaterial["unidade"] = $("#id_unidade_insumo").val();
        dadosMaterial["tipo"] = "Insumo";
    };


    adicionarMaterial(dadosMaterial);
})


const confirmarRemoçãoMaterial = indexMaterial => {
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
}


const habilitarCampos = () => {
    document.getElementById("id_numero_pedido").removeAttribute("disabled");
    // document.getElementById("id_farmaceutico_solicitante").removeAttribute("disabled");
}

document.getElementById("botao-salvar").addEventListener("click", event => {
    habilitarCampos();

    document.getElementById("id_requisicao_material_farmacia_form").submit();
})