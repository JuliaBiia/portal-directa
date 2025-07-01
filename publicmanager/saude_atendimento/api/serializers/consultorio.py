from datetime import date
from rest_framework import serializers
from publicmanager.saude_atendimento.models import (
    BloqueioAgenda, Feriado, HorarioMedico, AgendamentoConsultorio, Profissional
)

class AgendamentoConsultorioSerializer(serializers.ModelSerializer):
    medico_detalhes = serializers.SerializerMethodField()
    agendado_por_detalhes = serializers.SerializerMethodField()

    class Meta:
        model = AgendamentoConsultorio
        fields = ['id','nome_paciente', 'cpf_paciente',
                  'celular_paciente','telefone_fixo_paciente',
                  'medico_detalhes', 'agendado_por_detalhes',
                  'tipo_atendimento', 'data_atendimento',
                  'hora_inicio_atendimento', 'hora_termino_atendimento', 'observacoes'
                  ]

    def get_medico_detalhes(self, obj):
        return {
            "id": obj.medico.id,
            "nome": obj.medico.nome_profissional
        }
    def get_agendado_por_detalhes(self, obj):
        return {
            "id": obj.agendado_por.id,
            "nome": obj.agendado_por.nome
        }

    def validate(self, data):
        medico = self.instance.medico

        if data["data_atendimento"] < date.today():
            raise serializers.ValidationError("Não é permitido agendar atendimentos para uma data anterior a data atual.")
        elif data["hora_inicio_atendimento"] > data["hora_termino_atendimento"]:
            raise serializers.ValidationError("A hora do inicio do atendimento deve ser anterior a hora de término.")

        agendamentos = AgendamentoConsultorio.objects.filter(
            medico__id__exact=medico.id,
            data_atendimento=data["data_atendimento"],
            hora_inicio_atendimento=data["hora_inicio_atendimento"],
            hora_termino_atendimento=data["hora_termino_atendimento"]
        ).exclude(id__exact=self.instance.id)

        existe_atendimento_agendado_para_a_mesma_hora_passada_no_form = len(agendamentos) > 0


        if existe_atendimento_agendado_para_a_mesma_hora_passada_no_form:
            raise serializers.ValidationError("Já existe um paciente marcado para este horário. Por favor, escolha um horário diferente.")
        else:
            # Os médicos possuem horários cadastrados para eles. Uma edição da data e/ou da hora de início das consultas não pode ser aceita se ela estiver em desacordo com os horários cadastrados para o respectivo médico. As validações abaixo servem para garantir isto.

            horarios_medico = HorarioMedico.objects.filter(medico_horariomedico__id__exact=medico.id)

            medico_nao_tem_horarios_cadastrados = len(horarios_medico) == 0

            if medico_nao_tem_horarios_cadastrados:
                raise serializers.ValidationError("Um médico só pode atender um paciente se tiver horários cadastrados no sistema.")
            else:
                

                dia_da_semana_data_atendimento_num = data["data_atendimento"].isocalendar()[2]

                if dia_da_semana_data_atendimento_num == 7:
                    dia_da_semana_data_atendimento_num = 0

                horarios_medico = horarios_medico.filter(
                    dia_semana_horariomedico__exact=dia_da_semana_data_atendimento_num
                )

                medico_nao_atende_no_dia_do_atendimento = len(horarios_medico) == 0

                if medico_nao_atende_no_dia_do_atendimento:
                    raise serializers.ValidationError("Não é possível agendar este atendimento para a data selecionada. Por favor verifique a disponibilidade do medico!")
                else:
                    horarios_medico = horarios_medico.filter(
                        hora_inicial_horariomedico__lte=data["hora_inicio_atendimento"],
                        hora_final_horariomedico__gt=data["hora_inicio_atendimento"]
                    )

                    medico_nao_atende_no_horario_do_atendimento = len(horarios_medico) == 0

                    if medico_nao_atende_no_horario_do_atendimento:
                        raise serializers.ValidationError("Não é possível agendar este atendimento para o horário selecionado. Por favor verifique a disponibilidade do medico!")
                    else:
                        horarios_medico = horarios_medico.filter(
                            hora_final_horariomedico__gte=data["hora_termino_atendimento"]
                        )

                        medico_nao_atende_no_horario_do_atendimento = len(horarios_medico) == 0

                        if medico_nao_atende_no_horario_do_atendimento:
                            raise serializers.ValidationError("Não é possível agendar este atendimento para o horário selecionado. Por favor verifique a disponibilidade do medico!")

        
        # Não deve ser possível mudar a data de um atendimento para um período no qual a agenda do médico está fechada. As validações abaixo servem para garantir isto.
        bloqueios_agenda = BloqueioAgenda.objects.filter(
            medico__id__exact=medico.id,
            data_inicial__lte=data["data_atendimento"],
            data_final__gte=data["data_atendimento"]
        )

        data_atendimento_cai_em_bloqueio_agenda = len(bloqueios_agenda) > 0

        if data_atendimento_cai_em_bloqueio_agenda:
            raise serializers.ValidationError("Agenda bloqueada pelo médico! Não é possível agendar atendimentos para este dia.")
        
        # Não deve ser possível mudar a data de um atendimento para um período cadastrado como feriado. As validações abaixo servem para garantir isto.
        feriados = Feriado.objects.filter(
            data_inicial__lte=data["data_atendimento"],
            data_final__gte=data["data_atendimento"]
        )

        data_atendimento_cai_em_feriado = len(feriados) > 0

        if data_atendimento_cai_em_feriado:
            raise serializers.ValidationError("Feriado! Não é possível agendar atendimentos para este dia.")

        return data

class AgendamentoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgendamentoConsultorio
        fields = ['paciente', 'nome_paciente', 'cpf_paciente',
                  'celular_paciente', 'telefone_fixo_paciente',
                  'medico', 'agendado_por', 'tipo_atendimento',
                  'data_atendimento', 'hora_inicio_atendimento',
                  'hora_termino_atendimento', 'observacoes']

    def validate(self, data):
        medico = Profissional.objects.get(id=data["medico"].id)

        if data["data_atendimento"] < date.today():
            raise serializers.ValidationError("Não é permitido agendar atendimentos para uma data anterior a data atual.")
        elif data["hora_inicio_atendimento"] > data["hora_termino_atendimento"]:
            raise serializers.ValidationError("A hora do inicio do atendimento deve ser anterior a hora de término.")

        agendamentos = AgendamentoConsultorio.objects.filter(
            medico__id__exact=medico.id,
            data_atendimento=data["data_atendimento"],
            hora_inicio_atendimento=data["hora_inicio_atendimento"],
            hora_termino_atendimento=data["hora_termino_atendimento"]
        )

        existe_atendimento_agendado_para_a_mesma_hora_passada_no_form = len(agendamentos) > 0


        if existe_atendimento_agendado_para_a_mesma_hora_passada_no_form:
            raise serializers.ValidationError("Já existe um atendimento agendado para este horário. Por favor, escolha um horário diferente.")
        else:
            # Os médicos possuem horários cadastrados para eles. Uma edição da data e/ou da hora de início dos atendimentos não pode ser aceita se ela estiver em desacordo com os horários cadastrados para o respectivo médico. As validações abaixo servem para garantir isto.

            horarios_medico = HorarioMedico.objects.filter(medico_horariomedico__id__exact=medico.id)

            medico_nao_tem_horarios_cadastrados = len(horarios_medico) == 0

            if medico_nao_tem_horarios_cadastrados:
                raise serializers.ValidationError("Um médico só pode atender um paciente se tiver horários cadastrados no sistema.")
            else:
                dia_da_semana_data_atendimento_num = data["data_atendimento"].isocalendar()[2]

                if dia_da_semana_data_atendimento_num == 7:
                    dia_da_semana_data_atendimento_num = 0

                horarios_medico = horarios_medico.filter(
                    dia_semana_horariomedico__exact=dia_da_semana_data_atendimento_num
                )

                medico_nao_atende_no_dia_do_atendimento = len(horarios_medico) == 0

                if medico_nao_atende_no_dia_do_atendimento:
                    raise serializers.ValidationError("Não é possível agendar este atendimento para a data selecionada. Por favor verifique a disponibilidade do medico!")
                else:
                    horarios_medico = horarios_medico.filter(
                        hora_inicial_horariomedico__lte=data["hora_inicio_atendimento"],
                        hora_final_horariomedico__gt=data["hora_inicio_atendimento"]
                    )

                    medico_nao_atende_no_horario_do_atendimento = len(horarios_medico) == 0

                    if medico_nao_atende_no_horario_do_atendimento:
                        raise serializers.ValidationError("Não é possível agendar este atendimento para o horário selecionado. Por favor verifique a disponibilidade do medico!")
                    else:
                        horarios_medico = horarios_medico.filter(
                            hora_final_horariomedico__gte=data["hora_termino_atendimento"]
                        )

                        medico_nao_atende_no_horario_do_atendimento = len(horarios_medico) == 0

                        if medico_nao_atende_no_horario_do_atendimento:
                            raise serializers.ValidationError("Não é possível agendar este atendimento para o horário selecionado. Por favor verifique a disponibilidade do medico!")
        
        # Não deve ser possível mudar a data de um atendimento para um período no qual a agenda do médico está fechada. As validações abaixo servem para garantir isto.
        bloqueios_agenda = BloqueioAgenda.objects.filter(
            medico_bloqueio_agenda__id__exact=medico.id,
            data_inicial__lte=data["data_atendimento"],
            data_final__gte=data["data_atendimento"]
        )

        data_atendimento_cai_em_bloqueio_agenda = len(bloqueios_agenda) > 0

        if data_atendimento_cai_em_bloqueio_agenda:
            raise serializers.ValidationError("Agenda bloqueada pelo médico! Não é possível agendar atendimentos para este dia.")
        
        # Não deve ser possível mudar a data de um atendimento para um período cadastrado como feriado. As validações abaixo servem para garantir isto.
        feriados = Feriado.objects.filter(
            data_inicial__lte=data["data_atendimento"],
            data_final__gte=data["data_atendimento"]
        )

        data_atendimento_cai_em_feriado = len(feriados) > 0

        if data_atendimento_cai_em_feriado:
            raise serializers.ValidationError("Feriado! Não é possível agendar atendimentos para este dia.")

        return data

class FeriadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feriado
        fields = ['nome_feriado', 'data_inicial',
                  'data_final']
    
    def validate(self, data):
        instance = self.instance

        data_atual = date.today()

        data_inicial = data['data_inicial']
        data_final = data['data_final']

        if instance:
            dataNaoMudouNaEdicao = instance.data_inicial == data_inicial and instance.data_final == data_final

            if dataNaoMudouNaEdicao:
                return data


        if data_inicial < data_atual:
            raise serializers.ValidationError("Data inicial deve ser posterior ou igual a data atual.")
        elif data_final < data_atual:
            raise serializers.ValidationError("Data final deve ser posterior a data atual.")
        elif data_inicial > data_final:
            raise serializers.ValidationError("Data final deve ser posterior a data inicial.")
        else:
            """
            Mesmo se nenhum dos casos acima acontecerem, ainda há a possibilidade de acontecer um caso que exige lançamento de exceção, pois o usuário pode tentar cadastrar um feriado para um período de tempo que já foi cadastrado como feriado.

            Existem 3 situações nas quais isto pode acontecer. Nos comentários abaixo, é explicado melhor quais são estas situações.
            """

            # Situação 01: A data inicial do feriado que será cadastrado está entre a data inicial e a data final de algum dos feriados já cadastrados. Para esta situação, independe qual a data final.
            feriados = Feriado.objects.filter(
                data_inicial__lte=data_inicial,
                data_final__gte=data_inicial
            )

            if instance:
                feriados = feriados.exclude(id__exact=instance.id)

            if feriados:
                raise serializers.ValidationError("Unidade possui feriado registrado.")
            else:
                # Situação 02: Se chegou aqui, a data inicial do feriado que será cadastrado não está entre a data inicial e a data final de algum dos feriados já cadastrados. Porém, a data final do mesmo pode está e a data inicial está antes da data inicial do mesmo feriado cadastrado.
                feriados = Feriado.objects.filter(
                    data_inicial__lte=data_final,
                    data_final__gte=data_final
                )

                if instance:
                    feriados = feriados.exclude(id__exact=instance.id)

                if feriados:
                    raise serializers.ValidationError("Unidade possui feriado registrado.")
                else:
                    # Situação 03: Se chegou aqui, ainda existe a possibilidade de que algum dos feriados esteja entre os dias do feriado que será cadastrado. Por exemplo, o feriado que será cadastrado é 10/10/2023 - 17/10/2023 e tem um feriado já cadastrado é 13/10/2023 - 15/10/2023.
                    feriados = Feriado.objects.filter(
                        data_inicial__gt=data_inicial,
                        data_final__lt=data_final
                    )

                    if instance:
                        feriados = feriados.exclude(id__exact=instance.id)

                    if feriados:
                        raise serializers.ValidationError("Unidade possui feriado registrado.") 
        return data

class BloqueioAgendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloqueioAgenda
        fields = ['medico_bloqueio_agenda', 'data_inicial',
                  'data_final', 'motivo']
    
    def validate(self, data):
        instance = self.instance

        data_atual = date.today()

        data_inicial = data['data_inicial']
        data_final = data['data_final']

        if instance:
            dataNaoMudouNaEdicao = instance.data_inicial == data_inicial and instance.data_final == data_final

            if dataNaoMudouNaEdicao:
                return data

        if data_inicial < data_atual:
            raise serializers.ValidationError("Data inicial deve ser posterior ou igual a data atual.")
        elif data_final < data_atual:
            raise serializers.ValidationError("Data final deve ser posterior a data atual.")
        elif data_inicial > data_final:
            raise serializers.ValidationError("Data final deve ser posterior a data inicial.")
        else:
            """
            Mesmo se nenhum dos casos acima acontecerem, ainda há a possibilidade de acontecer um caso que exige lançamento de exceção, pois o usuário pode tentar cadastrar um bloqueio de agenda para um período de tempo para o qual a agenda do médico já está bloqueada.

            Existem 3 situações nas quais isto pode acontecer. Nos comentários abaixo, é explicado melhor quais são estas situações.
            """

            # Situação 01: A data inicial do novo bloqueio está entre a data inicial e a data final de algum dos bloqueios já inseridos. Para esta situação, independe qual a data final.
            bloqueios_agenda = BloqueioAgenda.objects.filter(
                medico_bloqueio_agenda__id__exact=data["medico"].id,
                data_inicial__lte=data_inicial,
                data_final__gte=data_inicial
            )

            if instance:
                bloqueios_agenda = bloqueios_agenda.exclude(id__exact=instance.id)

            if bloqueios_agenda:
                raise serializers.ValidationError("A agenda do médico já foi bloqueada para este período! Por favor selecione um período diferente.")
            else:
                # Situação 02: Se chegou aqui, a data inicial do novo bloqueio não está entre a data inicial e a data final de algum dos bloqueios já inseridos. Porém, a data final do mesmo pode está e a data inicial está antes da data inicial do mesmo bloqueio inserido.
                bloqueios_agenda = BloqueioAgenda.objects.filter(
                    medico_bloqueio_agenda__id__exact=data["medico"].id,
                    data_inicial__lte=data_final,
                    data_final__gte=data_final
                )

                if instance:
                    bloqueios_agenda = bloqueios_agenda.exclude(id__exact=instance.id)

                if bloqueios_agenda:
                    raise serializers.ValidationError("A agenda do médico já foi bloqueada para este período! Por favor selecione um período diferente.")
                else:
                    # Situação 03: Se chegou aqui, ainda existe a possibilidade de que algum dos bloqueios esteja entre os dias do novo bloqueio. Por exemplo, o bloqueio que será cadastrado é 10/10/2023 - 17/10/2023 e tem um bloqueio já inserido é 13/10/2023 - 15/10/2023.
                    bloqueios_agenda = BloqueioAgenda.objects.filter(
                        medico_bloqueio_agenda__id__exact=data["medico"].id,
                        data_inicial__gt=data_inicial,
                        data_final__lt=data_final
                    )

                    if instance:
                        bloqueios_agenda = bloqueios_agenda.exclude(id__exact=instance.id)

                    if bloqueios_agenda:
                        raise serializers.ValidationError("A agenda do médico já foi bloqueada para este período! Por favor selecione um período diferente.")
            

        return data