{% load static %}

convertDate(originalDate, format) {
    const convertedDate = moment(originalDate).format(format);
    return convertedDate;
},
getTimeline(){
    let url  = `{% url 'saude_enfermagem:atendimentos-get-solicitacoes-timeline' pk='00000000-0000-0000-0000-000000000000' %}`
    axios.get(url.replace('00000000-0000-0000-0000-000000000000', this.objectPk))
    .then((response)=>{  
        this.detalhesTimeLine = response.data
    });
},
finalizarAtendimentoMedicacao(tipo){
    self = this;

    Swal.fire({
        html: `<h2 class="swal2-title" id="swal2-title" style="display: block; font-size: 20px; color: var(--interactive);">Atenção!</h2>
                <div class="swal2-html-container" id="swal2-html-container" style="display: block; font-size: 18px; color: var(--interactive); margin-top: 7px;">${this.textAlert}</div>
            `,
        icon: "warning",
        cancelButtonText: '<i class="fa-solid fa-xmark mr-2"></i> VOLTAR P/ ATENDIMENTO',
        confirmButtonText: '<i class="fa-solid fa-circle-check mr-2"></i> FINALIZAR ATENDIMENTO ',
        showCancelButton: true,
        showConfirmButton: true,
        reverseButtons: true,
        allowOutsideClick: false,
        customClass: {popup: 'custom-popup-finalizar-modal-simples', confirmButton: 'swal2-confirm-custom', cancelButton: 'swal2-cancel-custom'},
        preConfirm: () => {
            let url  = "{% url 'saude_enfermagem:atendimentos-finalizar-solicitacao' pk='00000000-0000-0000-0000-000000000000' %}"
            axios.put(url.replace('00000000-0000-0000-0000-000000000000', self.paciente.atendimentoPK), {solicitacao_pk: self.objectPk , tipo: tipo})
            .then((response) => {
                self.getTimeline()

                let responseInfo = ''
                if(response.data.info === 'retorno'){
                    this.paciente.situacao = 'Retorno'
                    responseInfo = 'As solicitações foram concluídas. Por favor, providencie o <b>retorno</b> do paciente que ainda necessita de acompanhamento médico.'
                }else if(response.data.info === 'encerrado'){
                    this.paciente.situacao = 'Encerrado Pelo Sistema'
                    responseInfo = 'Atendimento do paciente encerrado. O médico não solicitou retorno, portanto o paciente já pode ser <b>liberado</b>.'

                }
                self.SweetAlert("Registro salvo com sucesso!", "success", responseInfo)
            });
        },
      });
},
finalizarAtendimento(tipo){
    self = this;

    if(self.solicitacoesSemAnexo.length > 0){
        let tagNames = [];

        if (self.solicitacoesNome) {
            for (const chave in self.solicitacoesNome) {
                tagNames.push(`<span class="br-tag small" style="background: #959ea9 !important; height: 30px;"><span id="densidade01">${self.solicitacoesNome[chave]}</span></span>`);
            }
        }
        Swal.fire({
            html: `<h2 class="swal2-title" id="swal2-title" style="display: block; font-size: 20px; color: var(--interactive);">Atenção!</h2>
                    <div class="swal2-html-container" id="swal2-html-container" style="display: block; font-size: 18px; color: var(--interactive); margin-top: 7px;">${self.textAlert}</div>
                    <div style="display: block; font-size: 14px; color: var(--color); margin-top: 30px; font-weight: bolder;">Existem solicitações sem anexo.</div>
                    <div>
                        <textarea id="swal2-textarea" class="swal2-textarea capslock" placeholder="Por favor, adicione a justivicativa." style="width: 80%; font-size: 16px !important;"></textarea>
                    </div>
                    <div style="text-transform: lowercase; color: #959ea9; text-align: left; margin-left: 72px;">
                        ${tagNames}
                    </div>
                `,
            icon: "warning",
            cancelButtonText: '<i class="fa-solid fa-xmark mr-2"></i> VOLTAR P/ ATENDIMENTO',
            confirmButtonText: '<i class="fa-solid fa-circle-check mr-2"></i> FINALIZAR ATENDIMENTO ',
            showCancelButton: true,
            showConfirmButton: true,
            reverseButtons: true,
            allowOutsideClick: false,
            customClass: {popup: 'custom-popup-finalizar', confirmButton: 'swal2-confirm-custom', cancelButton: 'swal2-cancel-custom'},
            preConfirm: () => {
                const selectElement = document.getElementById('swal2-textarea');
                const selectedValue = selectElement.value;

                if(selectedValue === '') {
                    Swal.showValidationMessage('Adicione uma justificativa.');
                }else{
                    self.solicitacoesSemAnexo.forEach((item) => {
                        let url  = "{% url 'saude_enfermagem:atendimentos-exames' pk='00000000-0000-0000-0000-000000000000' %}"
                        axios.put(url.replace('00000000-0000-0000-0000-000000000000', item.id), {com_anexo: false, justificativa: selectedValue}, {
                            headers: { 'Content-Type': 'multipart/form-data'},
                        }).then((response) => {
                            const foundExame = this.listagemAplicacoes.find(param => param.id === response.data.id);
        
                            if (foundExame) {
                                foundExame.arquivo_nome = response.data.arquivo_nome;
                                foundExame.arquivo = response.data.arquivo;
                                foundExame.situacao = response.data.situacao;
                            }
                        });
                    });

                    let url  = "{% url 'saude_enfermagem:atendimentos-finalizar-solicitacao' pk='00000000-0000-0000-0000-000000000000' %}"
                    axios.put(url.replace('00000000-0000-0000-0000-000000000000', self.paciente.atendimentoPK), {solicitacao_pk: self.objectPk})
                    .then((response) => {
                        self.getTimeline()

                        let responseInfo = ''
                        if(response.data.info === 'retorno'){
                            this.paciente.situacao = 'Retorno'
                            responseInfo = 'As solicitações foram concluídas. Por favor, providencie o <b>retorno</b> do paciente que ainda necessita de acompanhamento médico.'
                        }else if(response.data.info === 'encerrado'){
                            this.paciente.situacao = 'Encerrado Pelo Sistema'
                            responseInfo = 'Atendimento do paciente encerrado. O médico não solicitou retorno, portanto o paciente já pode ser <b>liberado</b>.'
                        }
                        self.SweetAlert("Registro salvo com sucesso!", "success", responseInfo)
                    });
                }
            },
          });

    }else{
        Swal.fire({
            html: `<h2 class="swal2-title" id="swal2-title" style="display: block; font-size: 20px; color: var(--interactive);">Atenção!</h2>
                    <div class="swal2-html-container" id="swal2-html-container" style="display: block; font-size: 18px; color: var(--interactive); margin-top: 7px;">${this.textAlert}</div>
                `,
            icon: "warning",
            cancelButtonText: '<i class="fa-solid fa-xmark mr-2"></i> VOLTAR P/ ATENDIMENTO',
            confirmButtonText: '<i class="fa-solid fa-circle-check mr-2"></i> FINALIZAR ATENDIMENTO ',
            showCancelButton: true,
            showConfirmButton: true,
            reverseButtons: true,
            allowOutsideClick: false,
            customClass: {popup: 'custom-popup-finalizar-modal-simples', confirmButton: 'swal2-confirm-custom', cancelButton: 'swal2-cancel-custom'},
            preConfirm: () => {
                let url  = "{% url 'saude_enfermagem:atendimentos-finalizar-solicitacao' pk='00000000-0000-0000-0000-000000000000' %}"
                axios.put(url.replace('00000000-0000-0000-0000-000000000000', self.paciente.atendimentoPK), {solicitacao_pk: self.objectPk , tipo: tipo})
                .then((response) => {
                    self.getTimeline();

                    if(tipo === 'laboratorio'){
                        self.getExamesLaboratoriais();
                    }else if(tipo === 'imagem'){
                        self.getExamesImagem()
                    }

                    let responseInfo = ''
                    if(response.data.info === 'retorno'){
                        this.paciente.situacao = 'Retorno'
                        responseInfo = 'As solicitações foram concluídas. Por favor, providencie o <b>retorno</b> do paciente que ainda necessita de acompanhamento médico.'
                    }else if(response.data.info === 'encerrado'){
                        this.paciente.situacao = 'Encerrado Pelo Sistema'
                        responseInfo = 'Atendimento do paciente encerrado. O médico não solicitou retorno, portanto o paciente já pode ser <b>liberado</b>.'
                    }
                    self.SweetAlert("Registro salvo com sucesso!", "success", responseInfo)
                });
            },
          });
    }
},
SweetAlert(titulo, icon, info=null){
    let informativo = ''

    if(info){
        informativo = `<p style="font-size: 20px; padding-left: 47px; padding-right: 47px;">${info}</p>`
    }
    Swal.fire({
        html: `<h2 class="swal2-title" id="swal2-title" style="display: block; font-size: 20px; color: var(--interactive);>Informação!</h2>
                <div class="swal2-html-container" id="swal2-html-container" style="display: block; font-size: 20px; color: var(--interactive); margin-top: 7px;">
                    <p style="color: var(--interactive); font-size: 20px;">${titulo}<p/> ${informativo}
                </div>
            `,
        icon: icon,
        confirmButtonText: '<i class="fa-solid fa-check ml-2"></i> FECHAR',
        cancelButtonText: '<i class="fas fa-arrow-left mr-2"></i> VOLTAR',
        showCancelButton: info !== null ? true : false,
        showConfirmButton: true,
        allowOutsideClick: false,
        reverseButtons: true,
        customClass: {popup: 'custom-popup-anexar-info',},
      }).then((result) => {
        if (result.dismiss === Swal.DismissReason.cancel) {
            window.location.href = this.urlRedirect;
        }
    });
},
onDragOver(event) {
    event.preventDefault();
},
// onDrop(event) {
//     const files = event.dataTransfer.files;
//     this.arquivosFiles = Array.from(files);
//     this.arquivosNomes = this.arquivosFiles.map(file => file.name);
// },
// onDrop(event) {
//     event.preventDefault();
//     const file = event.dataTransfer.files[0];
//     if (file) {
//         this.arquivoNome = file.name;
//         this.arquivoFile = file;
//     }
// },
// onFileChange(event) {
//     const file = event.target.files[0];
    
//     if (file) {
//         this.arquivoNome = file.name;
//         this.arquivoFile = file;
//     }
// },
onFileChange(event) {
    this.arquivosFiles = Array.from(event.target.files);
    this.arquivosNomes = this.arquivosFiles.map(file => file.name);
},
modalAnexarAquivo(tipo){
    this.arquivoNome = ''
    this.arquivoFile = null
    this.comAnexo = true
    this.justificativa = ''
    $('#fileInput').val('');
    $('#modal-anexo').hide();

    if(tipo === 'abrirAnexo'){
        $('#modal-anexo').show();
        this.arquivosNomes = [];
        this.arquivosFiles = [];
        this.photoCaptured = false;
        this.resetPhoto();
        this.stopCamera();
        this.type = 'arquivo';
    } else if(tipo === 'fecharAnexo'){
        $('#modal-anexo').hide();
        this.arquivosNomes = [];
        this.arquivosFiles = [];
        this.photoCaptured = false;
        this.resetPhoto();
        this.stopCamera();
        this.type = 'arquivo';
    }
}