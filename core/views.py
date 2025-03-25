from decouple import config
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now


from core.forms import CreateAtivo
from core.models import Ativo, Cotacao
from core.scheduler import criar_monitoramento_ativo, excluir_monitoramento_ativo
from core.stocks import obter_ativos_disponiveis, consultar_api

API_URL = 'https://brapi.dev/api/quote/'
API_KEY = config('API_KEY')

def home(request):
    """Renderiza a página inicial com os ativos e cotações cadastradas."""
    return render(request, 'home.html', {
        "ativos": Ativo.objects.all(),
        "cotacoes": Cotacao.objects.all()
    })

def ativo(request):
    """Renderiza a página de cadastro/edição de um ativo."""
    id_ativo = request.GET.get('id')
    
    if id_ativo:
        ativo = get_object_or_404(Ativo, id=id_ativo)
        form = CreateAtivo(initial={
            'ticker': ativo.ticker,
            'limite_inferior': ativo.limite_inferior,
            'limite_superior': ativo.limite_superior,
            'periodicidade': ativo.periodicidade
        })
        form.fields['ticker'].widget.attrs['readonly'] = True
    else:
        form = CreateAtivo()

    return render(request, 'ativo.html', {'form': form})

def submit_ativo(request):
    if request.POST:
        ticker = request.POST.get('ticker').upper()
        lim_sup = request.POST.get('limite_superior')
        lim_inf = request.POST.get('limite_inferior')
        periodo = request.POST.get('periodicidade')


        if Ativo.objects.filter(ticker=ticker).exists():
            messages.error(request, f"O ativo '{ticker}' já está sendo monitorado!")
            return redirect("/home/ativo/")  

        ativos_disponiveis = obter_ativos_disponiveis()
        if ticker not in ativos_disponiveis:
            messages.error(request, f"O ativo '{ticker}' não foi encontrado na API. Verifique o código e tente novamente.")
            return redirect("/home/ativo/")  

        ativo_info = consultar_api(ticker)
        nome_completo = ativo_info.get("longName", "Nome não disponível")

        ativo = Ativo.objects.create(
            ticker=ticker,
            nome=nome_completo,
            limite_superior=lim_sup,
            limite_inferior=lim_inf,
            periodicidade=periodo
        )

        criar_monitoramento_ativo(ticker)

        cotacao_info = consultar_api(ticker)
        preco_atual = cotacao_info.get("regularMarketPrice")
        if preco_atual:
            Cotacao.objects.create(
                ativo=ativo,
                preco=preco_atual,
                data_hora=now()
            )

    return redirect("/")



def deletar_ativo(request, id):
    """Exclui um ativo do banco de dados e interrompe seu monitoramento."""
    ativo = get_object_or_404(Ativo, id=id)
    excluir_monitoramento_ativo(ativo.ticker)
    ativo.delete()
    return redirect('/')

def obter_cotacoes(request, id):
    ativo = get_object_or_404(Ativo, id=id)

    cotacoes = [
        f"Data: {cotacao.data_hora.strftime('%d/%m/%Y')} | "
        f"Horário: {cotacao.data_hora.strftime('%H:%M:%S')} | "
        f"Valor: R${cotacao.preco:.2f}".replace('.', ',')
        for cotacao in Cotacao.objects.filter(ativo=ativo.id)
    ]

    return JsonResponse({'cotacoes': cotacoes})



