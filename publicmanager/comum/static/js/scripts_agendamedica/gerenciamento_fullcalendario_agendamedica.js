const calendarEl = document.getElementById('calendar');

const businessHours = JSON.parse(document.getElementById('business-hours-data').textContent);
const businessHoursEstruturaFullCalendar = JSON.parse(document.getElementById('business-hours-estrutura-fullcalendar-data').textContent);


const verificarSeAMarcacaoEhParaUmaBusinessHour = (dataCelulaInicioAtendimento, viewCelulaInicioAtendimento) => {

    const horariosDoMedicoParaODiaDaSemanaSelecionado = businessHours[dataCelulaInicioAtendimento.getDay()];

    if(horariosDoMedicoParaODiaDaSemanaSelecionado){
        if (viewCelulaInicioAtendimento.type === "dayGridMonth"){
            return true;
        }

        for(horarioDoMedico of horariosDoMedicoParaODiaDaSemanaSelecionado){
            let [ horarioInicial, horarioFinal ] = horarioDoMedico;

            const [ horarioInicialHora, horarioInicialMinuto ] = horarioInicial.split(":");
            horarioInicial = new Date(dataCelulaInicioAtendimento);
            horarioInicial.setHours(horarioInicialHora);
            horarioInicial.setMinutes(horarioInicialMinuto);

            const [ horarioFinalHora, horarioFinalMinuto ] = horarioFinal.split(":");
            horarioFinal = new Date(dataCelulaInicioAtendimento);
            horarioFinal.setHours(horarioFinalHora);
            horarioFinal.setMinutes(horarioFinalMinuto);

            if(horarioInicial <= dataCelulaInicioAtendimento && horarioFinal >= dataCelulaInicioAtendimento){
                return true;
            }
        }

        return false;
    }

    return false;
}


const verificarSeDataEhFeriado = data => {
    const dataHora = data.getHours();
    const dataMinuto = data.getMinutes();


    const feriados = JSON.parse(document.getElementById('matriz-feriados-data').textContent);

    for(index in feriados){
        const feriado = {};

        feriado.data_inicial = feriados[index][0];
        feriado.data_inicial = new Date(feriado.data_inicial[0], feriado.data_inicial[1]-1, feriado.data_inicial[2]).setHours(0,0,0,0); // ano, mês, dia

        feriado.data_final = feriados[index][1];
        feriado.data_final = new Date(feriado.data_final[0], feriado.data_final[1]-1, feriado.data_final[2]).setHours(0,0,0,0);

        if(feriado.data_inicial <= data.setHours(0, 0, 0, 0) && feriado.data_final >= data.setHours(0, 0, 0, 0)){
            data.setHours(dataHora, dataMinuto, 0);

            return true;
        }
    }

    data.setHours(dataHora, dataMinuto, 0);

    return false;
}

const verificarSeDataEstarBloqueadaParaOMedicoSelecionado = data => {
    const dataHora = data.getHours();
    const dataMinuto = data.getMinutes();

    const bloqueiosAgenda = JSON.parse(document.getElementById('matriz-bloqueios-agenda-data').textContent);

    for(index in bloqueiosAgenda){
        const bloqueioAgenda = {};

        bloqueioAgenda.data_inicial = bloqueiosAgenda[index][0];
        bloqueioAgenda.data_inicial = new Date(bloqueioAgenda.data_inicial[0], bloqueioAgenda.data_inicial[1]-1, bloqueioAgenda.data_inicial[2]);

        bloqueioAgenda.data_final = bloqueiosAgenda[index][1];
        bloqueioAgenda.data_final = new Date(bloqueioAgenda.data_final[0], bloqueioAgenda.data_final[1]-1, bloqueioAgenda.data_final[2]);

        if(bloqueioAgenda.data_inicial <= data.setHours(0, 0, 0, 0) && bloqueioAgenda.data_final >= data.setHours(0, 0, 0, 0)){
            data.setHours(dataHora, dataMinuto, 0);

            return true;
        }
    }

    data.setHours(dataHora, dataMinuto, 0)

    return false;
}

const retornarHoraMinutoComDoisDigitos = horaMinuto => {
    return horaMinuto < 10 ? `0${horaMinuto}` : horaMinuto
}


const confirmarDragging = (mensagemConfirmacao, callbackNegacao) => {
    const elementoModal = document.getElementById('modal-confirmacao-dragging');

    const elementoMensagemConfirmacao = document.querySelector("#modal-confirmacao-dragging > .br-modal > .br-modal-body > p");

    const botaoConfirmarOperacao = document.querySelector("#modal-confirmacao-dragging > .br-modal > .br-modal-body #confirmacao-dragging");
    const botaoNegarOperacao = document.querySelector("#modal-confirmacao-dragging > .br-modal > .br-modal-body #negacao-dragging");



    elementoMensagemConfirmacao.innerHTML = mensagemConfirmacao;

    botaoConfirmarOperacao.addEventListener('click', () => {

        botaoConfirmarOperacao.removeEventListener('click', () => {
            
        })
        
        elementoModal.style.display = "none";
    })
    botaoNegarOperacao.addEventListener('click', () => {

        botaoNegarOperacao.removeEventListener('click', () => {
            
        })

        callbackNegacao();

        elementoModal.style.display = "none";
    })

    elementoModal.style.display = "block";
}


window.onload = function () {
    const calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },


        initialView: umMedicoFoiSelecionado ? "timeGridWeek" : "dayGridMonth",


        locale: "pt-br",
        weekNumberCalculation: 'ISO',
        buttonText: {
            today: 'Hoje',
            month: 'Mês',
            week: 'Semana',
            day: 'Dia',
        },

        views: {
            timeGridWeek: {
                allDaySlot: false,
                slotDuration: '00:20:00',
                slotLabelFormat: {
                    hour: '2-digit',
                    minute: '2-digit'
                },
                slotLabelInterval: "00:20",
                slotMinTime: "08:00:00",
                slotMaxTime: "18:00:00",
            },
            timeGridDay: {
                allDaySlot: false,
                slotDuration: '00:20:00',
                slotLabelFormat: {
                    hour: '2-digit',
                    minute: '2-digit'
                },
                slotLabelInterval: "00:20",
                slotMinTime: "08:00:00",
                slotMaxTime: "18:00:00",
            },
        },
        businessHours: businessHoursEstruturaFullCalendar,
        dayMaxEvents: true, // allow "more" link when too many events
        events: JSON.parse(document.getElementById('agendamentos-data').textContent),
        eventStartEditable: true,

        datesSet: function (dateInfo) {
            view = dateInfo.view;

            const medicoSemHorarioCadastrado = businessHoursEstruturaFullCalendar.length === 0;

            if(view.type === 'dayGridMonth' && medicoSemHorarioCadastrado){
                Array.from(document.querySelectorAll('.fc-daygrid-day-bg')).map(elemento => {
                    const div1 = document.createElement('div')
                    div1.className = 'fc-daygrid-bg-harness';
                    div1.style.left = '0px';
                    div1.style.right = '0px';

                    const div2 = document.createElement('div')
                    div2.className = 'fc-non-business';

                    div1.appendChild(div2);
                    elemento.appendChild(div1);
                })
            } else if(view.type === 'timeGridWeek' && medicoSemHorarioCadastrado){
                Array.from(document.querySelectorAll('.fc-timegrid-col-bg')).map(elemento => {
                    const div1 = document.createElement('div')
                    div1.className = 'fc-timegrid-bg-harness';
                    div1.style.top = '0px';
                    div1.style.bottom = '-648px';

                    const div2 = document.createElement('div')
                    div2.className = 'fc-non-business';

                    div1.appendChild(div2);
                    elemento.appendChild(div1);
                })
            }
        },

        dateClick: async function (info) {
            dataCelulaInicioAtendimento = info.date;

            if( umMedicoFoiSelecionado && verificarSeAMarcacaoEhParaUmaBusinessHour(dataCelulaInicioAtendimento, info.view)){
                const aDataDaCelulaEhAnteriorADataAtual = verificarSeADataDaCelulaEhAnteriorADataAtualSemConsiderarHora(new Date(), dataCelulaInicioAtendimento);

                const dataCelulaInicioAtendimentoEhFeriado = verificarSeDataEhFeriado(dataCelulaInicioAtendimento);

                const dataCelulaInicioAtendimentoEstarBloqueadaParaOMedicoSelecionado = verificarSeDataEstarBloqueadaParaOMedicoSelecionado(dataCelulaInicioAtendimento);

                if (aDataDaCelulaEhAnteriorADataAtual) {
                    mostrarNotificaoImpossibilidade("Não é permitido agendar atendimentos para uma data anterior a data atual.")
                }
                else if (dataCelulaInicioAtendimentoEstarBloqueadaParaOMedicoSelecionado){
                    mostrarNotificaoImpossibilidade("Agenda bloqueada pelo médico! Não é possível agendar atendimentos para este dia.")
                }
                else if (dataCelulaInicioAtendimentoEhFeriado) {
                    mostrarNotificaoImpossibilidade("Feriado! Não é possível agendar atendimentos para este dia.")
                }
                else {
                    despreencherModalAgendarAtendimento();


                    // Código que ajusta o select de médico
                    const selectSelecaoMedico = document.querySelector('.select-medico #id_medico_filtragem_agendamentos');
                    const selectMedico = document.querySelector('#agendamento_form #id_medico');


                    mudarOptionSelected(
                        selectMedico,
                        retornarOptionSelected(selectSelecaoMedico).value
                    )


                    // Código que ajusta o campo de data
                    const dia = String(dataCelulaInicioAtendimento.getDate()).padStart(2, '0');
                    const mes = String(dataCelulaInicioAtendimento.getMonth() + 1).padStart(2, '0');
                    const ano = dataCelulaInicioAtendimento.getFullYear();
                    const data = new Date(ano, mes - 1, dia);


                    document.getElementById("id_data_atendimento").value = `${dia}/${mes}/${ano}`;


                    // Código que ajusta os select relacionados ao horário de início e término de consulta
                    ehHorarioComercial = dataCelulaInicioAtendimento.getHours() > 0

                    if (!ehHorarioComercial) {
                        dataCelulaInicioAtendimento.setHours(8)
                        dataCelulaInicioAtendimento.setMinutes(0)
                    }

                    const selectsHorarioInicioAtendimento = [selectHoraInicioAtendimento, selectMinutoInicioAtendimento];
                    preencherSelectsDoHorarioInicioAtendimento(dataCelulaInicioAtendimento, selectsHorarioInicioAtendimento);

                    dataCelulaTerminoAtendimento = retornarDataCelulaTerminoAtendimento(dataCelulaInicioAtendimento);

                    const selectsHorarioTerminoAtendimento = [selectHoraTerminoAtendimento, selectMinutoTerminoAtendimento];
                    preencherSelectsDoHorarioTerminoAtendimento(dataCelulaTerminoAtendimento, selectsHorarioTerminoAtendimento);

                    ajustarSelectModal();
                    ajustarSelectMedicoModalAgendamentoConsultorio();

                    habilitarOsCamposModalAgendarAtendimento();

                    document.querySelector(".campo-paciente").style.display = 'flex';

                    const quantidadeAtendimentosPorTipo = await getQuantidadeAgendamentosConsultorioPorTipo(selectMedico.value, [dia, mes, ano]);
                    
                    document.querySelector("#container-primeiro-atendimento > #valor-primeiro-atendimento").innerHTML = quantidadeAtendimentosPorTipo[0];
                    document.querySelector("#container-retorno > #valor-retorno").innerHTML = quantidadeAtendimentosPorTipo[1];
                    document.querySelector("#container-extra-encaixe > #valor-extra-encaixe").innerHTML = quantidadeAtendimentosPorTipo[2];

                    botaoAgendarAtendimento.style.display = 'block';
                    botaoEditarAgendamento.style.display = 'none';
                    cancelarAgendamentoAtendimento.style.display = 'flex';
                    removerAgendamento.style.display = 'none';
                    modalDeAgendamentoAtendimento.style.display = 'block';
                    preAtendimento.style.display = 'none';
                }
            }
        },
        
        eventClick: async function (info) {
            // botaoAgendarAtendimento.style.display = 'none';
            // botaoEditarAgendamento.style.display = 'block';
            // cancelarAgendamentoAtendimento.style.display = 'none';
            // removerAgendamento.style.display = 'flex';

            agendamentoID = info.event.id; // Esta linha não pode ser removida.

            renderizarModalEdicaoAgendamentoAtendimento(info.event.id);

        },

        eventDrop: async function (info){
            let dadosAtuaisAgendamento = {}

            try{
                dadosAtuaisAgendamento = await getAgendamentoConsultorio(info.event.id);
            } catch (error){
                info.revert();

                if(Object.keys(error).find(element => element === "status-code")){
                    if(error["status-code"] === 400 || error["status-code"] === 404){
                        mostrarNotificaoErro(error['status-message']);
                    } else{
                        mostrarNotificaoErro(error);
                    }
                } else{
                    mostrarNotificaoErro(error);
                }

                return "";
            }

            let dataAtendimento = dadosAtuaisAgendamento.data_atendimento.split('-');
            dataAtendimento = new Date(dataAtendimento[0], dataAtendimento[1]-1, dataAtendimento[2]);

            const aDataDaCelulaEhAnteriorADataAtual = verificarSeADataDaCelulaEhAnteriorADataAtualSemConsiderarHora(new Date(), dataAtendimento);
            const aDataDaCelulaDestinoEhAnteriorADataAtual = verificarSeADataDaCelulaEhAnteriorADataAtualSemConsiderarHora(new Date(), info.event.end);

            if(aDataDaCelulaEhAnteriorADataAtual || aDataDaCelulaDestinoEhAnteriorADataAtual){
                info.revert();
                mostrarNotificaoErro("Não é permitido remarcar agendamentos anteriores ao dia atual! Por favor  marque um novo agendamento.");
            } else{
                const dia = String(info.event.start.getDate()).padStart(2, '0');
                const mes = String(info.event.start.getMonth() + 1).padStart(2, '0');
                const ano = info.event.start.getFullYear();
                const nova_data_atendimento = `${ano}-${mes}-${dia}`;

                const nova_hora_hora_inicio_atendimento = String(info.event.start.getHours()).padStart(2, '0');
                const novo_minuto_hora_inicio_atendimento = String(info.event.start.getMinutes()).padStart(2, '0');
                const horario_hora_inicio_atendimento = `${nova_hora_hora_inicio_atendimento}:${novo_minuto_hora_inicio_atendimento}`;

                const nova_hora_hora_termino_atendimento = String(info.event.end.getHours()).padStart(2, '0');
                const novo_minuto_hora_termino_atendimento = String(info.event.end.getMinutes()).padStart(2, '0');
                const horario_hora_termino_atendimento = `${nova_hora_hora_termino_atendimento}:${novo_minuto_hora_termino_atendimento}`

                let novosDadosAgendamento = {
                    nome_paciente: dadosAtuaisAgendamento.nome_paciente,
                    celular_paciente: dadosAtuaisAgendamento.celular_paciente,
                    telefone_fixo_paciente: dadosAtuaisAgendamento.telefone_fixo_paciente,
                    medico: dadosAtuaisAgendamento.medico_detalhes.id,
                    tipo_atendimento: dadosAtuaisAgendamento.tipo_atendimento,
                    data_atendimento: nova_data_atendimento,
                    hora_inicio_atendimento: horario_hora_inicio_atendimento,
                    hora_termino_atendimento: horario_hora_termino_atendimento,
                    observacoes: dadosAtuaisAgendamento.observacoes,
                }

                try{
                    let _ = await editAgendamentoConsultorioComFetch(novosDadosAgendamento, info.event.id);
                } catch (error){
                    info.revert();
    
                    if(Object.keys(error).find(element => element === "status-code")){
                        if(error["status-code"] === 400 || error["status-code"] === 404){
                            mostrarNotificaoErro(error['status-message']);
                        } else{
                            mostrarNotificaoErro(error);
                        }
                    } else{
                        mostrarNotificaoErro(error);
                    }
    
                    return "";
                }

                const mensagemConfirmacao = `Deseja realmente remarcar o agendamento para às ${horario_hora_inicio_atendimento} do dia ${dia}/${mes}/${ano}?`;
                const callbackNegacao = async () => {
                    info.revert();

                    const dadosAnterioresAgendamento = {
                        nome_paciente: dadosAtuaisAgendamento.nome_paciente,
                        celular_paciente: dadosAtuaisAgendamento.celular_paciente,
                        telefone_fixo_paciente: dadosAtuaisAgendamento.telefone_fixo_paciente,
                        medico: dadosAtuaisAgendamento.medico_detalhes.id,
                        tipo_atendimento: dadosAtuaisAgendamento.tipo_atendimento,
                        data_atendimento: dadosAtuaisAgendamento.data_atendimento,
                        hora_inicio_atendimento: dadosAtuaisAgendamento.hora_inicio_atendimento,
                        hora_termino_atendimento: dadosAtuaisAgendamento.hora_termino_atendimento,
                        observacoes: dadosAtuaisAgendamento.observacoes,
                    }
                    
                    let _ = await editAgendamentoConsultorioComFetch(dadosAnterioresAgendamento, info.event.id);
                }

                confirmarDragging(mensagemConfirmacao, callbackNegacao);
            }
        }
    });
    
    calendar.render();

    const precisaDeixarAbertoOModalDeCadastrarFeriado = Number(sessionStorage.getItem("precisaDeixarAbertoOModalDeCadastrarFeriado"));
    const precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda = Number(sessionStorage.getItem("precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda"));

    if(precisaDeixarAbertoOModalDeCadastrarFeriado){
        modalFeriado.style.display = "block";
        sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarFeriado", 0);
    } else if(precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda){
        modalBloqueioAgenda.style.display = "block";
        sessionStorage.setItem("precisaDeixarAbertoOModalDeCadastrarBloqueioAgenda", 0);
        preencherSelectMedicoDoModalCadastrarBloqueioAgenda();
    }
}