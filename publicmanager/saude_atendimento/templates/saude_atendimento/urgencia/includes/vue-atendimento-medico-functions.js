{% load static %}

visualizarInformacoes(tipo, instance=null, acao=null) {
    self = this;

    if(tipo === 'procedimento'){
        if(acao === 'visualizar'){

            const swalConfig = {
                html: `
                    <div class="swal2-title swal2-title-custom text-left" id="swal2-title" style="display: block; height: 48px; margin-top: -32px;">
                        <h2 class="ml-3">
                            <i class="fas fa-briefcase-medical text-color-blue-1gov" style="font-size: 25px; margin-right: 5px;"></i>
                            <label class="text-color-blue-1gov custom-text" style="font-size: var(--font-size-scale-up-02) !important; font-weight: 700 !important;">INFORMAÇÕES DO PROCEDIMENTO</label>
                            <button type="button" class="close mr-2" aria-label="Close" onclick="Swal.close()" style="border: 0px; color: var(--blue-vivid-60); background-color: var(--lt-color-gray-100) !important;">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </h2>
                    </div>

                    <div class="container" style="padding: 25px;">
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Data:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" value="${this.convertDate(instance.created_at, 'DD/MM/YYYY')}" type="text" readonly disabled>
                            </div>
                        </div>
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Nome do paciente:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" value="${instance.paciente_nome}" type="text" readonly disabled>
                            </div>
                        </div>
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Médico:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" value="${instance.medico_solicitante.nome}" type="text" readonly disabled>
                            </div>
                        </div>
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Estabelecimento solicitante:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" value="${instance.estabelecimento_solicitante}" type="text" readonly disabled>
                            </div>
                        </div>
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Código do procedimento:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" style="width: 100%;" value="${instance.procedimento_codigo}" type="text" readonly disabled>
                            </div>
                        </div>
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Procedimento:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" style="width: 100%;" value="${instance.procedimento_nome}" type="text" readonly disabled>
                            </div>
                        </div>
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-4 br-input">
                                <label class="text-color-blue-1gov custom-text">Classificação:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" style="width: 97%;" value="${instance.classificacao_nome}" type="text" readonly disabled>
                            </div>
                            <div class="col-3 br-input">
                                <label class="text-color-blue-1gov custom-text">Quantidade:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" style="width: 100%;" value="${instance.quantidade}" type="text" readonly disabled>
                            </div>
                            <div class="col-4 br-input">
                                <label class="text-color-blue-1gov custom-text">Responsável:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" style="width: 100%;" value="${instance.realizado_por_nome}" type="text" readonly disabled>
                            </div>
                        </div>
                    </div>
                `,
                reverseButtons: true,
                allowOutsideClick: true,
                showClass: {popup: 'animated fadeInDown faster',},
                hideClass: {popup: 'animated fadeOutUp faster',},
                customClass: {popup: 'custom-popup-view-procedimento',},
            }
            
            if(instance.realizado_por === 0 || instance.realizado_por === '0'){
                if(instance.situacao !== 3 && instance.lista_chamada_solicitacao){
                    swalConfig.showCancelButton = false;
                    swalConfig.showConfirmButton = true;
                    swalConfig.confirmButtonText = "<i class='fa-solid fa-arrow-rotate-left'></i> REABRIR SOLICITAÇÃO"; 
                }else{
                    swalConfig.showCancelButton = false;
                    swalConfig.showConfirmButton = false;
                }
    
                Swal.fire(swalConfig).then((result) => {
                    if (result.isConfirmed) {
                        self.confirmarReaberturaSolicitacao(tipo, instance, acao);
                    }
                });
            }

            if(instance.realizado_por === 1 || instance.realizado_por === '1'){
                if(instance && instance.situacao === 0 || instance.situacao === '0' && !instance.lista_chamada_solicitacao){
                    swalConfig.showCancelButton = true;
                    swalConfig.showConfirmButton = true;
                    swalConfig.confirmButtonText = "<i class='fa-solid fa-arrow-rotate-left'></i> CONFIRMAR"; 
                    swalConfig.cancelButtonText = "<i class='fa-solid fa-xmark mr-2'></i> SUSPENDER";

                }else if(instance && instance.situacao === 1 || instance.situacao === '1' && instance.lista_chamada_solicitacao){
                    swalConfig.confirmButtonText = "<i class='fa-solid fa-check'></i> CONFIRMAR"; 
                    swalConfig.showCancelButton = false;
                    swalConfig.showConfirmButton = true;
                }else{
                    swalConfig.cancelButtonText = "<i class='fa-solid fa-xmark mr-2'></i> SUSPENDER";
                    swalConfig.showCancelButton = true;
                    swalConfig.showConfirmButton = false;
                }
    
                Swal.fire(swalConfig).then((result) => {
                    if (result.isConfirmed) {
                        Swal.fire({
                            title: 'Atenção!',
                            text: 'Deseja realmente confirmar o procedimento?',
                            icon: "info",
                            showCancelButton: true,
                            showConfirmButton: true,
                            confirmButtonText: "<i class='fa-solid fa-check'></i> CONFIRMAR",
                            cancelButtonText: "<i class='fa-solid fa-reply mr-2'></i> VOLTAR",
                            reverseButtons: true,
                            allowOutsideClick: false,
                            customClass: {popup: 'custom-popup-view-cancelar-confirmar-procedimento', confirmButton: 'swal2-confirm-custom', cancelButton: 'swal2-cancel-custom'},
                            preConfirm: () => {
                                self.suspenderConfirmarProcedimento('2', instance);
                            },
                        }).then((result) => {
                            if (result.dismiss === Swal.DismissReason.cancel) {
                                self.visualizarInformacoes('procedimento', instance, 'visualizar');
                            }
                        });

                    } else if (result.dismiss === 'cancel') {
                        Swal.fire({
                            html: `<h2 class="swal2-title" id="swal2-title" style="display: block; font-size: 20px; color: var(--interactive);">Atenção!</h2>
                                    <div class="swal2-html-container" id="swal2-html-container" style="display: block; font-size: 18px; color: var(--interactive); margin-top: 7px;">Por Favor, Adicione uma justificativa</div>
                                    <div>
                                        <textarea id="swal2-textarea" class="swal2-textarea capslock" placeholder="Por favor, adicione a justivicativa." style="width: 80%; font-size: 16px !important;"></textarea>
                                    </div>
                                `,
                            icon: "info",
                            showCancelButton: true,
                            showConfirmButton: true,
                            confirmButtonText: "<i class='fa-solid fa-check'></i> CONFIRMAR",
                            cancelButtonText: "<i class='fa-solid fa-reply mr-2'></i> VOLTAR",
                            reverseButtons: true,
                            allowOutsideClick: false,
                            customClass: {popup: 'custom-popup-view-cancelar-confirmar-procedimento', confirmButton: 'swal2-confirm-custom', cancelButton: 'swal2-cancel-custom'},
                            preConfirm: () => {
                                const selectElement = document.getElementById('swal2-textarea');
                                const selectedValue = selectElement.value;
    
                                if(selectedValue === '') {
                                    Swal.showValidationMessage('Adicione uma justificativa.');
                                }else{
                                    self.suspenderConfirmarProcedimento('1', instance, selectedValue);
                                }
                            },
                        }).then((result) => {
                            if (result.dismiss === Swal.DismissReason.cancel) {
                                self.visualizarInformacoes('procedimento', instance, 'visualizar');
                            }
                        });
                    }
                });
            }
        }
    }else if(tipo === 'exame') {
        let arquivoExameUrl = [];

        let arquivosComplementaresExames = []
        if(instance.arquivos.length > 0){
            for(let i = 0; i < instance.arquivos.length; i++){
                arquivosComplementaresExames.push(
                    `<div class="col-10 mt-2" onclick="window.open('/media/${instance.arquivos[i].arquivo}', '_blank')" style="text-transform: uppercase; border: 1px dashed #1351b4; padding: 6px; text-align: center; cursor: pointer;">
                        <i class="fas fa-file-image text-color-blue-1gov" style="font-size: 25px; margin-right: 19px;"></i>
                        <span style="color: var(--interactive-light);">${instance.arquivos[i].nome.length > 30 ? `...${instance.arquivos[i].nome.slice(-30)}` : instance.arquivos[i].nome}</span>
                    </div>`
                )
            }
        }

        if(instance.arquivo){
            arquivoExameUrl.push(
                `<div class="col-10" onclick="window.open('${instance.arquivo}', '_blank')" style="text-transform: uppercase; border: 1px dashed #1351b4; padding: 6px; text-align: center; cursor: pointer;">
                    <i class="fas fa-file-image text-color-blue-1gov" style="font-size: 25px; margin-right: 19px;"></i>
                    <span style="color: var(--interactive-light);">${instance.arquivo_nome.length > 30 ? `...${instance.arquivo_nome.slice(-30)}` : instance.arquivo_nome}</span>
                </div>`
            )
        }else{
            arquivoExameUrl.push(`<div class="col-10" style="text-transform: uppercase; border: 1px dashed #1351b4; padding: 6px; text-align: center;">
                    <i class="fas fa-file-image text-color-blue-1gov" style="font-size: 25px; margin-right: 19px;"></i>
                    <span style="color: var(--interactive-light);">Sem arquivo anexado</span>
                </div>`
            )
        }
        const swalConfig = {
            html: `
                <div class="swal2-title swal2-title-custom text-left" id="swal2-title" style="display: block; height: 48px; margin-top: -32px;">
                    <h2 class="ml-3">
                        <i class="fas fa-file-signature text-color-blue-1gov" style="font-size: 25px; margin-right: 5px;"></i>
                        <label class="text-color-blue-1gov custom-text" style="font-size: var(--font-size-scale-up-02) !important; font-weight: 700 !important;">INFORMAÇÕES DO EXAME</label>
                        <button type="button" class="close mr-2" aria-label="Close" onclick="Swal.close()" style="border: 0px; color: var(--blue-vivid-60); background-color: var(--lt-color-gray-100) !important;">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </h2>
                </div>

                <div class="container" style="padding: 25px;">
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Data:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${this.convertDate(instance.created_at, 'DD/MM/YYYY')}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Nome do paciente:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${this.paciente.nome}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Médico:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.medico_solicitante.nome}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Exame:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.nome}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Justificativa da solicitação:</label>
                            <textarea class="input-highlight-labeless w100 capslock mt-1 custom-input-info" type="text" style="height:180px;" readonly disabled>${instance.observacao ? instance.observacao : 'Sem justificativa'}</textarea>
                        </div>
                    </div>
                    <div class="d-flex align-items-center flex-column bd-highlight mb-3 mt-2" style="padding-left: 6px;">
                        ${arquivoExameUrl}
                        ${arquivosComplementaresExames.join('')}
                        <div class="col-10 mt-2" style="text-align: center;">
                            <p style="color:#404040;">Clique no link a cima para visualizar o anexo.</p>
                        </div>
                    </div>
                </div>
            `,
            reverseButtons: true,
            showClass: {popup: 'animated fadeInDown faster',},
            hideClass: {popup: 'animated fadeOutUp faster',},
            customClass: {popup: 'custom-popup-view-exame',},
        }

        if(instance && instance.situacao !== 3 && instance.lista_chamada_solicitacao){
            swalConfig.showCancelButton = false;
            swalConfig.showConfirmButton = true;
            swalConfig.confirmButtonText = "<i class='fa-solid fa-arrow-rotate-left'></i> REABRIR SOLICITAÇÃO"; 
        }else{
            swalConfig.showCancelButton = false;
            swalConfig.showConfirmButton = false;
        }

        Swal.fire(swalConfig).then((result) => {
            if (result.isConfirmed) {
                self.confirmarReaberturaSolicitacao(tipo, instance, acao);
            }
        });
    }else if(tipo === 'documentos'){
        if(acao === 'visualizar'){
            Swal.fire({
                html: `
                    <div class="swal2-title swal2-title-custom text-left" id="swal2-title" style="display: block; height: 48px; margin-top: -32px;">
                        <h2 class="ml-3">
                            <i class="fas fa-file-pdf text-color-blue-1gov" style="font-size: 25px; margin-right: 5px;"></i>
                            <label class="text-color-blue-1gov custom-text" style="font-size: var(--font-size-scale-up-02) !important; font-weight: 700 !important;">INFORMAÇÕES DO ANEXO</label>
                            <button type="button" class="close mr-2" aria-label="Close" onclick="Swal.close()" style="border: 0px; color: var(--blue-vivid-60); background-color: var(--lt-color-gray-100) !important;">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </h2>
                    </div>

                    <div class="container" style="padding: 25px;">
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Nome do paciente:</label>
                                <input class="input-highlight-labeless capslock custom-input-info" type="text" value="${instance.paciente_nome}" readonly/>
                            </div>
                        </div>
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Descrição resumida:</label>
                                <textarea class="form-control input-highlight-labeless w100 capslock custom-input-info" type="text" style="height:180px;" readonly disabled>${instance.descricao}</textarea>
                            </div>
                        </div>
                        <div class="d-flex align-items-center flex-column bd-highlight mt-2 mb-3" style="padding-left: 6px;">
                            <div class="col-10" onclick="window.open('${instance.arquivo_url}', '_blank')" style="text-transform: uppercase; border: 1px dashed #1351b4; padding: 6px; text-align: center; cursor: pointer;">
                                <i class="fas fa-file-pdf text-color-blue-1gov" style="font-size: 25px; margin-right: 19px;"></i>
                                <span style="color: var(--interactive-light);">${instance.nome.length > 30 ? `...${instance.nome.slice(-30)}` : instance.nome}</span>
                            </div>
                            <div class="col-10" style="text-align: center;">
                                <p style="color:#404040;">Clique no link a cima para visualizar o anexo.</p>
                            </div>
                        </div>
                    </div>
                `,
                showCancelButton: false,
                showConfirmButton: false,
                reverseButtons: true,
                allowOutsideClick: true,
                cancelButton: 'custom-left-button',
                showClass: {popup: 'animated fadeInDown faster',},
                hideClass: {popup: 'animated fadeOutUp faster',},
                customClass: {popup: 'custom-popup-documentos',},
            });

        }else if(acao === 'salvar'){
            Swal.fire({
                html: `
                    <div class="swal2-title swal2-title-custom text-left" id="swal2-title" style="display: block; height: 48px; margin-top: -32px;">
                        <h2 class="ml-3">
                            <i class="fas fa-paperclip text-color-blue-1gov" style="font-size: 25px; margin-right: 5px;"></i>
                            <label class="text-color-blue-1gov custom-text" style="font-size: var(--font-size-scale-up-02) !important; font-weight: 700 !important;">ANEXAR DOCUMENTO</label>
                            <button type="button" class="close mr-2" aria-label="Close" onclick="Swal.close()" style="border: 0px; color: var(--blue-vivid-60); background-color: var(--lt-color-gray-100) !important;">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </h2>
                    </div>

                    <div class="container" style="padding: 25px;">
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Nome do paciente:</label>
                                <input class="form-control input-tab capslock" type="text" value="${self.paciente.nome}" readonly/>
                            </div>
                        </div>
                        <div class="row br-input justify-content-center mt-2">
                            <div class="col-11 br-input">
                                <label class="text-color-blue-1gov custom-text">Descrição resumida:<span class="text-danger" style="font-size: 25px;">*</span></label>
                                <textarea class="form-control w100 capslock" id="descricao-anexo" type="text" style="height:150px;"></textarea>
                            </div>
                        </div>
                        <div class="d-flex align-items-center flex-column bd-highlight mt-2 mb-3">
                            <div class="col-11" style="padding-left: 5px !important;padding-right: 0px !important;">
                                <label for="file-documento" class="drop-container" id="dropcontainer" style="border: 1px dashed #1351b4;">
                                    <i class="fas fa-box-open text-color-blue-1gov" style="font-size: 33px; margin-right: 19px;"></i>
                                    <span class="drop-title">Clique aqui para anexar o arquivo <span class="text-danger" style="font-size: 15px;">(Obrigatório)</span></span>
                                    <input type="file" id="file-documento" class="form-control input-tab" style="border: 0px" style="cursor: pointer" required>
                                </label>
                            </div>
                        </div>
                    </div>
                `,
                cancelButtonText: '<i class="fa-solid fa-xmark mr-2"></i> Cancelar',
                confirmButtonText: '<i class="fa-regular fa-floppy-disk mr-2"></i>Salvar',
                showCancelButton: true,
                showConfirmButton: true,
                // reverseButtons: true,
                allowOutsideClick: false,
                preConfirm: () => {
                    var descricaoAnexo = document.getElementById('descricao-anexo');
                    var inputFile = document.getElementById('file-documento');
                    var selectedFile = inputFile.files[0];
                    
                    if(descricaoAnexo.value === ''){
                        Swal.showValidationMessage('O campo descrição está vazio.');
                        
                        var modal = document.querySelector(".swal2-modal");
                        var validate = document.querySelector(".swal2-validation-message");

                        validate.style.setProperty("background-color", "#fff", "important");
                        modal.style.setProperty("height", "605px", "important");
                    }else if(selectedFile === undefined){
                        Swal.showValidationMessage('Por favor, anexe o arquivo.');
                        
                        var modal = document.querySelector(".swal2-modal");
                        var validate = document.querySelector(".swal2-validation-message");

                        validate.style.setProperty("margin-top", "-100px", "important");
                        validate.style.setProperty("background-color", "#fff", "important");
                        modal.style.setProperty("height", "605px", "important");
                    }else{
                        var nomeArquivo = selectedFile.name
                        this.postDocumentoPaciente(descricaoAnexo.value, selectedFile, nomeArquivo)
                    }
                    
                },
                cancelButton: 'custom-left-button-anexo',
                showClass: {popup: 'animated fadeInDown faster',},
                hideClass: {popup: 'animated fadeOutUp faster',},
                customClass: {popup: 'custom-popup-documentos',},
            });
          
        }
    }else if(tipo === 'evolucao'){
        Swal.fire({
            html: `
                <div class="swal2-title swal2-title-custom text-left" id="swal2-title" style="display: block; margin-top: -20px;">
                    <h2 class="ml-3">
                        <i class="fas fa-list-ul text-color-blue-1gov" style="font-size: 25px; margin-right: 5px;"></i>
                        <label class="text-color-blue-1gov custom-text" style="font-size: var(--font-size-scale-up-02) !important; font-weight: 700 !important;">INFORMAÇÕES DA EVOLUÇÃO</label>
                        <button type="button" class="close mr-2" aria-label="Close" onclick="Swal.close()" style="border: 0px; color: var(--blue-vivid-60); background-color: var(--lt-color-gray-100) !important;">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </h2>
                </div>
                
                <div class="container" style="padding: 50px; margin-top: -30px; padding-left: 20px;">
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-6 br-input">
                            <label class="text-color-blue-1gov custom-text">Data:</label>
                            <input class="custom-input-info input-tab capslock" type="text" value="${this.convertDate(instance.created_at, 'DD/MM/YYYY')}" readonly disabled />
                        </div>
                        <div class="col-5 br-input">
                            <label class="text-color-blue-1gov custom-text">Hora:</label>
                            <input class="custom-input-info input-tab capslock" type="text" value="${this.convertDate(instance.created_at, 'H:mm')}" readonly disabled />
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Nº Atendimento:</label>
                            <input class="custom-input-info input-tab capslock" type="text" value="${instance.numero_evolucao_formatado}" readonly disabled />
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Nome do paciente:</label>
                            <input class="custom-input-info input-tab capslock" type="text" value="${instance.paciente_nome}" readonly disabled />
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Médico:</label>
                            <input class="custom-input-info input-tab capslock" type="text" value="${instance.profissional.nome}" readonly disabled />
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Evolução:</label>
                            <textarea class="custom-input-info input-highlight-labeless w100 capslock mt-1" type="text" style="height:180px;" readonly disabled>${instance.registro_evolucao}</textarea>
                        </div>
                    </div>
                </div>
            `,
            showCancelButton: false,
            showConfirmButton: false,
            reverseButtons: true,
            allowOutsideClick: true,
            cancelButton: 'custom-left-button',
            showClass: {popup: 'animated fadeInDown faster',},
            hideClass: {popup: 'animated fadeOutUp faster',},
            customClass: { container: 'swal2-modal-evolucao', popup: 'custom-popup-view-evolucao',},
        });
    }else if(tipo === 'diagnostico'){
        let arquivoUrl = [];
        if(instance.arquivo_url && instance.nome_arquivo){
            arquivoUrl.push(
                `<div class="col-10" onclick="window.open('${instance.arquivo_url}', '_blank')" style="text-transform: uppercase; border: 1px dashed #1351b4; padding: 6px; text-align: center; cursor: pointer;">
                    <i class="fas fa-file-image text-color-blue-1gov" style="font-size: 25px; margin-right: 19px;"></i>
                    <span style="color: var(--interactive-light);">${instance.nome_arquivo.length > 30 ? `...${instance.nome_arquivo.slice(-30)}` : instance.nome_arquivo}</span>
                </div>`
            )
        }else{
            arquivoUrl.push(`<div class="col-10" style="text-transform: uppercase; border: 1px dashed #1351b4; padding: 6px; text-align: center;">
                    <i class="fas fa-file-image text-color-blue-1gov" style="font-size: 25px; margin-right: 19px;"></i>
                    <span style="color: var(--interactive-light);">Sem arquivo anexado</span>
                </div>`
            )
        }
        Swal.fire({
            html: `
                <div class="swal2-title swal2-title-custom text-left" id="swal2-title" style="display: block; height: 48px; margin-top: -32px;">
                    <h2 class="ml-3">
                        <i class="fas fa-list-ul text-color-blue-1gov" style="font-size: 25px; margin-right: 5px;"></i>
                        <label class="text-color-blue-1gov custom-text" style="font-size: var(--font-size-scale-up-02) !important; font-weight: 700 !important;">INFORMAÇÕES DO DIAGNÓSTICO</label>
                        <button type="button" class="close mr-2" aria-label="Close" onclick="Swal.close()" style="border: 0px; color: var(--blue-vivid-60); background-color: var(--lt-color-gray-100) !important;">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </h2>
                </div>
               
                <div class="container" style="padding: 25px;">
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-6 br-input">
                            <label class="text-color-blue-1gov custom-text">Data:</label>
                            <input class="custom-input-info input-highlight-labeless capslock custom-input-info" value="${this.convertDate(instance.created_at, 'DD/MM/YYYY')}" type="text" readonly disabled>
                        </div>
                        <div class="col-5 br-input">
                            <label class="text-color-blue-1gov custom-text">Nº atendimento:</label>
                            <input class="custom-input-info input-highlight-labeless capslock custom-input-info" value="${instance.numero_diagnostico_formatado}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Médico:</label>
                            <input class="custom-input-info input-highlight-labeless capslock custom-input-info" value="${instance.profissional.nome}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Nome do paciente:</label>
                            <input class="custom-input-info input-highlight-labeless capslock custom-input-info" value="${instance.paciente_nome}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">CID:</label>
                            <input class="custom-input-info input-highlight-labeless capslock custom-input-info" value="${instance.cid_nome}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Descrição:</label>
                            <textarea class="custom-input-info input-highlight-labeless w100 capslock mt-1" type="text" style="height:180px;" readonly disabled>${instance.descricao ? instance.descricao : 'Sem descrição'}</textarea>
                        </div>
                    </div>
                    <div class="d-flex align-items-center flex-column bd-highlight mt-2 mb-3" style="padding-left: 6px;">
                        ${arquivoUrl}
                        <div class="col-10" style="text-align: center;">
                            <p style="color:#404040;">Clique no link a cima para visualizar o anexo.</p>
                        </div>
                    </div>
                </div>
            `,
            showCancelButton: false,
            showConfirmButton: false,
            reverseButtons: true,
            allowOutsideClick: true,
            cancelButton: 'custom-left-button',
            showClass: {popup: 'animated fadeInDown faster',},
            hideClass: {popup: 'animated fadeOutUp faster',},
            customClass: {popup: 'custom-popup-view-diagnostico',},
        });
    }else if(tipo === 'medicacao'){
        let situacaoMedicacoes = [];
        
        if (instance.situacao_medicacao_atendimento.length > 0) {
            instance.situacao_medicacao_atendimento.forEach((item) => {
                if(!item.cancelado){
                    situacaoMedicacoes.push(`<span class="br-tag small" style="background: #959ea9 !important; height: 30px;"><span id="densidade01">${this.convertDate(item.data_hora_aplicacao, 'LT')}</span></span>`);
                }else{
                    situacaoMedicacoes.push(`<span class="br-tag small" style="background: #e52207 !important; height: 30px;"><span id="densidade01">SUSPENSO</span></span>`);
                }
            })
        }else{
            situacaoMedicacoes.push(`<div class="mt-2" style="text-align: center;">Sem registro de informações.</div>`);
        }
        
        const swalConfig = {
            html: `
                <div class="swal2-title swal2-title-custom text-left" id="swal2-title" style="display: block; margin-top: -20px;">
                    <h2 class="ml-3">
                        <i class="fas fa-syringe text-color-blue-1gov" style="font-size: 25px; margin-right: 5px;"></i>
                        <label class="text-color-blue-1gov custom-text" style="font-size: var(--font-size-scale-up-02) !important; font-weight: 700 !important;">INFORMAÇÕES DA MEDICAÇÃO</label>
                        <button type="button" class="close mr-2" aria-label="Close" onclick="Swal.close()" style="border: 0px; color: var(--blue-vivid-60); background-color: var(--lt-color-gray-100) !important;">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </h2>
                </div>
               
                <div class="container" style="padding: 25px;">
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Nome do paciente:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.paciente_nome}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Médico:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.medico_nome}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Medicação:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.medicamento_nome}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Tipo parental:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.tipo_parenteral_nome ? instance.tipo_parenteral_nome : 'Sem informação'}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-6 br-input">
                            <label class="text-color-blue-1gov custom-text">Via:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.admin_medicamentosa_nome}" type="text" readonly disabled>
                        </div>
                        <div class="col-5 br-input">
                            <label class="text-color-blue-1gov custom-text">Duração do tratamento:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${this.calcularMeses(instance.duracao_tratamento)}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-6 br-input">
                            <label class="text-color-blue-1gov custom-text">Aplicação:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.aplicacao == 0 ? 'IMEDIATA' : 'POSTERIOR'}" type="text" readonly disabled>
                        </div>
                        <div class="col-5 br-input">
                            <label class="text-color-blue-1gov custom-text">Uso contínuo:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.uso_continuo ? 'SIM' : 'NÃO'}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-6 br-input">
                            <label class="text-color-blue-1gov custom-text">Dosagem:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.dosagem ? instance.dosagem : 'Sem informação'}" type="text" readonly disabled>
                        </div>
                        <div class="col-5 br-input">
                            <label class="text-color-blue-1gov custom-text">Posologia:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.posologia ? instance.posologia : (instance.dose_unica === true ? 'DOSE ÚNICA' : 'Sem informação')}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Medicamento Controlado:</label>
                            <input class="input-highlight-labeless capslock custom-input-info" value="${instance.medicamento_controlado === true ? 'SIM' : 'NÃO'}" type="text" readonly disabled>
                        </div>
                    </div>
                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 br-input">
                            <label class="text-color-blue-1gov custom-text">Descrição:</label>
                            <textarea class="custom-input-info input-highlight-labeless w100 capslock mt-1" type="text" style="height:180px;" readonly disabled>${instance.observacao ? instance.observacao : 'Sem descrição'}</textarea>
                        </div>
                    </div>

                    <div class="row br-input justify-content-center mt-2">
                        <div class="col-11 text-center">
                            <label class="text-color-blue-1gov custom-text">Aplicações dos Medicamentos:</label>
                        </div>
                        <div class="col-11 text-center mt-2">
                            ${situacaoMedicacoes.join(' ')}
                        </div>
                    </div>
                </div>
            `,
            reverseButtons: true,
            allowOutsideClick: true,
            cancelButton: 'custom-left-button',
            showClass: {popup: 'animated fadeInDown faster',},
            hideClass: {popup: 'animated fadeOutUp faster',},
            customClass: {popup: 'custom-popup-view-medicacao',},
        }

        if(instance.situacao !== 4 && instance.lista_chamada_solicitacao){
            swalConfig.showCancelButton = false;
            swalConfig.showConfirmButton = true;
            swalConfig.confirmButtonText = "<i class='fa-solid fa-arrow-rotate-left'></i> REABRIR SOLICITAÇÃO"; 
        }else{
            swalConfig.showCancelButton = false;
            swalConfig.showConfirmButton = false;
        }

        Swal.fire(swalConfig).then((result) => {
            if (result.isConfirmed) {
                self.confirmarReaberturaSolicitacao(tipo, instance, acao);
            }
        });
    }
},
confirmarReaberturaSolicitacao(tipo, instance=null, acao=null){
    self = this;

    Swal.fire({
        title: "Atenção",
        text: "Deseja Realmente efetuar a reabertura dessa solicitação?",
        icon: "warning",
        input: "textarea",
        showCancelButton: true,
        confirmButtonText: "Confirmar",
        cancelButtonText: "Cancelar",
        allowOutsideClick: false,
        customClass: {popup: 'custom-popup-view-exame-confirmacao-reabertura',},
        preConfirm: () => {
            let value = $('#swal2-textarea').val();

            if(!value){
                Swal.showValidationMessage('Adicione uma observação!');
            }else{
                let url  = "{% url 'saude_atendimento:atendimentos-reabertura-solicitacao' pk='00000000-0000-0000-0000-000000000000' %}"
                axios.put(url.replace('00000000-0000-0000-0000-000000000000', instance.id), { tipo: tipo, justificativa: value })
                .then((response) => {
                    let titulo = `${tipo} reaberto com sucesso!`
                    
                    self.SweetAlert(titulo, "success")

                    if(tipo === 'exame'){
                        self.crudExame('GET')
                    }else if(tipo === 'medicacao'){
                        self.crudMedicacaoAtendimento('GET')
                    }else if(tipo === 'procedimento'){
                        self.crudProcedimentoAtendimento('GET')
                    }
                }); 
            }
        }
    }).then((result) => {
        if (result.isDismissed) {
            self.visualizarInformacoes(tipo, instance, acao);
        }
    });
},
handleFileChange(event) {
    const file = event.target.files[0];
    this.formularioDiagnostico.arquivo = file;
    this.formularioDiagnostico.nomeArquivo = file.name
},
atualizarCheckbox(tipo, option) {
    if(tipo === 'situacaoRua'){
        if (this.listagemHistoricoPatologico.tempo_situacao_de_rua === option) {
            this.listagemHistoricoPatologico.tempo_situacao_de_rua = null;
        } else {
            this.listagemHistoricoPatologico.tempo_situacao_de_rua = option;
        }
    }else if(tipo === 'frequenciaDiaria'){
        if (this.listagemHistoricoPatologico.frequencia_diaria_alimentacao === option) {
            this.listagemHistoricoPatologico.frequencia_diaria_alimentacao = null;
        } else {
            this.listagemHistoricoPatologico.frequencia_diaria_alimentacao = option;
        }
    }else if(tipo === 'situacaoPeso'){
        if (this.listagemHistoricoPatologico.situacao_peso === option) {
            this.listagemHistoricoPatologico.situacao_peso = null;
        } else {
            this.listagemHistoricoPatologico.situacao_peso = option;
        }
    }
},
convertDate(originalDate, format) {
    const convertedDate = moment(originalDate).format(format);
  
    return convertedDate;
},
showModalDelete(tipo, titulo, object=null){
    Swal.fire({
        imageUrl: "{% static 'img/icons/icone_atencao.svg' %}",
        imageWidth: 125,
        imageHeight: 125,
        imageAlt: "Custom image",
        title: 'Atenção!',
        text: `Deseja realmente remover este(a) ${titulo.toLowerCase()}?`,
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "<i class='fa-solid fa-trash mr-2'></i> Deletar",
        cancelButtonText: "<i class='fa-solid fa-xmark mr-2'></i> Cancelar",
        reverseButtons: true,
        customClass: {popup: 'custom-delete-view', actions: 'swal2-actions-delete', title: 'swal2-title-delete'},
    }).then((result) => {
        if (result.isConfirmed) {
            if(tipo === 'exame'){
                this.crudExame('DELETE', object)
            }else if(tipo === 'procedimento'){
                this.crudProcedimentoAtendimento('DELETE', object)
            }else if(tipo === 'medicação'){
                this.crudMedicacaoAtendimento('DELETE', object)
            }
        }
    });
},
prevPage() {
    if (this.currentPage > 1) {
        this.currentPage--;
        this.getHistoricoAnteriores();
    }
},
nextPage() {
    if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.getHistoricoAnteriores();
    }
},
goToPage(page) {
    this.currentPage = page;
    this.getHistoricoAnteriores();
},
SweetAlert(titulo, icon){
    Swal.fire({
        toast: true,
        position: "top-end",
        title: titulo,
        icon: icon,
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
        didOpen: (toast) => {toast.onmouseenter = Swal.stopTimer; toast.onmouseleave = Swal.resumeTimer;
        },
        customClass: {container: 'custom-swal-container', title: 'custom-swal-title'},
    });
},
alertFinalizarBoletim(boletimPk, listaChamadoPk, pacienteNome){
    self = this;
    
    Swal.fire({
        html: `
        <div class="swal2-title swal2-title-custom text-left" id="swal2-title" style="display: block; height: 48px; margin-top: -32px;">
            <h2 class="ml-3">
                <i class="fas fa-syringe text-color-blue-1gov" style="font-size: 25px; margin-right: 5px;"></i>
                <label class="text-color-blue-1gov custom-text" style="font-size: var(--font-size-scale-up-02) !important; font-weight: 700 !important;">Alta do Paciente</label>
                <button type="button" class="close mr-2" aria-label="Close" onclick="Swal.close()" style="border: 0px; color: var(--blue-vivid-60); background-color: var(--lt-color-gray-100) !important;">
                    <span aria-hidden="true">&times;</span>
                </button>
            </h2>
        </div>
    
        <div class="container" style="padding: 12px; padding-left: 25px; padding-right: 25px;">
            <div class="row br-input justify-content-center mt-2">
                <div class="col-11 br-input">
                    <label class="text-color-blue-1gov custom-text">Paciente:</label>
                    <input class="form-control input-tab capslock" type="text" value="${self.paciente.nome}" readonly/>
                </div>
            </div>
            <div class="row br-input justify-content-center mt-2">
                <div class="col-6 br-input">
                    <label class="text-color-blue-1gov custom-text">Data:</label>
                    <input class="form-control input-tab capslock" type="text" value="${self.dataAtual}" readonly/>
                </div>
                <div class="col-5 br-input">
                    <label class="text-color-blue-1gov custom-text">Hora:</label>
                    <input class="form-control input-tab capslock" type="text" value="${self.horaAtual}" readonly/>
                </div>
            </div>
            <div class="row br-input justify-content-center mt-2">
                <div class="col-11 br-input">
                    <label class="text-color-blue-1gov custom-text">Tipo:</label>
                    <div class="br-input">
                        <select id="tipoSelect" class="select-custom" style="height: 51px;>
                            <option value="">SELECIONE UMA OPÇÃO</option>
                            <option value="">SELECIONE UMA OPÇÃO</option>
                            <option value="2">CURADO</option>
                            <option value="3">ÓBITO</option>
                            <option value="4">REVELIA</option>
                            <option value="5">MELHORADO</option>
                            <option value="6">INALTERADO</option>
                            <option value="7">TRANSFERÊNCIA</option>
                            <option value="8">DECISÃO MÉDICA</option>
                            <option value="9">ENCERRAMENTO ADMINISTRATIVO</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
        `,
        confirmButtonColor: "#1250b4",
        confirmButtonText: '<i class="fa-regular fa-floppy-disk mr-2"></i>Salvar',
        cancelButtonText: '<i class="fa-solid fa-xmark mr-2"></i> Fechar',
        showCancelButton: true,
        showConfirmButton: true,
        allowOutsideClick: false,
        reverseButtons: true,
        customClass: {container: 'swal2-modal-alta-hospitalar-paciente', popup: 'custom-popup-view-alta-do-paciente'},
        preConfirm: () => {
            const selectElement = document.getElementById('tipoSelect');
            const selectedValue = selectElement.value;

            if (selectedValue === '') {
                Swal.showValidationMessage('Selecione o tipo da alta!');
                var modal = document.querySelector(".swal2-modal");
                var validate = document.querySelector(".swal2-validation-message");

                validate.style.setProperty("background-color", "transparent", "important");
                validate.style.setProperty("z-index", "1", "important");
                validate.style.setProperty("font-size", "20px", "important");
                validate.style.setProperty("height", "80px", "important");
                validate.style.setProperty("margin-top", "-50px", "important");
                validate.style.setProperty("opacity", "1", "important");
                validate.style.setProperty("color", "black", "important");
                validate.style.setProperty("margin-left", "-18px", "important");
                modal.style.setProperty("height", "480px", "important");
            } else {
                self.finalizarBoletim(selectedValue)
            }
        },
    });
},
replaceUrlId(url, Id) {
    return url.replace('00000000-0000-0000-0000-000000000000', Id);
},
calcularMeses(duracaoTratamento) {
    const meses = Math.floor(duracaoTratamento / 30);
    const diasRestantes = duracaoTratamento % 30;
    
    if (meses > 0 && diasRestantes > 0) {
        return `${meses} mês${meses > 1 ? 'es' : ''} e ${diasRestantes} dia${diasRestantes > 1 ? 's' : ''}`;
    } else if (meses > 0) {
        return `${meses} mês${meses > 1 ? 'es' : ''}`;
    } else if(duracaoTratamento){
        return `${duracaoTratamento} dia${duracaoTratamento > 1 ? 's' : ''}`;
    }
},
EditarCancelarMedicacao(type, object=null){
    if(type === 'editar'){
        const adminMedicamentosa = `${object.admin_medicamentosa}`
        const parental = object.tipo_parenteral ? `${object.tipo_parenteral}` : ''

        $(".via-admin").val(adminMedicamentosa).trigger('change');
        $(".parental").val(parental).trigger('change');
        $(".posologia").val(parseInt(object.posologia)).trigger('change');

        this.formularioMedicacao.id = object.id
        this.formularioMedicacao.via = adminMedicamentosa
        this.formularioMedicacao.parental = parental
        this.formularioMedicacao.doseUnica = object.dose_unica
        this.formularioMedicacao.medicamentoControlado = object.medicamento_controlado
        this.formularioMedicacao.posologia = parseInt(object.posologia)
        this.formularioMedicacao.dosagem = object.dosagem
        this.formularioMedicacao.tipoPosologia = object.numero_tipo_posologia
        this.formularioMedicacao.duracaoTratamento = object.duracao_tratamento
        this.formularioMedicacao.observacao = object.observacao
        this.formularioMedicacao.aplicacao = `${object.aplicacao}`
        this.formularioMedicacao.usoContinuo = object.uso_continuo

        $(".via-admin").val(object.admin_medicamentosa).trigger('change');
        this.$nextTick(() => {this.$refs.customMedicacaoAtendimento.selectOption(object.medicacao)});

        const focusContainer = document.getElementById('focus-container-medicamentos');
        if (focusContainer) {
            focusContainer.scrollIntoView({ behavior: 'smooth' });
            focusContainer.focus();
        }
    }else{
        this.formularioMedicacao.id = ''
        this.formularioMedicacao.via = ''
        this.formularioMedicacao.parental = ''
        this.formularioMedicacao.medicacaoPk = null
        this.formularioMedicacao.doseUnica = true
        this.formularioMedicacao.posologia = ''
        this.formularioMedicacao.dosagem = ''
        this.formularioMedicacao.tipoPosologia = 0
        this.formularioMedicacao.duracaoTratamento = 1
        this.formularioMedicacao.observacao = ''
        this.formularioMedicacao.quantidade = 0
        this.formularioMedicacao.aplicacao = '0'
        this.formularioMedicacao.usoContinuo = false

        $(".via-admin").val('').trigger('change');
        $(".parental").val('').trigger('change');
        $(".posologia").val('').trigger('change');
        this.$nextTick(() => {this.$refs.customMedicacaoAtendimento.selectOption(null)});
    }
},
EditarCancelarProcedimentos(type, id=null, quantidade=null, procedimentoId=null, classificacao=null, procedimentoSelecionado=null, realizadoPor, tipoSolicitacao){
    if(type === 'editar'){
        this.formularioProcedimento.id = id
        this.formularioProcedimento.quantidade = quantidade
        this.formularioProcedimento.classificacao = classificacao
        this.formularioProcedimento.tipoSolicitacao = tipoSolicitacao
        this.formularioProcedimento.realizadoPor = realizadoPor
    
        this.$nextTick(() => {this.$refs.customProcediemento.selectOption(procedimentoSelecionado)});
        
        const focusContainer = document.getElementById('focus-container-topo-procedimentos');
        if (focusContainer) {
            focusContainer.scrollIntoView({ behavior: 'smooth' });
            focusContainer.focus();
        }
        
    }else{
        this.formularioProcedimento.id = ''
        this.formularioProcedimento.quantidade = 1
        this.formularioProcedimento.classificacao = 1
        this.formularioProcedimento.tipoSolicitacao = 0
        this.formularioProcedimento.realizadoPor = 0
        this.$nextTick(() => {this.$refs.customProcediemento.selectOption(null)});
    }
},
EditarEvolucao(id=null, registroEvolucao=null, evolucaoRetorno=null){
    this.formularioEvolucao.id = id
    this.formularioEvolucao.registroEvolucao = registroEvolucao
    this.formularioEvolucao.evolucaoRetorno = evolucaoRetorno   
    
    const focusContainer = document.getElementById('focus-container-evolucao');
    if (focusContainer) {
        focusContainer.scrollIntoView({ behavior: 'smooth' });
        focusContainer.focus();
    }
},
verificarSairAtendimento(){
    if(this.verificarSeTemProcedimentoMedico){
        Swal.fire({
            title: 'Atenção!',
            text: 'Você possui procedimentos médicos pendentes, deseja realmente sair do atendimento?',
            icon: "warning",
            showCancelButton: true,
            showConfirmButton: true,
            confirmButtonText: "<i class='fa-solid fa-reply mr-2'></i> CONFIRMAR",
            cancelButtonText: "<i class='fa-solid fa-xmark mr-2'></i> CANCELAR",
            reverseButtons: true,
            allowOutsideClick: false,
            customClass: {popup: 'custom-popup-view-sair-atendimento', confirmButton: 'swal2-confirm-custom', cancelButton: 'swal2-cancel-custom'},
            preConfirm: () => {
                window.location.href = "{% url 'saude_atendimento:atendimento_medico_list' %}"
            },
        });
    }else{
        window.location.href = "{% url 'saude_atendimento:atendimento_medico_list' %}"
    }
},
verificarConcederAlta(){
    if(this.verificarSeTemProcedimentoMedico){
        Swal.fire({
            title: 'Atenção!',
            text: 'Não é possível conceder alta ao paciente, pois existem procedimentos médicos pendentes.',
            icon: "warning",
            showCancelButton: true,
            showConfirmButton: false,
            cancelButtonText: "<i class='fa-solid fa-xmark mr-2'></i> FECHAR",
            reverseButtons: true,
            allowOutsideClick: false,
            customClass: {popup: 'custom-popup-view-sair-atendimento', confirmButton: 'swal2-confirm-custom', cancelButton: 'swal2-cancel-custom'},
        });
    }else{
        this.alertFinalizarBoletim()
    }
}