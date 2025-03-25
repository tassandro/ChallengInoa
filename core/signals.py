import requests
import logging
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from core.models import Ticker


logger = logging.getLogger(__name__)

@receiver(post_migrate)
def initialize_items(sender, **kwargs):
    """Busca e salva os códigos de ativos disponíveis na API no modelo Ticker."""
    url = "https://brapi.dev/api/available"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        stocks = data.get("stocks", [])
        if not isinstance(stocks, list):
            logger.warning("Formato inesperado dos dados da API. Nenhum ativo salvo.")
            return

        codigos_existentes = set(Ticker.objects.values_list("codigo", flat=True))
        novos_tickers = [Ticker(codigo=stock) for stock in stocks if stock not in codigos_existentes]

        if novos_tickers:
            Ticker.objects.bulk_create(novos_tickers)
            logger.info(f"{len(novos_tickers)} novos registros de ações foram salvos no banco de dados.")
        else:
            logger.info("Nenhum novo ativo foi adicionado ao banco de dados.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar a API: {e}")
