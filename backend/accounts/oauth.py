from authlib.integrations.django_client import OAuth
from django.conf import settings

oauth = OAuth()

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="zoho",
    authorize_url=f"{settings.ZOHO_ACCOUNTS_DOMAIN}/oauth/v2/auth",
    access_token_url=f"{settings.ZOHO_ACCOUNTS_DOMAIN}/oauth/v2/token",
    api_base_url=f"{settings.ZOHO_ACCOUNTS_DOMAIN}/oauth/",
    client_id=settings.ZOHO_CLIENT_ID,
    client_secret=settings.ZOHO_CLIENT_SECRET,
    client_kwargs={"scope": "AaaServer.profile.Read", "access_type": "offline"},
)
