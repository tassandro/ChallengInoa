from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from core.forms import LoginForm, CreateAtivo
from core.models import Ativo,Cotacao
import requests

API_URL = 'https://brapi.dev/api/quote/'
API_KEY = '6s4xhTzigCC6bbdpf6Pk3Z'

def get_data(request, ticker):
    url = f'{API_URL}{ticker}?token={API_KEY}'
    print(url)
    r = requests.get(url)
    data = r.json()

    return JsonResponse(data)


def home(request):
    user = request.user
    ativos = Ativo.objects.filter(usuario=user)
    cotacoes = Cotacao.objects.filter(ativo__in=ativos)
    return render(request, 'home.html', {"user": user, "ativos": ativos, "cotacoes": cotacoes})


def login_user(request):
    return render(request, 'login.html', {'form': LoginForm()})

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Login inválido! Tente novamente.")
            return redirect('/login/')
    return redirect('/')


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
    print(id_ativo)
    dado = {}

    if id_ativo:
        ativo = Ativo.objects.get(id=id_ativo)
        dados_form = {'ticker': ativo.ticker,
                    'limite_inferior': ativo.limite_inferior,
                    'limite_superior': ativo.limite_superior,
                    'periodicidade': ativo.periodicidade}
        dados = {'form': CreateAtivo(initial=dados_form)}
    else:
        dados = {'form': CreateAtivo()}

    return render(request, 'ativo.html', dados)

def deletar_ativo(request, id):
    usuario = request.user
    ativo = Ativo.objects.get(id=id)

    if ativo.usuario == usuario:
        ativo.delete()
    return redirect('/')


def submit_ativo(request):
    if request.POST:
        ticker = request.POST.get('ticker')
        lim_sup = request.POST.get('limite_superior')
        lim_inf = request.POST.get('limite_inferior')
        periodo = request.POST.get('periodicidade')
        usuario = request.user
        if Ativo.objects.filter(ticker__exact=ticker).exists():
            Ativo.objects.filter(ticker__exact=ticker).update(ticker=ticker,
                                                               limite_superior=lim_sup,
                                                               limite_inferior=lim_inf,
                                                               periodicidade=periodo)
        else:
            Ativo.objects.create(ticker=ticker,
                               limite_superior=lim_sup,
                               limite_inferior=lim_inf,
                               periodicidade=periodo,
                                usuario=usuario)
    return redirect('/')