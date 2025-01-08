from django.contrib import admin
from core.models import Ativo, Cotacao

class AtivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker', 'limite_superior', 'limite_inferior', 'periodicidade')

class CotacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ativo', 'preco', 'data_hora')

# Register your models here.
admin.site.register(Ativo, AtivoAdmin)
admin.site.register(Cotacao, CotacaoAdmin)