from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .oauth import oauth

User = get_user_model()


def _get_or_create_user(email, first_name="", last_name=""):
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_active": True,
        },
    )
    if created:
        user.set_unusable_password()
        user.save()
    return user


def _login_user(request, user):
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")


@require_http_methods(["GET"])
def google_login(request):
    redirect_uri = request.build_absolute_uri(reverse("accounts:google_callback"))
    return oauth.google.authorize_redirect(request, redirect_uri)


@require_http_methods(["GET"])
def google_callback(request):
    token = oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo") or {}
    email = userinfo.get("email")
    if not email or not userinfo.get("email_verified"):
        return JsonResponse({"detail": "Google account has no verified email"}, status=400)

    user = _get_or_create_user(
        email,
        first_name=userinfo.get("given_name", ""),
        last_name=userinfo.get("family_name", ""),
    )
    _login_user(request, user)
    return _redirect_to_frontend()


@require_http_methods(["GET"])
def zoho_login(request):
    redirect_uri = request.build_absolute_uri(reverse("accounts:zoho_callback"))
    return oauth.zoho.authorize_redirect(request, redirect_uri)


@require_http_methods(["GET"])
def zoho_callback(request):
    token = oauth.zoho.authorize_access_token(request)
    userinfo = oauth.zoho.get("user/info", token=token).json()
    email = userinfo.get("Email")
    if not email:
        return JsonResponse({"detail": "Zoho account has no email"}, status=400)

    user = _get_or_create_user(
        email,
        first_name=userinfo.get("First_Name", ""),
        last_name=userinfo.get("Last_Name", ""),
    )
    _login_user(request, user)
    return _redirect_to_frontend()


def _redirect_to_frontend():
    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/customers")


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({"detail": "logged out"})


@require_http_methods(["GET"])
def me(request):
    get_token(request)  # ensure the csrftoken cookie is set for anonymous visitors too
    if not request.user.is_authenticated:
        return JsonResponse({"is_authenticated": False})
    return JsonResponse(
        {
            "is_authenticated": True,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "permissions": sorted(request.user.get_all_permissions()),
        }
    )
