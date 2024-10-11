from django.contrib import admin
from .models import CustomUser, Property, Cart, CartItem, Payment, Transaction, Order, OrderItem, PropertyFeature, Owner, Image, Client

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'user_type')
    list_filter = ('user_type', 'date_joined', )
    search_fields = ('first_name', 'last_name', 'username')
    ordering = ('-date_joined',)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('title', 'city', 'price', 'address', 'listed_at', 'status')
    list_filter = ('status', 'city', 'price')
    search_fields = ('name', 'city', 'address')
    # prepopulated_fields = {'slug': ('name', 'city')}
    ordering = ('-updated_at',)
    
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


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('price', 'transaction_type', 'description', 'added_at')
    list_filter = ('transaction_type', 'price', 'added_at')
    search_fields = ('amount', 'added_at')
    ordering = ('-added_at',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'transaction_desc', 'date_paid')
    list_filter = ('user__username', 'payment__mode', 'date_paid')
    search_fields = ('user__username', 'payment__mode', 'date_paid')
    ordering = ('-date_paid',)


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


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Property, PropertyAdmin )
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PropertyFeature)
admin.site.register(Owner)
admin.site.register(Image)
admin.site.register(Client)