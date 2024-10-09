from django.contrib import admin
from .models import CustomUser, Property, Cart, CartItem, Payment, Transaction, Order, OrderItem, Property_Features, Property_Lord, Image, Client

# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email', 'username', 'user_type')
#     list_filter = ('user_type',)
#     search_fields = ('first_name', 'last_name', 'email', 'username')
#     ordering = ('-date_joined',)


# class PropertyAdmin(admin.ModelAdmin):
#     list_display = ('name', 'city', 'address', 'updated_at', 'status')
#     list_filter = ('status', 'city')
#     search_fields = ('name', 'city', 'address')
#     prepopulated_fields = {'slug': ('name', 'city')}
#     ordering = ('-updated_at',)


# class CartAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_at')
#     list_filter = ('created_at',)
#     search_fields = ('user__username',)
#     ordering = ('-created_at',)


# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('property', 'quantity')
#     list_filter = ('property__name', 'quantity')
#     search_fields = ('property__name', 'quantity')
#     ordering = ('-property__name',)


# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('mode', 'amount', 'created_at')
#     list_filter = ('mode', 'created_at')
#     search_fields = ('amount', 'created_at')
#     ordering = ('-created_at',)


# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'payment', 'order', 'created_at')
#     list_filter = ('user__username', 'payment__mode', 'order__name', 'created_at')
#     search_fields = ('user__username', 'payment__mode', 'order__name', 'created_at')
#     ordering = ('-created_at',)


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('name', 'user', 'payment', 'status', 'created_at')
#     list_filter = ('name', 'user__username', 'payment__mode', 'status', 'created_at')
#     search_fields = ('name', 'user__username', 'payment__mode', 'status', 'created_at')
#     ordering = ('-created_at',)


# class Order_ItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'property', 'quantity')
#     list_filter = ('order__name', 'property__name', 'quantity')
#     search_fields = ('order__name', 'property__name', 'quantity')
#     ordering = ('-order__name',)


# class Property_FeaturesAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     list_filter = ('name', 'description')
#     search_fields = ('name', 'description')
#     ordering = ('-name',)


# class Property_LordAdmin(admin.ModelAdmin):
#     list_display = ('name', 'phone_number')
#     list_filter = ('name', 'phone_number')
#     search_fields = ('name', 'phone_number')
#     ordering = ('-name',)


admin.site.register(CustomUser)
admin.site.register(Property )
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Payment)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Property_Features)
admin.site.register(Property_Lord)
admin.site.register(Image)
admin.site.register(Client)