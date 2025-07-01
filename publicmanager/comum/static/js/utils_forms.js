const retornarOptionSelected = selectElement => {
    return selectElement.options[selectElement.selectedIndex];
}

const mudarOptionSelected = (selectElement, valorDoNovoOptionSelected) => {

    Array.from(
        selectElement.options
    ).map(
        option => {
            if(option.value === valorDoNovoOptionSelected){
                option.setAttribute("selected", "selected");
            } else{
                option.removeAttribute("selected");
            }
        }
    );
}


const ajustarSelectModal = () => {
    converterParaSelect2("modal-campo-select");
    aplicarEstilizacaoPadraoSelec2();
}