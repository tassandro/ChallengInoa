import os
import logging
from datetime import datetime, timedelta
from decouple import config
import requests
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from core.models import Ativo, Cotacao

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho do banco de dados SQLite usado no Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sqlite_path = os.path.join(BASE_DIR, "db.sqlite3")

# Configuração do JobStore com SQLite
jobstores = {"default": SQLAlchemyJobStore(url=f"sqlite:///{sqlite_path}")}

job_defaults = {
    "misfire_grace_time": 10,  
    "coalesce": True,  
    "max_instances": 1,  
}

# Criação do scheduler com configuração do JobStore
scheduler = BackgroundScheduler(jobstores=jobstores, job_defaults=job_defaults)
scheduler.start()

# Configuração da API
API_URL = "https://brapi.dev/api/quote/"
API_KEY = config("API_KEY")
EMAIL_REMETENTE = config("EMAIL_HOST_USER")


def buscar_dados_api(ticker):
    """Faz a requisição para a API e retorna o preço do ativo."""
    try:
        url = f"{API_URL}{ticker}?token={API_KEY}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  

        data = response.json()
        if data.get("error"):
            logger.warning(f"Erro na API para {ticker}: {data['error']}")
            return None

        result = data.get("results", [])
        if not result:
            logger.warning(f"⚠️ Nenhum dado encontrado para {ticker}.")
            return None

        return {
            "preco": result[0].get("regularMarketPrice"),
            "nome": result[0].get("longName"),
        }

    except requests.RequestException as e:
        logger.error(f"Erro ao buscar dados da API para {ticker}: {e}")
        return None


def enviar_email_alerta(ticker, preco_atual, limite, tipo_alerta):
    """Envia um e-mail de alerta para compra ou venda."""
    data_hora = datetime.now().strftime("%H:%M:%S do dia %d/%m/%Y")

    assunto = f"Alerta de {tipo_alerta} do ativo {ticker}!"
    mensagem = (
        f"A cotação do ativo {ticker} atingiu o valor de R${preco_atual:.2f}, às {data_hora}.\n\n"
        f"O limite definido foi de R${limite:.2f}.\n"
        f"Essa pode ser uma oportunidade de {tipo_alerta.lower()}!"
    )

    send_mail(
        subject=assunto,
        message=mensagem,
        from_email=EMAIL_REMETENTE,
        recipient_list=[EMAIL_REMETENTE],  
        fail_silently=False,
    )

    logger.info(f"E-mail de {tipo_alerta} enviado - {ticker}: R${preco_atual:.2f}")


def obter_cotacao(ticker):
    """Obtém a cotação do ativo e dispara alertas caso necessário."""
    ativo = Ativo.objects.get(ticker=ticker)
    dados = buscar_dados_api(ticker)
    if not dados:
        return

    preco_atual = dados["preco"]

    if ativo.nome is None and dados["nome"]:
        ativo.nome = dados["nome"]
        ativo.save()

    # Prevenção de e-mails duplicados
    ultima_cotacao = Cotacao.objects.filter(ativo=ativo).order_by("-data_hora").first()
    if ultima_cotacao and ultima_cotacao.preco == preco_atual:
        logger.info(f"Cotação de {ticker} já registrada recentemente. Nenhum e-mail enviado.")
        return

    # Criação do registro de cotação
    Cotacao.objects.create(ativo=ativo, preco=preco_atual)
    logger.info(f"Cotação registrada - {ticker}: R${preco_atual:.2f}")

    # Envio de alertas se os limites forem atingidos
    if preco_atual <= ativo.limite_inferior:
        enviar_email_alerta(ticker, preco_atual, ativo.limite_inferior, "compra")

    elif preco_atual >= ativo.limite_superior:
        enviar_email_alerta(ticker, preco_atual, ativo.limite_superior, "venda")


def criar_monitoramento_ativo(ticker):
    """Cria ou altera o monitoramento de um ativo no scheduler."""
    ativo = Ativo.objects.get(ticker=ticker)
    intervalo = ativo.periodicidade

    if scheduler.get_job(ticker): 
        scheduler.reschedule_job(job_id=ticker, trigger="interval", minutes=intervalo)
        logger.info(f"⏳ Monitoramento de {ticker} atualizado para {intervalo} minutos.")
    else:  
        scheduler.add_job(
            obter_cotacao,
            "interval",
            minutes=intervalo,
            args=[ticker],
            id=ticker,
            replace_existing=True,
            start_date=datetime.now() + timedelta(seconds=5), 
        )
        logger.info(f"Monitoramento de {ticker} iniciado a cada {intervalo} minutos.")


def excluir_monitoramento_ativo(ticker):
    """Remove um ativo do monitoramento."""
    if scheduler.get_job(ticker):
        scheduler.remove_job(ticker)
        logger.info(f"{ticker} removido do monitoramento.")


def shutdown_scheduler():
    """Desliga o scheduler corretamente."""
    scheduler.shutdown(wait=False)
    logger.info("Scheduler desligado.")
