from django.test import TestCase
from django.test import override_settings
from types import SimpleNamespace
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient

from listing.models import Property, PropertyOffer
from order.models import Order
from user.models import CustomUser

from .models import Payment, PaymentIntent, Transaction


class PaymentApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="payment-user",
            email="payment@example.com",
            password="password123",
        )
        self.property = Property.objects.create(
            title="Payment property",
            description="A property used to test payment visibility.",
            city="Nairobi",
            address="Kilimani",
            price=100000,
        )
        order = Order.objects.create(user=self.user)
        Payment.objects.create(
            user=self.user,
            order=order,
            property_paid_for=self.property,
            price=100000,
            payment_mode="mpesa",
            description="Test payment",
        )
        self.offer = PropertyOffer.objects.create(
            property=self.property,
            seeker=self.user,
            amount=1000,
            status="accepted",
        )

    def test_payment_and_transaction_records_are_read_only_until_gateway_is_configured(self):
        self.client.force_authenticate(self.user)

        payment_response = self.client.post(
            "/payment/",
            {"price": 10, "payment_mode": "mpesa", "description": "Forged payment"},
            format="json",
        )
        transaction_response = self.client.post(
            "/payment/transactions/",
            {"amount": 10, "transaction_desc": "Forged transaction", "payment": 1},
            format="json",
        )

        self.assertEqual(payment_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(transaction_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_can_only_read_their_own_payment_records(self):
        self.client.force_authenticate(self.user)

        response = self.client.get("/payment/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_payment_intent_requires_idempotency_key(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            "/payment/intents/",
            {"offer": self.offer.pk, "phone_number": "0712345678"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PaymentIntent.objects.count(), 0)

    def test_unconfigured_payment_provider_fails_closed_and_is_idempotent(self):
        self.client.force_authenticate(self.user)
        headers = {"HTTP_IDEMPOTENCY_KEY": "intent-001"}
        payload = {
            "offer": self.offer.pk,
            "phone_number": "0712345678",
        }

        response = self.client.post("/payment/intents/", payload, format="json", **headers)
        replay = self.client.post("/payment/intents/", payload, format="json", **headers)

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(replay.status_code, status.HTTP_200_OK)
        self.assertEqual(PaymentIntent.objects.count(), 1)
        self.assertEqual(PaymentIntent.objects.get().status, "failed")
        self.assertEqual(Payment.objects.count(), 1)

    def test_payment_intent_cannot_use_another_seeker_accepted_offer(self):
        other_user = CustomUser.objects.create_user(
            username="other-payment-user",
            email="other-payment@example.com",
            password="password123",
        )
        other_offer = PropertyOffer.objects.create(
            property=self.property,
            seeker=other_user,
            amount=1000,
            status="accepted",
        )
        self.client.force_authenticate(self.user)

        response = self.client.post(
            "/payment/intents/",
            {"offer": other_offer.pk, "phone_number": "0712345678"},
            format="json",
            HTTP_IDEMPOTENCY_KEY="intent-other-user",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(PaymentIntent.objects.filter(idempotency_key="intent-other-user").exists())

    @override_settings(
        PAYMENT_PROVIDER="mpesa",
        MPESA_CALLBACK_BASE_URL="https://payments.example.com",
    )
    @patch.dict(
        "os.environ",
        {
            "MPESA_ENVIRONMENT": "sandbox",
            "MPESA_CONSUMER_KEY": "consumer-key",
            "MPESA_CONSUMER_SECRET": "consumer-secret",
            "MPESA_PASSKEY": "passkey",
            "MPESA_EXPRESS_SHORTCODE": "174379",
        },
    )
    @patch("django_daraja.mpesa.core.MpesaClient")
    def test_configured_mpesa_provider_starts_processing_intent(self, client_class):
        client_class.return_value.stk_push.return_value = SimpleNamespace(
            response_code="0",
            checkout_request_id="ws_CO_123",
            merchant_request_id="29115-123",
        )
        self.client.force_authenticate(self.user)

        response = self.client.post(
            "/payment/intents/",
            {
                "offer": self.offer.pk,
                "phone_number": "0712345678",
            },
            format="json",
            HTTP_IDEMPOTENCY_KEY="intent-002",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        intent = PaymentIntent.objects.get(idempotency_key="intent-002")
        self.assertEqual(intent.status, "processing")
        self.assertEqual(intent.checkout_request_id, "ws_CO_123")
        client_class.return_value.stk_push.assert_called_once()

        replay_with_new_key = self.client.post(
            "/payment/intents/",
            {
                "offer": self.offer.pk,
                "phone_number": "0712345678",
            },
            format="json",
            HTTP_IDEMPOTENCY_KEY="intent-002-new-key",
        )
        self.assertEqual(replay_with_new_key.status_code, status.HTTP_200_OK)
        client_class.return_value.stk_push.assert_called_once()

    def test_mpesa_success_callback_reconciles_once(self):
        intent = PaymentIntent.objects.create(
            user=self.user,
            property_paid_for=self.property,
            offer=self.offer,
            amount=1000,
            phone_number="0712345678",
            idempotency_key="intent-003",
            status="processing",
            checkout_request_id="ws_CO_123",
        )
        payload = {
            "Body": {
                "stkCallback": {
                    "ResultCode": 0,
                    "ResultDesc": "The service request is processed successfully.",
                    "CallbackMetadata": {
                        "Item": [{"Name": "MpesaReceiptNumber", "Value": "ABC123"}]
                    },
                }
            }
        }

        response = self.client.post(
            f"/payment/callback/mpesa/{intent.callback_token}/",
            payload,
            format="json",
        )
        replay = self.client.post(
            f"/payment/callback/mpesa/{intent.callback_token}/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(replay.status_code, status.HTTP_200_OK)
        intent.refresh_from_db()
        self.assertEqual(intent.status, "succeeded")
        self.assertEqual(intent.provider_reference, "ABC123")
        self.assertEqual(Payment.objects.filter(payment_intent=intent).count(), 1)
        self.assertEqual(Transaction.objects.filter(payment__payment_intent=intent).count(), 1)

    def test_mpesa_callback_rejects_malformed_payload(self):
        intent = PaymentIntent.objects.create(
            user=self.user,
            property_paid_for=self.property,
            offer=self.offer,
            amount=1000,
            phone_number="0712345678",
            idempotency_key="intent-004",
            status="processing",
        )

        response = self.client.post(
            f"/payment/callback/mpesa/{intent.callback_token}/",
            {"unexpected": "payload"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        intent.refresh_from_db()
        self.assertEqual(intent.status, "processing")
