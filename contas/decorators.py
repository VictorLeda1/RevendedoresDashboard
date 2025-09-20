from functools import wraps
from django.shortcuts import redirect
from urllib.parse import quote

def login_required_jwt(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        next_url = quote(request.get_full_path())
        return redirect(f'/login/?next={next_url}')
    return _wrapped