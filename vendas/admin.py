from django.contrib import admin
from .models import Venda

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('produto', 'valor', 'data', 'cliente', 'vendedor', 'cupom')
    list_filter = ('data', 'vendedor')
    search_fields = ('produto', 'cliente', 'vendedor', 'cupom')
