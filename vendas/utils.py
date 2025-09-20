from typing import Optional
from django.db.models import QuerySet
from .models import Venda


def vendas_do_usuario(user) -> QuerySet[Venda]:
    """
    Retorna as vendas cujo campo `cupom` corresponde ao `cupom_reseller` do usuário.
    Se o usuário não tiver cupom definido, retorna um queryset vazio.
    """
    cupom: Optional[str] = getattr(user, 'cupom_reseller', None)
    if not cupom:
        return Venda.objects.none()
    return Venda.objects.filter(cupom=cupom).order_by('-data')
