from datetime import datetime, timedelta

def calcular_proxima_hora_aplicacao_diaria(data_ultima_aplicacao, posologia_horas):
    try:
        data_ultima_aplicacao = datetime.strptime(data_ultima_aplicacao, '%d/%m/%Y %H:%M')
        proxima_aplicacao = data_ultima_aplicacao + timedelta(hours=int(posologia_horas))
        agora = datetime.now()

        if agora >= proxima_aplicacao:
            return "Já passou da hora da próxima aplicação."
        else:
            return proxima_aplicacao.strftime('%d/%m/%Y %H:%M')
    except ValueError:
        return "Formato de data inválido."

def calcular_proxima_hora_aplicacao_semanal(data_ultima_aplicacao_str):
    try:
        data_ultima_aplicacao = datetime.strptime(data_ultima_aplicacao_str, '%d/%m/%Y %H:%M')
        proxima_aplicacao = data_ultima_aplicacao + timedelta(weeks=1)
        agora = datetime.now()

        if agora >= proxima_aplicacao:
            return "Já passou da hora da próxima aplicação."
        else:
            return proxima_aplicacao.strftime('%d/%m/%Y %H:%M')
    except ValueError:
        return "Formato de data inválido."

def calcular_proxima_hora_aplicacao_mensal(data_ultima_aplicacao_str):
    try:
        data_ultima_aplicacao = datetime.strptime(data_ultima_aplicacao_str, '%d/%m/%Y %H:%M')
        proxima_aplicacao = data_ultima_aplicacao + timedelta(days=30)  # Considerando média de 30 dias para cálculo mensal
        agora = datetime.now()

        if agora >= proxima_aplicacao:
            return "Já passou da hora da próxima aplicação."
        else:
            return proxima_aplicacao.strftime('%d/%m/%Y %H:%M')
    except ValueError:
        return "Formato de data inválido."
