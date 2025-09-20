from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from urllib.parse import quote
from .forms import LoginForm, SignupForm
from .decorators import login_required_jwt
from .utils_jwt import generate_jwt

COOKIE_OPTS = {
    'httponly': True,
    'samesite': 'Lax',
    'secure': False,      # em prod => True
    'path': '/',
}

def _set_auth_cookie(response, user):
    token = generate_jwt(user)
    response.set_cookie(settings.JWT_COOKIE_NAME, token, **COOKIE_OPTS)

def login_view(request):
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            resp = redirect(next_url or '/dashboard/')
            _set_auth_cookie(resp, user)
            return resp
        messages.error(request, 'Erro no login.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'next': next_url})

def logout_view(request):
    resp = redirect('/login/')
    resp.delete_cookie(settings.JWT_COOKIE_NAME, path='/')
    messages.success(request, 'Logout efetuado.')
    return resp

def signup_view(request):
    # Access control: only superusers can access signup
    if not request.user or not getattr(request.user, 'is_authenticated', False):
        next_url = quote(request.get_full_path())
        return redirect(f'/login/?next={next_url}')
    if not getattr(request.user, 'is_superuser', False):
        return redirect('/dashboard/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            resp = redirect('/dashboard/')
            _set_auth_cookie(resp, user)
            messages.success(request, 'Cadastro criado com sucesso!')
            return resp
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required_jwt
def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})