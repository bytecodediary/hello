from django.test import TestCase

from listing.models import Property
from user.models import CustomUser

from .models import Cart, CartItem, Order, OrderItem


class CartItemTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="example@gmail.com",
            password="password",
            username="username",
        )
        self.property = Property.objects.create(
            title="test name",
            description="test description",
            city="Nairobi",
            address="test address",
            price=100000,
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            property=self.property,
            quantity=3,
            cart=self.cart,
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.quantity, 3)
        self.assertEqual(self.cart_item.property.title, "test name")

    def test_cart_total(self):
        self.assertEqual(self.cart.total(), 300000)


class OrderItemTest(TestCase):
    def test_order_item_creation(self):
        user = CustomUser.objects.create_user(
            email="buyer@gmail.com",
            password="password",
            username="buyer",
        )
        property_instance = Property.objects.create(
            title="test name",
            description="test description",
            city="Nairobi",
            address="test address",
            price=100000,
        )
        order = Order.objects.create(user=user)
        item = OrderItem.objects.create(order=order, property=property_instance, quantity=1)

        self.assertEqual(item.property, property_instance)
        self.assertEqual(item.order, order)
