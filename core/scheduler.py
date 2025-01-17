from datetime import datetime, timedelta
from decouple import config

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from django.core.mail import send_mail
from core.models import Ativo, Cotacao

import requests

"""
    Aqui estão as funções relacionadas com o gerenciamento de tarefas do scheduler.
    
    Criação, alteração e exclusão de tarefas.
    
    A tarefas são salvas no banco de dados e persistem caso o servidor seja reiniciado.
    
    Problema conhecido: ao reiniciar o servidor, pode acontecer de uma tarefa de monitoramento
    de um mesmo ativo ser executada mais um vez no mesmo tempo. Isso gera registro a mais no banco.
    Não consegui resolver esse problema.
    
"""

import os
# Caminho do banco de dados SQLite usado no Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sqlite_path = os.path.join(BASE_DIR, 'db.sqlite3')

# Configuração do JobStore com SQLite
jobstores = {
    'default': SQLAlchemyJobStore(url=f'sqlite:///{sqlite_path}')  # Conectar o APScheduler ao banco do Django
}

job_defaults = {
    'misfire_grace_time': 10,  # Limite de 10 segundos para *misfires*
    'coalesce': True,  # Junta execuções múltiplas atrasadas em uma única execução
    'max_instances': 1  # Evita múltiplas execuções simultâneas do mesmo *job*
}

# Criação do scheduler com configuração do JobStore
scheduler = BackgroundScheduler(jobstores=jobstores, job_defaults=job_defaults)
scheduler.start()

API_URL = 'https://brapi.dev/api/quote/'
API_KEY = config('API_KEY')

def obter_cotacao(ticker):
    url = f'{API_URL}{ticker}?token={API_KEY}'
    response = requests.get(url)
    data = response.json()

    preco_atual = None
    ativo = Ativo.objects.get(ticker=ticker)

    if data.get('error'):
        print(f'Não foi possível obter a cotação do ativo - {ticker}.')
    else:
        result = data.get('results', [])
        if result:
            preco_atual = result[0].get('regularMarketPrice', 'No price available')
            if ativo.nome is None:
                ativo.nome = result[0].get('longName', 'No name available')
                ativo.save()

    Cotacao.objects.create(ativo=ativo, preco=preco_atual)
    print("Cotação criada com sucesso!")

    data_hora = datetime.now().strftime('%H:%M:%S do dia %d/%m/%Y')

    if preco_atual <= ativo.limite_inferior:
        send_mail(
            subject=f'Alerta de compra do ativo {ticker}!',
            message=f'A cotação do ativo {ticker} atingiu o valor de R${preco_atual}, às {data_hora}.\n\n'
                    f'O limite inferior definido foi de R${ativo.limite_inferior}.',
            from_email=config('EMAIL_HOST_USER'),
            recipient_list=[config('EMAIL_HOST_USER')],
            fail_silently=False
        )
        print(f"E-mail de compra enviado - Valor da cotação do ativo {ticker}:R${preco_atual}")
    if preco_atual >= ativo.limite_superior:
        send_mail(
            subject=f'Alerta de venda do ativo {ticker}!',
            message=f'A cotação do ativo {ticker} atingiu o valor de R${preco_atual}, às {data_hora} \n\n'
                    f'O limite superior definido foi de R${ativo.limite_superior}.',
            from_email=config('EMAIL_HOST_USER'),
            recipient_list=[config('EMAIL_HOST_USER')],
            fail_silently=False
        )
        print(f"E-mail de venda enviado - Valor da cotação do ativo {ticker}:R${preco_atual}")


def criar_monitoramento_ativo(ticker):
    ativo = Ativo.objects.get(ticker=ticker)

    intervalo = ativo.periodicidade

    if scheduler.get_job(ticker): # Alteração do ativo já existente
        scheduler.reschedule_job(
            job_id=ticker,
            trigger='interval',
            minutes=intervalo,
        )
    else: # Criação do ativo
        scheduler.add_job(
            obter_cotacao,
            'interval',
            minutes=intervalo,
            args=[ticker],
            id=ticker,
            replace_existing=True,
            start_date=datetime.now() + timedelta(seconds=5)  # Executar após 5s de reinício
        )

def excluir_monitoramento_ativo(ticker):
    if scheduler.get_job(ticker):
        scheduler.remove_job(ticker)
        print(f"{ticker} removido do monitoramento.")

def shutdown_scheduler():
    scheduler.shutdown(wait=False)