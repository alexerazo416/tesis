from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from .models import Usuario
from django.urls import reverse
def role_required(allowed_roles):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if 'user_id' not in request.session:
                return redirect('login')
            user = Usuario.objects.get(id=request.session['user_id'])
            if user.rol not in allowed_roles:
                return redirect(reverse('permission_denied'))
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator
