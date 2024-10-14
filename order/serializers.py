from rest_framework import serializers
from .models import Order, OrderItem
from user.serializers import CustomUserSerializer
from .models import Cart, CartItem

class OrderItemSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    property_name = serializers.CharField(source="property.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['slug', 'quantity', 'property_name']

class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemSerializer(source="order_items" ,many=True, read_only=True)
    slug = serializers.SlugField()
    user = CustomUserSerializer(source="order", read_only=True)

    class Meta:
        model = Order
        fields = ['slug', 'user', 'created_at', 'updated_at']

class CartItemSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source="property.title", read_only=True)
    slug = serializers.SlugField()

    class Meta:
        model = CartItem
        fields = ['slug', 'property_name', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = CustomUserSerializer()
    slug =serializers.SlugField()
   
    class Meta:
        model = Cart
        fields = ['slug', 'total_price', 'items', 'user']
    
    def get_total_price(self, obj):
        total = sum(item.quantity * item.property.price for item in obj.items.all())
        return total
