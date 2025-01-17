import requests
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from core.models import Ticker

"""
    O signal abaixo foi criado para salvar os códigos dos ativos disponibilizados pela API.
    Ia ser implementada uma busca por esses código no sistema, mas optou-se por não fazer isso.
"""

@receiver(post_migrate)
def initialize_items(sender, **kwargs):
    url = "https://brapi.dev/api/available"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erros na requisição
        data = response.json()

        if "stocks" in data:
            stocks = data["stocks"]

            # Salvar os dados no modelo Ticker
            for stock in stocks:
                Ticker.objects.get_or_create(codigo=stock)

            return f"{len(stocks)} registros de ações foram salvos/atualizados no banco de dados."
        else:
            return "Dados de ativos não encontrados na resposta."
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a API: {e}"