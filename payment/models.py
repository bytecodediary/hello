import uuid

from django.db import models
from django.db.models import Q
from listing.models import generate_unique_slug


class PaymentIntent(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_MODES = (
        ('mpesa', 'Mpesa'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.CASCADE,
        related_name='payment_intents',
    )
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payment_intents',
    )
    property_paid_for = models.ForeignKey(
        'listing.Property',
        on_delete=models.PROTECT,
        related_name='payment_intents',
    )
    offer = models.ForeignKey(
        'listing.PropertyOffer',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='payment_intents',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    payment_mode = models.CharField(max_length=30, choices=PAYMENT_MODES, default='mpesa')
    phone_number = models.CharField(max_length=32)
    idempotency_key = models.CharField(max_length=128)
    callback_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    merchant_request_id = models.CharField(max_length=100, blank=True)
    checkout_request_id = models.CharField(max_length=100, blank=True)
    provider_reference = models.CharField(max_length=100, blank=True)
    failure_reason = models.CharField(max_length=255, blank=True)
    callback_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'idempotency_key'],
                name='unique_payment_intent_idempotency',
            ),
            models.UniqueConstraint(
                fields=['offer'],
                condition=Q(status__in=('pending', 'processing', 'succeeded')),
                name='one_active_payment_intent_per_offer',
            ),
        ]
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['checkout_request_id']),
        ]


class Payment(models.Model):
    PaymentModes = (
    ('bank', 'Bank'),
    ('mpesa', 'Mpesa'),
    ('paypal', 'Paypal'),
    ('stripe', 'stripe'),
    )

    order = models.ForeignKey(
        "order.Order",
        on_delete=models.SET_NULL,
        related_name='payments',
        null=True,
        blank=True,
    )
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, related_name='user_payments')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    payment_mode = models.CharField(max_length=30, choices=PaymentModes, default='mpesa')
    description = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    property_paid_for = models.ForeignKey(
        "listing.Property",
        on_delete=models.CASCADE,
        related_name="property_payments",
    )
    payment_intent = models.OneToOneField(
        PaymentIntent,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='payment',
    )

    def __str__(self):
        return f"{self.payment_mode} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

class Transaction(models.Model):
    Status_Types = (
        ('paid', 'paid'),
        ('refunded', 'refunded'),
        ('failed', 'failed'),
        ('unsettled', 'unsettled')
    )

    TRANSACTION_TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('authorization', 'Authorization'),
        ('chargeback', 'Chargeback'),
        ('adjustment', 'Adjustment'),
        ('payout', 'Payout'),
    ]

    amount = models.IntegerField(default=0)
    date_paid = models.DateTimeField(auto_now=True)
    transaction_desc = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="transactions")
    status = models.CharField(max_length=50, choices=Status_Types, default='unsettled')
    transaction_type = models.CharField(max_length=200, choices=TRANSACTION_TYPE_CHOICES, default='')

    def __str__(self):
        return f"transaction for {self.payment.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)
