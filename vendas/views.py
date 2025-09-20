from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from contas.decorators import login_required_jwt
from .forms import VendaForm
from urllib.parse import quote

@login_required_jwt
def nova_venda_view(request):
    # Access control: only superusers can access nova venda
    if not request.user or not getattr(request.user, 'is_authenticated', False):
        next_url = quote(request.get_full_path())
        return redirect(f'/login/?next={next_url}')
    if not getattr(request.user, 'is_superuser', False):
        return redirect('/dashboard/')

    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save()
            messages.success(request, 'Venda registrada com sucesso!')
            return redirect('/dashboard/')
        messages.error(request, 'Erro ao salvar a venda.')
    else:
        form = VendaForm()
    return render(request, 'vendas_form.html', {'form': form})
