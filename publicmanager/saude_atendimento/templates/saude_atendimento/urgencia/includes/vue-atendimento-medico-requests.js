getProcedimentos(search) {
    var apiUrl = "{% url 'saude_cadastro:api_procedimento_list' %}";
    return axios.get(apiUrl, { params: { search } });
},
getCids(search) {
    var apiUrl = "{% url 'saude_cadastro:api_cid_list' %}";
    return axios.get(apiUrl, { params: { search } });
},
getExames(search) {
    var apiUrl = "{% url 'saude_cadastro:api_exame_list' %}";
    return axios.get(apiUrl, { params: { search } });
},
getMedicacoes(search) {
    var apiUrl = `{% url 'saude_farmacia:api_lista_medicamentos' %}?unidade_saude_id=${this.unidadeSaudeSessionId}`;
    return axios.get(apiUrl, { params: { search } });
},
getPrincipioAtivo(search) {
    var apiUrl = "{% url 'saude_farmacia:api_principio_ativo' %}";
    return axios.get(apiUrl, { params: { search } });
},
getAtendimentoMedico(){
    this.isLoadingPage = true

    axios.get(`{% url 'saude_atendimento:atendimentos-get-atendimento-medico' object.lista_chamada_atendimento_medico_set.pk %}`)
    .then((response)=>{  
        this.atendimentoMedico = response.data

        const arrayOrdenado = response.data.sinais_vitais[response.data.sinais_vitais.length - 1]
        
        this.formularioReclassificacao = {
            tipoClassificacaoRiscoId: response.data.classificacao.tipo_classificacao_risco.id,
            presaoArterial: arrayOrdenado.presao_arterial,
            frequenciaCardiaca: arrayOrdenado.frequencia_cardiaca,
            frequenciaRespiratoria: arrayOrdenado.frequencia_respiratoria,
            temperatura: arrayOrdenado.temperatura,
            spo2: arrayOrdenado.spo2,
            hgt: arrayOrdenado.hgt,
        };
    }).finally(() => {
        this.isLoadingPage = false
    })
},
finalizarBoletim(situacaoAltaPaciente){
    let url  = "{% url 'saude_atendimento:api_finalizar_boletim' pk='00000000-0000-0000-0000-000000000000' %}"
    axios.put(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.boletimPk), {"chamado_id": this.paciente.listaChamadoPk, "situacao": situacaoAltaPaciente, 'situacao_chamado': 5})
    .then((response)=>{
        window.location.replace(this.urlRedirect);
    });
},
postEvolucao(metodo, evolucaoId=null){
    if(metodo === 'POST'){
        let url  = "{% url 'saude_atendimento:atendimentos-criar-atualizar-historico-evolucao' pk='00000000-0000-0000-0000-000000000000' %}"
        axios.post(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK), {"evolucao": this.formularioEvolucao.registroEvolucao, "retorno": this.formularioEvolucao.evolucaoRetorno})
        .then((response)=>{
            this.formularioEvolucao.evolucaoRetorno =  true
            this.formularioEvolucao.registroEvolucao = ""
            this.atendimentoMedico.evolucao = response.data
            this.SweetAlert("EVOLUÇÃO SALVO COM SUCESSO!", "success")
        });
    }else if(metodo === 'PUT'){
        let url  = "{% url 'saude_atendimento:atendimentos-criar-atualizar-historico-evolucao' pk='00000000-0000-0000-0000-000000000000' %}"
        axios.put(url.replace('00000000-0000-0000-0000-000000000000', evolucaoId), {"evolucao": this.formularioEvolucao.registroEvolucao, "retorno": this.formularioEvolucao.evolucaoRetorno})
        .then((response)=>{
            this.formularioEvolucao.id =  ''
            this.formularioEvolucao.evolucaoRetorno =  true
            this.formularioEvolucao.registroEvolucao = ""

            this.atendimentoMedico.evolucao = response.data
            this.SweetAlert("EVOLUÇÃO ATUALIZADA COM SUCESSO!", "success")
        });
    }
},
postDagnostico(){
    const formularioDiagnostico = new FormData();
    formularioDiagnostico.append('cid', this.formularioDiagnostico.cid.value);
    formularioDiagnostico.append('arquivo', this.formularioDiagnostico.arquivo);
    formularioDiagnostico.append('descricao', this.formularioDiagnostico.descricao);
    formularioDiagnostico.append('nome_arquivo', this.formularioDiagnostico.nomeArquivo);

    let url  = "{% url 'saude_atendimento:atendimentos-criar-diagnostico-atendimento' pk='00000000-0000-0000-0000-000000000000' %}"
    axios.post(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK), formularioDiagnostico, {
        headers: { 'Content-Type': 'multipart/form-data'},
    }).then((response) => {
        this.atendimentoMedico.diagnostico = response.data

        this.formularioDiagnostico.nomeArquivo = '';
        this.formularioDiagnostico.arquivo = '';
        this.formularioDiagnostico.descricao = '';
        this.$refs.diagnosticoForm.reset();
        this.$nextTick(() => {this.$refs.customDiagnosticoCid.selectOption(null)});
        this.SweetAlert("DIAGNÓSTICO SALVO COM SUCESSO!", "success")

    });
},
postPutReclassificacao(){
    const formularioReclassificacao = new FormData();formularioReclassificacao.append('tipo_lassificacao_risco_id', this.formularioReclassificacao.tipoClassificacaoRiscoId);
    formularioReclassificacao.append('queixa_principal', this.atendimentoMedico.classificacao.queixa_principal);
    formularioReclassificacao.append('peso', this.atendimentoMedico.classificacao.peso);
    formularioReclassificacao.append('altura', this.atendimentoMedico.classificacao.altura);
    formularioReclassificacao.append('escala_dor', this.atendimentoMedico.classificacao.escala_dor);
    formularioReclassificacao.append('estado_geral', this.atendimentoMedico.classificacao.estado_geral);
    formularioReclassificacao.append('observacao', this.atendimentoMedico.classificacao.observacao);
    formularioReclassificacao.append('tipo_classificacao_risco_id', this.formularioReclassificacao.tipoClassificacaoRiscoId);
    formularioReclassificacao.append('presao_arterial', this.formularioReclassificacao.presaoArterial);
    formularioReclassificacao.append('frequencia_cardiaca', this.formularioReclassificacao.frequenciaCardiaca);
    formularioReclassificacao.append('frequencia_respiratoria', this.formularioReclassificacao.frequenciaRespiratoria);
    formularioReclassificacao.append('temperatura', this.formularioReclassificacao.temperatura);
    formularioReclassificacao.append('spo2', this.formularioReclassificacao.spo2);
    formularioReclassificacao.append('hgt', this.formularioReclassificacao.hgt);

    let url  = "{% url 'saude_atendimento:atendimentos-reclassificacao' pk='00000000-0000-0000-0000-000000000000' %}"
    axios.post(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK), formularioReclassificacao, {
        headers: { 'Content-Type': 'multipart/form-data'},
    }).then((response) => {
        this.getAtendimentoMedico()
        this.reclassification = false
        this.SweetAlert("RECLASSIFICACAO SALVO COM SUCESSO!", "success")

    })
},
getPutHistoricoPatologico(metodo){
    let url  = "{% url 'saude_atendimento:atendimentos-historico-patologico' pk='00000000-0000-0000-0000-000000000000' %}"
    
    if(metodo === 'GET'){
        axios.get(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK))
        .then((response)=>{
            this.listagemHistoricoPatologico = response.data

            this.$nextTick(() => {
                
                response.data.alergias.forEach((alergia) => {
                    this.$refs.customSelect.selectOption(alergia);
                });
                response.data.antecedentes_patologicos.forEach((patologico) => {
                    this.$refs.customAntecedentesPatologicos.selectOption(patologico);
                });

                response.data.patologicos_familiares.forEach((familiar) => {
                    this.$refs.customPatologicosFaliliares.selectOption(familiar);
                });
            });

            for (const [key, value] of Object.entries(response.data)) {
                if (key !== 'id') {
                    if (value === true || (typeof value === 'string' && value !== '') || (Array.isArray(value) && value.length > 0)) {
                        this.bloqueioPatologicoForm = true;
                        break;
                    }
                }
            }
        })
    }else if(metodo === 'PUT'){
        const formularioPatologico = new FormData();
        for (const propriedade in this.listagemHistoricoPatologico) {
            if(propriedade === 'alergias_medicamentosas'){
                formularioPatologico.append(propriedade, this.selectedPrincipioValues.map(principio => principio.value));
            }else if(propriedade === 'antecedentes_patologicos_pessoais'){
                formularioPatologico.append(propriedade, this.selectedPessoaisValues.map(pessoais => pessoais.value));
            }else if(propriedade === 'antecedentes_patologicos_familiares'){
                formularioPatologico.append(propriedade, this.selectedFamiliaresValues.map(familiar => familiar.value));
            }else{
                formularioPatologico.append(propriedade, this.listagemHistoricoPatologico[propriedade]);
            }
        }

        axios.put(url.replace('00000000-0000-0000-0000-000000000000', this.listagemHistoricoPatologico.id), formularioPatologico, {
            headers: { 'Content-Type': 'multipart/form-data'},
        }).then((response)=>{
            this.bloqueioPatologicoForm = true
            this.SweetAlert("ANAMNESE ATUALIZADA COM SUCESSO!", "success")
        });

    }
},
getHistoricoAnteriores(){
    let params = `page=${this.currentPage}&page_size=${this.pageSize}`
    this.loadingTable = true

    let url  = `{% url 'saude_atendimento:atendimentos-get-historico-ateriores' pk='00000000-0000-0000-0000-000000000000' %}?${params}`
    axios.get(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.id))
    .then((response)=>{
        this.listagemHistoricoAnteriores = response.data.results
        this.resultsTotal = response.data.count
        this.totalPages = Math.ceil(response.data.count / response.data.page_size);
    }).finally(() => {
        this.loadingTable = false
    })
},
crudExame(metodo, exame=null){
    let url  = "{% url 'saude_atendimento:atendimentos-exame-atendimento' pk='00000000-0000-0000-0000-000000000000' %}"
    if(metodo === 'GET'){
        axios.get(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK))
        .then((response)=>{
            this.listagemExames = response.data
        });
    }else if(metodo === 'POST'){
        const forExame = new FormData();
        forExame.append('exame', this.selectExame ? this.selectExame.value : '');
        forExame.append('observacao', this.formularioExame.observacao);

        axios.post(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK), forExame, {
            headers: { 'Content-Type': 'multipart/form-data'},
        }).then((response) => {
            this.listagemExames = response.data
            this.formularioExame.observacao = ''
            this.$nextTick(() => {this.$refs.customExames.selectOption(null)});
            this.SweetAlert("EXAME SALVO COM SUCESSO!", "success")
        }); 
    }else if(metodo === 'PUT'){
        const forExame = new FormData();
        forExame.append('arquivo_nome', this.formularioExame.nomeArquivoAnexo);
        forExame.append('arquivo', this.formularioExame.arquivoAnexo);

        axios.put(url.replace('00000000-0000-0000-0000-000000000000', exame.id), forExame, {
            headers: { 'Content-Type': 'multipart/form-data'},
        }).then((response) => {
            const foundExame = this.listagemExames.find(param => param.id === response.data.id);

            if (foundExame) {
                foundExame.arquivo_nome = response.data.arquivo_nome;
                foundExame.arquivo = response.data.arquivo;
            }
            this.SweetAlert("EXAME ANEXADO COM SUCESSO!", "success")
        });

    }else if(metodo === 'DELETE'){
        axios.delete(url.replace('00000000-0000-0000-0000-000000000000', exame.id))
        .then((response)=>{
            this.listagemExames.splice(this.listagemExames.indexOf(exame), 1)
            
            this.deleteTitulo = ''
            this.formularioExame.id = ''
            this.formularioExame.deleteExame = ''
            this.formularioExame.justificativa = ''
            this.$nextTick(() => {this.$refs.customExames.selectOption(null)});
            this.SweetAlert("EXAME DELETADO COM SUCESSO!", "warning")
        });
    }
},
crudProcedimentoAtendimento(metodo, procedimento=null){
    let url  = "{% url 'saude_atendimento:atendimentos-procedimento-atendimento' pk='00000000-0000-0000-0000-000000000000' %}"
    if(metodo === 'GET'){
        axios.get(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK))
        .then((response)=>{
            this.listagemProcedimentos = response.data
            this.crudJustificativaProcedimentoAtendimento('GET')
        });
    }else if(metodo === 'POST'){
        const formularioProcedimento = new FormData();
        formularioProcedimento.append('procedimento', this.formularioProcedimento.procedimentoPk);
        formularioProcedimento.append('quantidade', this.formularioProcedimento.quantidade);
        formularioProcedimento.append('classificacao', this.formularioProcedimento.classificacao);
        formularioProcedimento.append('tipo_solicitacao', this.formularioProcedimento.tipoSolicitacao);
        formularioProcedimento.append('realizado_por', this.formularioProcedimento.realizadoPor);

        axios.post(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK), formularioProcedimento, {
            headers: { 'Content-Type': 'multipart/form-data'},
        }).then((response) => {
            this.listagemProcedimentos = response.data

            this.formularioProcedimento.id = '';
            this.formularioProcedimento.quantidade = 1;
            this.formularioProcedimento.classificacao = 1;
            this.formularioProcedimento.tipoSolicitacao = 0
            this.formularioProcedimento.realizadoPor = 0
            this.$nextTick(() => {this.$refs.customProcediemento.selectOption(null)});
            this.SweetAlert("PROCEDIMENTO SALVO COM SUCESSO!", "success")
        });  
    }else if(metodo === 'PUT'){
        const formularioProcedimento = new FormData();
        formularioProcedimento.append('procedimento', this.formularioProcedimento.procedimentoPk);
        formularioProcedimento.append('quantidade', this.formularioProcedimento.quantidade);
        formularioProcedimento.append('classificacao', this.formularioProcedimento.classificacao);
        formularioProcedimento.append('tipo_solicitacao', this.formularioProcedimento.tipoSolicitacao);
        formularioProcedimento.append('realizado_por', this.formularioProcedimento.realizadoPor);
       
        axios.put(url.replace('00000000-0000-0000-0000-000000000000', procedimento.id), formularioProcedimento, {
            headers: { 'Content-Type': 'multipart/form-data'},
        }).then((response) => {
            const foundProcedimento = this.listagemProcedimentos.find(param => param.id === response.data.id);
            
            if (foundProcedimento) {
                foundProcedimento.procedimentoPk = response.data.procedimento.id;
                foundProcedimento.procedimento_nome = response.data.procedimento_nome;
                foundProcedimento.procedimento_codigo = response.data.procedimento_codigo;
                foundProcedimento.quantidade = response.data.quantidade;
                foundProcedimento.classificacao = response.data.classificacao;
                foundProcedimento.tipo_solicitacao = response.data.tipo_solicitacao;
                foundProcedimento.realizado_por = response.data.realizado_por;
                foundProcedimento.realizado_por_nome = response.data.realizado_por_nome;
            }
            
            this.formularioProcedimento.id = '';
            this.formularioProcedimento.classificacao = 1;
            this.formularioProcedimento.quantidade = 1;
            this.formularioProcedimento.tipoSolicitacao = 0;
            this.formularioProcedimento.realizadoPor = 0;
            this.$nextTick(() => {this.$refs.customProcediemento.selectOption(null)});

            this.SweetAlert("PROCEDIMENTO ATUALIZADO COM SUCESSO!", "success")
        });
    }else if(metodo === 'DELETE'){
        axios.delete(url.replace('00000000-0000-0000-0000-000000000000', procedimento.id))
        .then((response)=>{
            this.listagemProcedimentos.splice(this.listagemProcedimentos.indexOf(procedimento), 1)
            this.formularioProcedimento.id = '';
            this.formularioProcedimento.classificacao = 0;
            this.formularioProcedimento.quantidade = '';
            this.formularioProcedimento.editar = false;
            this.$nextTick(() => {this.$refs.customProcediemento.selectOption(null)});
            this.SweetAlert("PROCEDIMENTO DELETADO COM SUCESSO!", "warning")
        });
    }
},
crudJustificativaProcedimentoAtendimento(metodo, procedimento=null){
    let url  = "{% url 'saude_atendimento:atendimentos-get-justificativa-procedimento-atendimento' pk='00000000-0000-0000-0000-000000000000' %}"
    axios.get(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK))
    .then((response)=>{
        this.listagemJustificativaProcedimentos = response.data
    });
},
postDocumentoPaciente(descricaoAnexo=null, selectedFile=null, nomeArquivo=null){
    const formularioDocumentos = new FormData();
    formularioDocumentos.append('nome', nomeArquivo);
    formularioDocumentos.append('arquivo', selectedFile);
    formularioDocumentos.append('descricao', descricaoAnexo);

    let url  = "{% url 'saude_atendimento:atendimentos-documentacao-paciente' pk='00000000-0000-0000-0000-000000000000' %}"
    axios.post(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK), formularioDocumentos, {
        headers: { 'Content-Type': 'multipart/form-data'},
    }).then((response) => {
        this.atendimentoMedico.documentos = response.data
        this.SweetAlert("DOCUMENTO SALVO COM SUCESSO!", "success")
    });  
},
verificarCriarMedicacao(metodo, medicacao=null){
    if(this.formularioMedicacao.aplicacao === '1' || this.formularioMedicacao.aplicacao === 1){
        if(metodo === 'POST'){
            this.crudMedicacaoAtendimento('POST')
        }
        if(metodo === 'PUT'){
            this.crudMedicacaoAtendimento('PUT', medicacao)
        }
    }else{
        if(this.formularioMedicacao.quantidade > 0){
            if(metodo === 'POST'){
                this.crudMedicacaoAtendimento('POST')
            }
            if(metodo === 'PUT'){
                this.crudMedicacaoAtendimento('PUT', medicacao)
            }
        }else{
            if(metodo === 'POST'){
                this.crudMedicacaoAtendimento('POST')
            }
            if(metodo === 'PUT'){
                this.crudMedicacaoAtendimento('PUT', medicacao)
            }
            // Swal.fire({
            //     icon: "warning",
            //     title: 'ATENÇÃO!',
            //     text: "NÃO EXISTE A MEDICAÇÃO SELECIONADA EM ESTOQUE. DESEJA CONTINUAR?",
            //     showCancelButton: true,
            //     confirmButtonColor: "#3085d6",
            //     cancelButtonColor: "#d33",
            //     cancelButtonText: "<i class='fa-solid fa-xmark mr-2'></i> Cancelar",
            //     confirmButtonText: "<i class='fa-solid fa-circle-check mr-2'></i> Confirmar",
            //     reverseButtons: true,
            //     customClass: {popup: 'custom-popup-view-info-medicacao',},
            // }).then((result) => {
            //     if (result.isConfirmed) {
            //         this.formularioMedicacao.estoque_zero = true;
            //         if(metodo === 'POST'){
            //             this.crudMedicacaoAtendimento('POST')
            //         }
            //         if(metodo === 'PUT'){
            //             this.crudMedicacaoAtendimento('PUT', medicacao)
            //         }
            //     }
            // });
        }
    }
},
crudMedicacaoAtendimento(metodo, medicacao=null){
    let url  = "{% url 'saude_atendimento:atendimentos-medicacao-atendimento' pk='00000000-0000-0000-0000-000000000000' %}"
    if(metodo === 'GET'){
        axios.get(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK))
        .then((response)=>{
            this.listagemMedicacoesAtendimentos = response.data
        });
    }else if(metodo === 'POST'){
        this.formularioMedicacao.carregando = true

        const formMedicacao = new FormData();
        formMedicacao.append('via', this.formularioMedicacao.via);
        formMedicacao.append('parental', this.formularioMedicacao.parental);
        formMedicacao.append('medicacao', this.formularioMedicacao.medicacaoPk);
        formMedicacao.append('dosagem', this.formularioMedicacao.dosagem);
        formMedicacao.append('posologia', this.formularioMedicacao.posologia);
        formMedicacao.append('tipo_posologia', this.formularioMedicacao.tipoPosologia);
        formMedicacao.append('duracao_tratamento', this.formularioMedicacao.duracaoTratamento);
        formMedicacao.append('uso_continuo', this.formularioMedicacao.usoContinuo);
        formMedicacao.append('observacao', this.formularioMedicacao.observacao);
        formMedicacao.append('aplicacao', this.formularioMedicacao.aplicacao);
        formMedicacao.append('dose_unica', this.formularioMedicacao.doseUnica);
        formMedicacao.append('medicamento_controlado', this.formularioMedicacao.medicamentoControlado);
        formMedicacao.append('estoque_zero', this.formularioMedicacao.estoque_zero);

        axios.post(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK), formMedicacao, {
            headers: { 'Content-Type': 'multipart/form-data'},
        }).then((response) => {
            this.listagemMedicacoesAtendimentos = response.data
            
            $(".via-admin").val('').trigger('change');
            $(".parental").val('').trigger('change');
            $(".posologia").val('').trigger('change');
            this.formularioMedicacao.via = ''
            this.formularioMedicacao.parental = ''
            this.formularioMedicacao.medicacaoPk = null
            this.formularioMedicacao.dosagem = ''
            this.formularioMedicacao.posologia = ''
            this.formularioMedicacao.duracaoTratamento = 1
            this.formularioMedicacao.observacao = ''
            this.formularioMedicacao.usoContinuo = ''
            this.formularioMedicacao.aplicacao = '0'
            this.formularioMedicacao.estoque_zero = false
            this.$nextTick(() => {this.$refs.customMedicacaoAtendimento.selectOption(null)});
            this.SweetAlert("MEDICAÇÃO SALVA COM SUCESSO!", "success")

            this.formularioMedicacao.carregando = false
        }); 
    }else if(metodo === 'PUT'){
        this.formularioMedicacao.carregando = true

        const formMedicacao = new FormData();
        formMedicacao.append('via', this.formularioMedicacao.via);
        formMedicacao.append('parental', this.formularioMedicacao.parental);
        formMedicacao.append('medicacao', this.formularioMedicacao.medicacaoPk);
        formMedicacao.append('dosagem', this.formularioMedicacao.dosagem);
        formMedicacao.append('posologia', this.formularioMedicacao.posologia);
        formMedicacao.append('tipo_posologia', this.formularioMedicacao.tipoPosologia);
        formMedicacao.append('duracao_tratamento', this.formularioMedicacao.duracaoTratamento);
        formMedicacao.append('uso_continuo', this.formularioMedicacao.usoContinuo);
        formMedicacao.append('observacao', this.formularioMedicacao.observacao);
        formMedicacao.append('aplicacao', this.formularioMedicacao.aplicacao);
        formMedicacao.append('dose_unica', this.formularioMedicacao.doseUnica);
        formMedicacao.append('medicamento_controlado', this.formularioMedicacao.medicamentoControlado);
        formMedicacao.append('estoque_zero', this.formularioMedicacao.estoque_zero);

        axios.put(url.replace('00000000-0000-0000-0000-000000000000', medicacao.id), formMedicacao, {
            headers: { 'Content-Type': 'multipart/form-data'},
        }).then((response) => {
            this.listagemMedicacoesAtendimentos = response.data

            this.EditarCancelarMedicacao('cancelar')
            this.SweetAlert("MEDICAÇÃO ATUALIZADA COM SUCESSO!", "success")

            this.formularioMedicacao.carregando = false
        });
    }else if(metodo === 'DELETE'){
        axios.delete(url.replace('00000000-0000-0000-0000-000000000000', medicacao.id))
        .then((response)=>{
            this.listagemMedicacoesAtendimentos.splice(this.listagemMedicacoesAtendimentos.indexOf(medicacao), 1)
            this.EditarCancelarMedicacao('cancelar')
            this.SweetAlert("MEDICAÇÃO DELETADA COM SUCESSO!", "warning")
        });
    }
},
criarSolicitacoes(){
    let url  = "{% url 'saude_atendimento:atendimentos-criar-ordenacao-atendimento' pk='00000000-0000-0000-0000-000000000000' %}"
    axios.post(url.replace('00000000-0000-0000-0000-000000000000', this.paciente.atendimentoPK), { ordenacoes: this.listItems })
    .then((response) => {
        this.abrirModal('modalDrag', 'fechar')
        this.atendimentoMedico.existe_solicitacoes_abertas = true
        this.paciente.situacao = response.data.situacao
        Swal.fire({
            text: "SOLICITAÇÕES EFETUADAS COM SUCESSO!",
            icon: "success",
            showCancelButton: false,
            showCloseButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Fechar",
            allowOutsideClick: false,
            customClass: {popup: 'custom-popup-view-confirmacao-solicitacoes'},
            preConfirm: () => {
                window.location.href = "{% url 'saude_atendimento:atendimento_medico_list' %}"
            },
            willClose: () => {
                window.location.href = "{% url 'saude_atendimento:atendimento_medico_list' %}"
            }
        });
    });  
},
confirmarReaberturaAtendimento(pk){
    Swal.fire({
        html: `
            <h2 class="swal2-title" id="swal2-title" style="display: block; font-size: 20px; color: var(--interactive);">Atenção!</h2>
            <div class="swal2-html-container mt-2" id="swal2-html-container" style="display: block; font-size: 18px; color: var(--interactive); margin-top: 7px;">Deseja Realmente Reabrir o Atendimento? </div>
            <div><textarea id="swal2-textarea" class="swal2-textarea" placeholder="Por favor, adicione a justivicativa para reabertura." style="width: 80%; font-size: 16px !important;"></textarea></div>
        `,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        confirmButtonText: '<i class="fa-solid fa-check mr-2"></i> CONFIRMAR',
        cancelButtonText: '<i class="fa-solid fa-xmark"></i> CANCELAR',
        reverseButtons: true,
        customClass: {popup: 'custom-popup-view-reabertura',},
        preConfirm: () => {
            const selectElement = document.getElementById('swal2-textarea');
            const observacao = selectElement.value;

            if(observacao === '') {
                Swal.showValidationMessage('Adicione uma justificativa.');
            }else{
                let url  = "{% url 'saude_atendimento:atendimentos-reabertura-atendimento-medico' pk='00000000-0000-0000-0000-000000000000' %}"
                axios.put(url.replace('00000000-0000-0000-0000-000000000000', pk), {justificativa: observacao })
                .then((response)=>{  
                    this.paciente.situacao_numero = response.data.status_lista_chamada_numero;
                    this.paciente.situacao = response.data.status_lista_chamada;
                    
                    this.SweetAlert("REABERTURA SALVA COM SUCESSO!", "success");
                });
            }
        },
    });
},
suspenderConfirmarProcedimento(tipo, procedimento, justificativa=null){
    const forProcedimento = new FormData();
    forProcedimento.append('tipo', tipo);
    forProcedimento.append('justificativa', justificativa);

    let url  = "{% url 'saude_atendimento:atendimentos-suspender-confirmar-procedimento' pk='00000000-0000-0000-0000-000000000000' %}"
    axios.put(url.replace('00000000-0000-0000-0000-000000000000', procedimento.id), forProcedimento, {
        headers: { 'Content-Type': 'multipart/form-data'},
    }).then((response)=>{  
        const foundProcedimento = this.listagemProcedimentos.find(param => param.id === response.data.id);

        if (foundProcedimento) {
            foundProcedimento.situacao = response.data.situacao;
        }
        this.SweetAlert("PROCEDIMENTO SUSPENSO COM SUCESSO!", "success");
    });
}