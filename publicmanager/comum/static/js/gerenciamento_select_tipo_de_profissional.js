const ocultarMostrarCampos = (valorOptionSelected, idForm) => {
    valorOptionSelected = valorOptionSelected.toUpperCase()
 
    if(valorOptionSelected === 'MED' || valorOptionSelected.includes('MEDICO') || valorOptionSelected.includes('MEDICA')) {
        if(idForm === "profissional_form_cadastro_edicao"){
            Array.from(document.querySelectorAll(".campo-oculto-container input")).forEach(
                campo => campo.setAttribute('required', 'required')
            )
    
            document.querySelector('.campo-oculto-container .campo-oculto-coren input').removeAttribute('required');
        }

        $(".campo-oculto-container").show()
        $(".campo-oculto-cns").show()
        $(".campo-oculto-cbo").show()
        $(".campo-oculto-crm").show()
        $(".campo-oculto-coren").removeClass('coren-tecnico-enfermagem')
        $(".campo-oculto-coren").hide()
    }

    else if(valorOptionSelected.includes('TECNICO DE ENFERMAGEM') || valorOptionSelected.includes('TÉCNICO DE ENFERMAGEM')){
        if(idForm === "profissional_form_cadastro_edicao"){
            Array.from(document.querySelectorAll(".campo-oculto-container input")).forEach(
                campo => campo.removeAttribute('required')
            )
            
            document.querySelector('.campo-oculto-container .campo-oculto-coren input').setAttribute('required', 'required')
        }

        $(".campo-oculto-container").show()
        $(".campo-oculto-cns").hide()
        $(".campo-oculto-cbo").hide()
        $(".campo-oculto-crm").hide()
        $(".campo-oculto-coren").addClass('coren-tecnico-enfermagem')
        $(".campo-oculto-coren").show()

        
    }

    else if(valorOptionSelected.includes('ENFERMEIRO') || valorOptionSelected.includes('ENFERMEIRA')){
        if(idForm === "profissional_form_cadastro_edicao"){
            Array.from(document.querySelectorAll(".campo-oculto-container input")).forEach(
                campo => campo.setAttribute('required', 'required')
            )
    
            document.querySelector('.campo-oculto-container .campo-oculto-crm input').removeAttribute('required');
        }

        $(".campo-oculto-container").show()
        $(".campo-oculto-cns").show()
        $(".campo-oculto-cbo").show()
        $(".campo-oculto-crm").hide()
        $(".campo-oculto-coren").removeClass('coren-tecnico-enfermagem')
        $(".campo-oculto-coren").show()
    }

    else{
        if(idForm === "profissional_form_cadastro_edicao"){
            Array.from(document.querySelectorAll(".campo-oculto-container input")).forEach(
                campo => campo.removeAttribute('required', 'required')
            )   
        }

        $(".campo-oculto-container").hide()
    }
}

const ajustarValorOptionSelected = valorOptionSelected => {
    valorOptionSelected = valorOptionSelected.toUpperCase();

    let valorOptionSelectedCorrigido = "";

    for (let i = 0; i < valorOptionSelected.length; i++) {
        const caractere = valorOptionSelected.charAt(i);

        const novoCaractere = charMap[caractere];

        if (typeof novoCaractere === 'undefined'){
        valorOptionSelectedCorrigido += caractere;
        } else{
        valorOptionSelectedCorrigido += novoCaractere;
        }
    }

    return valorOptionSelectedCorrigido;
}

$(document).ready(function() {
    const idForm = document.querySelector("form").id;

    let tipoProfissional = document.getElementById('id_tipo_profissional');

    if(idForm === "profissional_form_busca"){
        tipoProfissional = document.getElementById('id_tipo_profissional_filtro');
    }
    
    const optionSelected = tipoProfissional.options[tipoProfissional.selectedIndex];
    const valorOptionSelected = optionSelected.innerHTML;

    const valorOptionSelectedCorrigido = ajustarValorOptionSelected(valorOptionSelected)

    ocultarMostrarCampos(valorOptionSelectedCorrigido);
    
});


$("#id_tipo_profissional").on("change", function () {
    const valorOptionSelected = this.options[this.selectedIndex].text

    const valorOptionSelectedCorrigido = ajustarValorOptionSelected(valorOptionSelected)

    ocultarMostrarCampos(valorOptionSelectedCorrigido);

    Array.from(document.querySelectorAll(".campo-oculto > input")).forEach(
        campo => campo.value = ""
    )

  }
);

$("#id_tipo_profissional_filtro").on("change", function () {
    const valorOptionSelected = this.options[this.selectedIndex].text

    const valorOptionSelectedCorrigido = ajustarValorOptionSelected(valorOptionSelected)

    ocultarMostrarCampos(valorOptionSelectedCorrigido);

    Array.from(document.querySelectorAll(".campo-oculto > input")).forEach(
        campo => campo.value = ""
    )

  }
);