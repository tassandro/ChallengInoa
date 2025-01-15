import requests
from decouple import config

from django.contrib import messages
from django.shortcuts import render, redirect

from core.forms import LoginForm, CreateAtivo
from core.models import Ativo, Cotacao
from core.scheduler import criar_monitoramento_ativo,excluir_monitoramento_ativo
from core.stocks import obter_ativos_disponiveis, consultar_api

API_URL = 'https://brapi.dev/api/quote/'
API_KEY = config('API_KEY')

def home(request):
    user = request.user
    ativos = Ativo.objects.all()
    cotacoes = Cotacao.objects.all()
    return render(request, 'home.html', {"ativos": ativos, "cotacoes": cotacoes})

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
        # Caso o ativo já esteja criado no banco
        if Ativo.objects.filter(ticker__exact=ticker).exists():
            Ativo.objects.filter(ticker__exact=ticker).update(limite_superior=lim_sup,
                                                               limite_inferior=lim_inf,
                                                               periodicidade=periodo)
        # Caso o ativo ainda não foi criado no banco
        else:
            # Verifica se o ativo está disponivel
            if ticker in obter_ativos_disponiveis():
                Ativo.objects.create(ticker=ticker,
                                     limite_superior=lim_sup,
                                     limite_inferior=lim_inf,
                                     periodicidade=periodo)
            else:
                return redirect('/')
        criar_monitoramento_ativo(ticker)

    return redirect('/')

def deletar_ativo(request, id):
    ativo = Ativo.objects.get(id=id)
    excluir_monitoramento_ativo(ativo.ticker)
    ativo.delete()
    return redirect('/')