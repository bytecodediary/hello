from rest_framework import serializers
from listing.models import Property
from .models import Order, OrderItem, Cart, CartItem


class OrderItemSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())
    property_name = serializers.CharField(source="property.title", read_only=True)
    price_each = serializers.IntegerField(source="property.price", read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['slug', 'property', 'property_name', 'price_each', 'quantity', 'line_total']
        read_only_fields = ['slug', 'property_name', 'price_each', 'line_total']

    def get_line_total(self, obj):
        return obj.quantity * obj.property.price


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source="order_items", many=True, read_only=True)
    total = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['slug', 'status', 'created_at', 'updated_at', 'items', 'total']
        read_only_fields = ['slug', 'status', 'created_at', 'updated_at', 'items', 'total']

    def get_total(self, obj):
        return sum(item.quantity * item.property.price for item in obj.order_items.all())


class CartItemSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())
    property_name = serializers.CharField(source="property.title", read_only=True)
    property_price = serializers.IntegerField(source="property.price", read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['slug', 'property', 'property_name', 'property_price', 'quantity', 'line_total']
        read_only_fields = ['slug', 'property_name', 'property_price', 'line_total']

    def get_line_total(self, obj):
        return obj.quantity * obj.property.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="order_items", many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['slug', 'total_price', 'items']
        read_only_fields = ['slug', 'total_price', 'items']

    def get_total_price(self, obj):
        return sum(item.quantity * item.property.price for item in obj.order_items.all())
