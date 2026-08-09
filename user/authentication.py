from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware, RejectRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied


class CookieJWTAuthentication(JWTAuthentication):
    """Accept the standard Bearer token and the browser auth cookie."""

    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)

        raw_token = request.COOKIES.get(settings.AUTH_ACCESS_COOKIE)
        if not raw_token:
            return None

        if request.method not in {"GET", "HEAD", "OPTIONS", "TRACE"}:
            enforce_csrf(request)

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token


def enforce_csrf(request):
    try:
        CsrfViewMiddleware(lambda _request: None)._check_token(request)
    except RejectRequest as exc:
        raise PermissionDenied("CSRF validation failed.") from exc
