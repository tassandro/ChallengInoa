import requests
from decouple import config

API_URL = 'https://brapi.dev/api/quote/'
API_KEY = config('API_KEY')

def consultar_api(ticker):
    url = f'{API_URL}{ticker}?token={API_KEY}'
    r = requests.get(url)
    data = r.json()

    response = {}

    if data.get('error'):
        response['error'] = data.get('error')
        response['message'] = data.get('message')
    else:
        result = data.get('results', [])
        if result:
            response['longName'] = result[0].get('longName', 'No name available')
            response['regularMarketPrice'] = result[0].get('regularMarketPrice', 'No price available')

    return response

def obter_ativos_disponiveis():
    url = "https://brapi.dev/api/available"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erros na requisição
        data = response.json()

        if "stocks" in data:
            return data["stocks"]
        else:
            return "Dados de ativos não encontrados na resposta."
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a API: {e}"