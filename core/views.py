from django.db import connection
from django.db.utils import DatabaseError
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(request):
    """Return a safe liveness/readiness response for reverse proxies."""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse(
            {'status': 'degraded', 'database': 'unavailable'},
            status=503,
        )

    return JsonResponse({'status': 'ok', 'database': 'ok'})
