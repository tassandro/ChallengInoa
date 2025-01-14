from apscheduler.schedulers.background import BackgroundScheduler

from core.models import Ativo, Cotacao

import requests

# Scheduler responsável por executar jobs
# É configurado com opções default
scheduler = BackgroundScheduler()
scheduler.start()

API_URL = 'https://brapi.dev/api/quote/'
API_KEY = '6s4xhTzigCC6bbdpf6Pk3Z'

# https://brapi.dev/api/available

def obter_cotacao(ticker):
    url = f'{API_URL}{ticker}?token={API_KEY}'
    r = requests.get(url)
    data = r.json()

    preco_atual = None

    if data.get('error'):
        print(f'Não foi possível obter a cotação do ativo - {ticker}.')
    else:
        result = data.get('results', [])
        if result:
            preco_atual = result[0].get('regularMarketPrice', 'No price available')

    ativo = Ativo.objects.get(ticker=ticker)

    Cotacao.objects.create(ativo=ativo, preco=preco_atual)
    print("Cotação criada com sucesso!")

    if preco_atual <= ativo.limite_inferior:
        print("Compre")
    if preco_atual >= ativo.limite_superior:
        print('Venda')


def criar_monitoramento_ativo(ticker):
    ativo = Ativo.objects.get(ticker=ticker)

    intervalo = ativo.periodicidade

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