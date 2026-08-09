import os

from django.conf import settings
from django.core.checks import Error, Tags, register


@register(Tags.security)
def payment_configuration_check(app_configs, **kwargs):
    if settings.PAYMENT_PROVIDER != 'mpesa':
        return []

    errors = []
    if not settings.MPESA_CALLBACK_BASE_URL:
        errors.append(Error(
            'MPESA_CALLBACK_BASE_URL must be configured when M-Pesa payments are enabled.',
            id='payment.E001',
        ))
    elif not settings.DEBUG and not settings.MPESA_CALLBACK_BASE_URL.lower().startswith('https://'):
        errors.append(Error(
            'MPESA_CALLBACK_BASE_URL must use HTTPS in production.',
            id='payment.E002',
        ))

    environment = os.getenv('MPESA_ENVIRONMENT', '').strip().lower()
    required = [
        'MPESA_CONSUMER_KEY',
        'MPESA_CONSUMER_SECRET',
        'MPESA_PASSKEY',
        'MPESA_EXPRESS_SHORTCODE' if environment == 'sandbox' else 'MPESA_SHORTCODE',
    ]
    missing = [name for name in required if not os.getenv(name, '').strip()]
    if environment not in {'sandbox', 'production'}:
        missing.append('MPESA_ENVIRONMENT')
    if missing:
        errors.append(Error(
            f'M-Pesa configuration is incomplete: {", ".join(sorted(set(missing)))}.',
            id='payment.E003',
        ))
    return errors
