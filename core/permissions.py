from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def get_role(user):
    """Retorna 'admin', 'funcionario', 'paciente' ou None."""
    if not user.is_authenticated:
        return None
    if user.is_superuser or user.is_staff:
        return 'admin'
    if hasattr(user, 'funcionario'):
        return 'funcionario'
    if hasattr(user, 'paciente'):
        return 'paciente'
    return None


def roles_required(*roles):
    """
    Decorator de view: exige login e um dos papéis informados.
    Uso: @roles_required('admin', 'funcionario')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if get_role(request.user) not in roles:
                raise PermissionDenied('Você não tem permissão para acessar esta página.')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
