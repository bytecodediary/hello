from django.db import models
from listing.models import generate_unique_slug

class Payment(models.Model):
    PaymentModes = (
    ('bank', 'Bank'),
    ('mpesa', 'Mpesa'),
    ('paypal', 'Paypal'),
    ('stripe', 'stripe'),
    )

    order = models.ForeignKey("order.Order", on_delete=models.CASCADE, related_name='orders', default='')
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, related_name='user_payments')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    payment_mode = models.CharField(max_length=30, choices=PaymentModes, default='mpesa')
    description = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    property_paid_for = models.ForeignKey("listing.Property", on_delete=models.CASCADE, related_name="property_payments")

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
