import requests
from decouple import config
from core.models import Ticker

API_URL = 'https://brapi.dev/api/quote/'
API_KEY = config('API_KEY')

def consultar_api(ticker):
    """Consulta a API e retorna informações sobre o ativo."""
    url = f'{API_URL}{ticker}?token={API_KEY}'
    
    try:
        response = requests.get(url)
        data = response.json()
    except requests.RequestException as e:
        return {'error': 'Erro ao conectar com a API', 'message': str(e)}

    if 'error' in data:
        return {'error': data.get('error'), 'message': data.get('message')}

    result = data.get('results', [])
    if result:
        return {
            'longName': result[0].get('longName', 'Nome não disponível'),
            'regularMarketPrice': result[0].get('regularMarketPrice', 'Preço não disponível'),
        }
    
    return {'error': 'Dados não encontrados'}

def obter_ativos_disponiveis():
    """Retorna uma lista dos tickers disponíveis no banco de dados."""
    return list(Ticker.objects.values_list('codigo', flat=True))
