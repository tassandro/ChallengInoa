from django.contrib import admin
from core.models import Ativo, Cotacao, Ticker

class AtivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'limite_superior', 'limite_inferior', 'periodicidade')

class CotacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ativo', 'preco', 'data_hora')

class TickerAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo')

# Register your models here.
admin.site.register(Ativo, AtivoAdmin)
admin.site.register(Cotacao, CotacaoAdmin)
admin.site.register(Ticker, TickerAdmin)
