const converterParaSelect2 = (nomeDaClasseSelects = "campo-select") => $(`.${nomeDaClasseSelects}`)
    .each(
        function(_, element) {
            const elementId = element.id;
            
            if(element.getAttribute("data-tipo-container-form") === "modal"){
                $(`#${elementId}`).select2({
                    "language": "pt",
                    "dropdownParent": $(`#${element.getAttribute("data-class-modal")}`)
                });
            } else{
                $(`#${elementId}`).select2({
                    "language": "pt"
                });
            }
        }
    );

const aplicarEstilizacaoPadraoSelec2 = () => {
    $('.select2-container--default').css({
        // "margin-top": "4px",
    })

    $('.select2-container--default .select2-selection--single').css({
        "height": "51px",
        "border": "1px solid rgb(131 133 136)",
        "display": "flex",
        "align-items": "center"
    });

    $('.select2-container--default .select2-selection--single .select2-selection__arrow').css({
        "top": "18px",
        "height": "32px",
        "width": "32px",
        "margin-top": "-8px",
        "margin-right": "4px"
    });

    $('.select2-container--default .select2-selection--single .select2-selection__arrow b').css({
        "border": "none"
    });
}

$(document).ready(function() {
    converterParaSelect2();
    aplicarEstilizacaoPadraoSelec2();
});