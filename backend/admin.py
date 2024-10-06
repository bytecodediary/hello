from django.contrib import admin
from .models import CustomUser, Property, Cart, CartItem, Payment, Transaction, Order, Order_Item, Property_Features, Property_Lord

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Property)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Payment)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(Property_Features)
admin.site.register(Property_Lord)