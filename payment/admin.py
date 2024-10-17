from django.contrib import admin
from .models import Payment, Transaction

# Register your models here.
admin.site.register(Payment)
admin.site.register(Transaction)