from django.contrib import admin
from .models import Payment, PaymentIntent, Transaction

# Register your models here.
admin.site.register(Payment)
admin.site.register(PaymentIntent)
admin.site.register(Transaction)
