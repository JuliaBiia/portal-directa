const calendarEl = document.getElementById('calendar');

const businessHours = JSON.parse(document.getElementById('business-hours-data').textContent);


let agendamentoID = "";


window.onload = function () {
    const calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },


        initialView: "timeGridWeek",


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
        businessHours: businessHours,
        dayMaxEvents: true, // allow "more" link when too many events
        events: JSON.parse(document.getElementById('agendamentos-data').textContent),

        datesSet: function (dateInfo) {
            view = dateInfo.view;

            const medicoSemHorarioCadastrado = businessHours.length === 0;

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
    });
    
    calendar.render();
}