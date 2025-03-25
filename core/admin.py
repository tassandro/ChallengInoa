from django.contrib import admin
from core.models import Ativo, Cotacao, Ticker

"""
   Configuração do Django Admin para visualização e gerenciamento dos dados no painel administrativo.
"""

@admin.register(Ativo)
class AtivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'limite_superior', 'limite_inferior', 'periodicidade')
    search_fields = ('ticker__codigo',)
    list_filter = ('periodicidade',)
    ordering = ('id',)

@admin.register(Cotacao)
class CotacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ativo', 'preco', 'data_hora')
    search_fields = ('ativo__ticker__codigo',)
    list_filter = ('data_hora',)
    ordering = ('-data_hora',)

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo')
    search_fields = ('codigo',)
    ordering = ('codigo',)
