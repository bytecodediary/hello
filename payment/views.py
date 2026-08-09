from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .models import Payment, PaymentIntent, Transaction
from .serializers import PaymentIntentSerializer, PaymentSerializer, TransactionSerializer
from .services import PaymentGatewayError, get_payment_gateway


class PaymentIntentView(generics.ListCreateAPIView):
    serializer_class = PaymentIntentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentIntent.objects.filter(user=self.request.user).select_related('property_paid_for')

    def create(self, request, *args, **kwargs):
        idempotency_key = request.headers.get('Idempotency-Key', '').strip()
        if not idempotency_key:
            return Response(
                {'detail': 'Idempotency-Key is required for payment requests.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(idempotency_key) > 128:
            return Response(
                {'detail': 'Idempotency-Key must be 128 characters or fewer.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing = self.get_queryset().filter(idempotency_key=idempotency_key).first()
        if existing:
            return Response(self.get_serializer(existing).data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer = serializer.validated_data['offer']
        if offer.seeker_id != request.user.id:
            return Response(
                {'detail': 'You can only pay for your own accepted offer.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if offer.amount != offer.amount.to_integral_value():
            return Response(
                {'detail': 'M-Pesa payments must be whole KES amounts.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        active_intent = self.get_queryset().filter(
            offer=offer,
            status__in=('pending', 'processing', 'succeeded'),
        ).first()
        if active_intent:
            return Response(self.get_serializer(active_intent).data, status=status.HTTP_200_OK)
        try:
            intent = serializer.save(
                user=request.user,
                idempotency_key=idempotency_key,
                property_paid_for=offer.property,
                amount=offer.amount,
                currency=offer.currency,
                payment_mode='mpesa',
            )
        except IntegrityError:
            intent = self.get_queryset().filter(idempotency_key=idempotency_key).first()
            if intent:
                return Response(self.get_serializer(intent).data, status=status.HTTP_200_OK)
            active_intent = self.get_queryset().filter(
                offer=offer,
                status__in=('pending', 'processing', 'succeeded'),
            ).first()
            if active_intent:
                return Response(self.get_serializer(active_intent).data, status=status.HTTP_200_OK)
            raise

        try:
            provider_result = get_payment_gateway().start(intent)
        except PaymentGatewayError as exc:
            intent.status = 'failed'
            intent.failure_reason = str(exc)[:255]
            intent.save(update_fields=['status', 'failure_reason', 'updated_at'])
            return Response(
                {'detail': str(exc), 'payment_intent': self.get_serializer(intent).data},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        intent.status = provider_result['status']
        intent.checkout_request_id = provider_result['checkout_request_id']
        intent.merchant_request_id = provider_result['merchant_request_id']
        intent.save(update_fields=[
            'status', 'checkout_request_id', 'merchant_request_id', 'updated_at',
        ])
        return Response(self.get_serializer(intent).data, status=status.HTTP_201_CREATED)


class PaymentView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Payment.objects.filter(user=self.request.user)
            .select_related("user", "order", "property_paid_for")
            .prefetch_related("transactions")
            .order_by("-added_at")
        )

class TransactionView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Transaction.objects.filter(payment__user=self.request.user)
            .select_related("payment", "payment__user", "payment__property_paid_for")
            .order_by("-date_paid")
        )


@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def mpesa_callback(request, token):
    with transaction.atomic():
        intent = get_object_or_404(
            PaymentIntent.objects.select_for_update(),
            callback_token=token,
        )
        if intent.status == 'succeeded':
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

        payload = request.data
        callback = payload.get('Body', {}).get('stkCallback', {})
        if not isinstance(callback, dict) or 'ResultCode' not in callback:
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid callback payload'}, status=400)

        intent.callback_payload = payload
        result_code = str(callback.get('ResultCode'))
        if result_code != '0':
            intent.status = 'failed'
            intent.failure_reason = str(callback.get('ResultDesc', 'Payment failed'))[:255]
            intent.save(update_fields=['status', 'failure_reason', 'callback_payload', 'updated_at'])
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

        metadata_payload = callback.get('CallbackMetadata') or {}
        metadata = {
            item.get('Name'): item.get('Value')
            for item in metadata_payload.get('Item', [])
            if isinstance(item, dict) and item.get('Name')
        }
        payment, _ = Payment.objects.get_or_create(
            payment_intent=intent,
            defaults={
                'order': intent.order,
                'user': intent.user,
                'price': intent.amount,
                'payment_mode': intent.payment_mode,
                'description': f'Payment for {intent.property_paid_for.title}'[:255],
                'property_paid_for': intent.property_paid_for,
            },
        )
        Transaction.objects.get_or_create(
            payment=payment,
            transaction_type='payment',
            defaults={
                'amount': int(intent.amount),
                'transaction_desc': 'M-Pesa property payment',
                'status': 'paid',
            },
        )
        intent.status = 'succeeded'
        intent.provider_reference = str(metadata.get('MpesaReceiptNumber', ''))[:100]
        intent.failure_reason = ''
        intent.save(update_fields=[
            'status', 'provider_reference', 'failure_reason', 'callback_payload', 'updated_at',
        ])

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
