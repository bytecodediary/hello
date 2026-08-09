import os
from decimal import Decimal
from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse


class PaymentGatewayError(Exception):
    """A safe, user-facing payment gateway failure."""


class PaymentProviderNotConfigured(PaymentGatewayError):
    """Raised when live payment credentials or callback configuration is absent."""


def _required_mpesa_environment():
    environment = os.getenv('MPESA_ENVIRONMENT', '').strip().lower()
    required = {
        'MPESA_ENVIRONMENT': environment,
        'MPESA_CONSUMER_KEY': os.getenv('MPESA_CONSUMER_KEY', '').strip(),
        'MPESA_CONSUMER_SECRET': os.getenv('MPESA_CONSUMER_SECRET', '').strip(),
        'MPESA_PASSKEY': os.getenv('MPESA_PASSKEY', '').strip(),
    }
    shortcode_key = 'MPESA_EXPRESS_SHORTCODE' if environment == 'sandbox' else 'MPESA_SHORTCODE'
    required[shortcode_key] = os.getenv(shortcode_key, '').strip()
    missing = [key for key, value in required.items() if not value]
    if environment not in {'sandbox', 'production'}:
        missing.append('MPESA_ENVIRONMENT (sandbox or production)')
    if missing:
        missing_labels = ', '.join(sorted(set(missing)))
        raise PaymentProviderNotConfigured(
            f'M-Pesa is not configured. Missing: {missing_labels}.'
        )


def _callback_url(intent):
    base_url = settings.MPESA_CALLBACK_BASE_URL
    if not base_url:
        raise PaymentProviderNotConfigured('MPESA_CALLBACK_BASE_URL must be configured.')
    if not settings.DEBUG and not base_url.lower().startswith('https://'):
        raise PaymentProviderNotConfigured('MPESA_CALLBACK_BASE_URL must use HTTPS in production.')
    return urljoin(
        f'{base_url}/',
        reverse('mpesa-callback', kwargs={'token': intent.callback_token}).lstrip('/'),
    )


class MpesaPaymentGateway:
    def start(self, intent):
        _required_mpesa_environment()
        if intent.currency != 'KES':
            raise PaymentGatewayError('M-Pesa payments must use KES.')

        amount = Decimal(intent.amount)
        if amount != amount.to_integral_value():
            raise PaymentGatewayError('M-Pesa payments must be whole KES amounts.')

        try:
            from django_daraja.mpesa.core import MpesaClient

            response = MpesaClient().stk_push(
                intent.phone_number,
                int(amount),
                f'PI{str(intent.id).replace("-", "")[:10]}',
                'Nyumba property payment',
                _callback_url(intent),
            )
        except PaymentGatewayError:
            raise
        except Exception as exc:
            raise PaymentGatewayError('The payment provider could not be reached.') from exc

        response_code = str(getattr(response, 'response_code', '') or '')
        checkout_request_id = str(getattr(response, 'checkout_request_id', '') or '')
        merchant_request_id = str(getattr(response, 'merchant_request_id', '') or '')
        if response_code != '0' or not checkout_request_id:
            description = getattr(response, 'response_description', '') or getattr(
                response,
                'error_message',
                '',
            )
            raise PaymentGatewayError(description or 'The payment provider rejected the request.')

        return {
            'status': 'processing',
            'checkout_request_id': checkout_request_id[:100],
            'merchant_request_id': merchant_request_id[:100],
        }


def get_payment_gateway():
    if settings.PAYMENT_PROVIDER == 'mpesa':
        return MpesaPaymentGateway()
    raise PaymentProviderNotConfigured(
        'Payments are not enabled. Configure PAYMENT_PROVIDER=mpesa and the M-Pesa credentials.'
    )
