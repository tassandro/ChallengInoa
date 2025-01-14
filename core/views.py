import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect

from core.forms import LoginForm, CreateAtivo
from core.models import Ativo, Cotacao
from core.scheduler import criar_monitoramento_ativo,excluir_monitoramento_ativo

API_URL = 'https://brapi.dev/api/quote/'
API_KEY = '6s4xhTzigCC6bbdpf6Pk3Z'

def get_api(ticker):
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

def home(request):
    user = request.user
    ativos = Ativo.objects.all()
    cotacoes = Cotacao.objects.all()
    return render(request, 'home.html', {"ativos": ativos, "cotacoes": cotacoes})



# def visualizar_historico(request):
#     # Recuperar todos os ativos para exibição no dropdown
#     ativos = Ativo.objects.all()
#     cotacoes = []
#     selected_ativo = None
#
#     # Se o formulário foi enviado via POST
#     if request.method == 'POST':
#         selected_ativo = request.POST.get('selected_ativo')  # Recupera o ID do ativo selecionado
#         if selected_ativo:  # Se um ativo válido foi selecionado
#             cotacoes = Cotacao.objects.filter(ativo=selected_ativo)  # Filtra cotações pelo ativo selecionado
#
#     # Renderiza o template com os dados necessários
#     return render(request, 'home.html', {
#         'ativos': ativos,
#         'cotacoes': cotacoes,
#         'selected_ativo': selected_ativo,
#     })

def ativo(request):
    id_ativo = request.GET.get('id')
    dado = {}

    if id_ativo:
        ativo = Ativo.objects.get(id=id_ativo)
        dados_form = {'ticker': ativo.ticker,
                    'limite_inferior': ativo.limite_inferior,
                    'limite_superior': ativo.limite_superior,
                    'periodicidade': ativo.periodicidade}
        # Instancia o formulário com os dados existentes
        form = CreateAtivo(initial=dados_form)

        # Torna o campo "ticker" não editável
        form.fields['ticker'].widget.attrs['readonly'] = True

        dados = {'form': form}
    else:
        dados = {'form': CreateAtivo()}

    return render(request, 'ativo.html', dados)


def submit_ativo(request):
    if request.POST:
        ticker = request.POST.get('ticker')
        lim_sup = request.POST.get('limite_superior')
        lim_inf = request.POST.get('limite_inferior')
        periodo = request.POST.get('periodicidade')
        if Ativo.objects.filter(ticker__exact=ticker).exists():
            Ativo.objects.filter(ticker__exact=ticker).update(limite_superior=lim_sup,
                                                               limite_inferior=lim_inf,
                                                               periodicidade=periodo)
            criar_monitoramento_ativo(ticker)
        else:
            response = get_api(ticker)

            if response.get('error'):
                messages.error(request, response['message']) # Não está funcionando
            else:
                # print(response)
                Ativo.objects.create(ticker=ticker,
                                     nome=response.get('longName'),
                                     limite_superior=lim_sup,
                                     limite_inferior=lim_inf,
                                     periodicidade=periodo)
                criar_monitoramento_ativo(ticker)
                # messages.success(request, "Ativo criado com sucesso!")
    return redirect('/')

def deletar_ativo(request, id):
    ativo = Ativo.objects.get(id=id)
    excluir_monitoramento_ativo(ativo.ticker)
    ativo.delete()
    return redirect('/')