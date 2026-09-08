from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("google/login/", views.google_login, name="google_login"),
    path("google/callback/", views.google_callback, name="google_callback"),
    path("zoho/login/", views.zoho_login, name="zoho_login"),
    path("zoho/callback/", views.zoho_callback, name="zoho_callback"),
    path("logout/", views.logout_view, name="logout"),
    path("me/", views.me, name="me"),
]
