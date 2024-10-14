from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    ordering = ('-created_at',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('property', 'quantity')
    list_filter = ('property__title', 'quantity')
    search_fields = ('property__title', 'quantity')
    ordering = ('-property__title',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',  'status', 'created_at') #'payment'
    list_filter = ('user__username', 'status', 'created_at') #'payment__mode'
    search_fields = ('user__username',  'status', 'created_at') #'payment__mode'
    ordering = ('-created_at',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'property', 'quantity')
    list_filter = ( 'property__title', 'quantity') #'order__name',
    search_fields = ( 'property__title', 'quantity') #'order__name',
    ordering = ('-property__title',)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)