from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from listing.models import Property
from order.models import Order
from user.models import CustomUser

from .models import Payment


class PaymentApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="payment-user",
            email="payment@example.com",
            password="password123",
        )
        property_instance = Property.objects.create(
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
            property_paid_for=property_instance,
            price=100000,
            payment_mode="mpesa",
            description="Test payment",
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
