from django.db import models

class Ticker(models.Model):
    codigo = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.codigo

class Ativo(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    limite_inferior = models.DecimalField(max_digits=10, decimal_places=2, help_text="Limite inferior do túnel de preço")
    limite_superior = models.DecimalField(max_digits=10, decimal_places=2, help_text="Limite superior do túnel de preço")
    periodicidade = models.IntegerField(help_text="Periodicidade de checagem (em minutos)")

    def __str__(self):
        return f"{self.ticker} - {self.nome or 'Ativo'}"

class Cotacao(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE, related_name="cotacoes")
    preco = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço registrado do ativo")
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ativo.ticker} - {self.preco} em {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"

