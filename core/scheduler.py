from datetime import datetime
from decouple import config

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from django.core.mail import send_mail
from core.models import Ativo, Cotacao

import requests
import os

# Caminho do banco de dados SQLite usado no Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sqlite_path = os.path.join(BASE_DIR, 'db.sqlite3')

# Configuração do JobStore com SQLite
jobstores = {
    'default': SQLAlchemyJobStore(url=f'sqlite:///{sqlite_path}')  # Conectar o APScheduler ao banco do Django
}

# Criação do scheduler com configuração do JobStore
scheduler = BackgroundScheduler(jobstores=jobstores)
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
            subject=f'Alerta de compra do ativo {ticker}!',  # Assunto
            message=f'A cotação do ativo {ticker} atingiu o valor de R${preco_atual}, às {data_hora}',  # Mensagem
            from_email=config('EMAIL_HOST_USER'),  # Remetente (from)
            recipient_list=[config('EMAIL_HOST_USER')],  # Lista de destinatários
            fail_silently=False  # Lança erro se houver falha
        )
        print(f"E-mail de compra enviado - Valor da cotação do ativo {ticker}:R${preco_atual}")
    if preco_atual >= ativo.limite_superior:
        send_mail(
            subject=f'Alerta de venda do ativo {ticker}!',  # Assunto
            message=f'A cotação do ativo {ticker} atingiu o valor de R${preco_atual}, às {data_hora}',  # Mensagem
            from_email=config('EMAIL_HOST_USER'),  # Remetente (from)
            recipient_list=[config('EMAIL_HOST_USER')],  # Lista de destinatários
            fail_silently=False  # Lança erro se houver falha
        )
        print(f"E-mail de venda enviado - Valor da cotação do ativo {ticker}:R${preco_atual}")


def criar_monitoramento_ativo(ticker):
    ativo = Ativo.objects.get(ticker=ticker)

    intervalo = ativo.periodicidade

    obter_cotacao(ticker)

    if scheduler.get_job(ticker):
        print(f"Monitoramento do ativo {ticker} já existe. Verificando se é necessário alterar o intervalo.")
        scheduler.reschedule_job(
            job_id=ticker,
            trigger='interval',
            minutes=intervalo,
        )
        print(f"Monitoramento do ativo {ticker} modificado com sucesso - intervalo de {intervalo} minutos."),

    else:
        scheduler.add_job(
            obter_cotacao,
            'interval',
            minutes=intervalo,
            args=[ticker],
            id=ticker,
            replace_existing=True,
        )
        print(f"Monitoramento do ativo {ticker} criado com sucesso - intervalo de {intervalo} minutos."),

def excluir_monitoramento_ativo(ticker):
    if scheduler.get_job(ticker):
        scheduler.remove_job(ticker)
        print(f"{ticker} removido do monitoramento.")