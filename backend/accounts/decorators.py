from functools import wraps

from django.http import JsonResponse


def require_permission(code):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({"detail": "Authentication required"}, status=401)
            if not request.user.has_perm(code):
                return JsonResponse({"detail": "Permission denied"}, status=403)
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
