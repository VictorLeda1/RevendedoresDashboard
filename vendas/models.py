from django.db import models

# Venda = Produto, valor, data, cliente, vendedor, cupom

class Venda(models.Model):
    produto = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100, null=True, blank=True)
    vendedor = models.CharField(max_length=100, null=True, blank=True)
    cupom = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.produto
