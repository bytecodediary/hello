from django.test import TestCase
from listing.models import CustomUser, Image, Property
from .models import CartItem

# Create your tests here.
class CartItemTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='example@gmail.com',
            password='password',
            username='username'
        )
        self.image = Image.objects.create(
            image='image.png',
            image_alt='test image alt'
        )
        self.property = Property.objects.create(
            title='test name',
            description='test description',
            city='location',
            status='available',
            image=self.image,
            landlord=self.user,
        )
        self.cart_item = CartItem.objects.create(
            property=self.property,
            quantity=3
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.quantity, 3)
        self.assertEqual(self.cart_item.property.landlord.email, 'example@gmail.com')

    def test_str(self):
        self.assertEqual(str(self.cart_item), f'CartItem for {self.cart_item.property.title}')

def OrderItemTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'example@gmail.com',
            password = 'password',
            username='username',
        )
        self.image = Image.objects.create(
            image = 'image.png',
            image_alt = 'test image alt'
        )
        self.property = Property.objects.create(
            title = 'test name',
            description = 'test description',
            city = 'location',
            status = 'available',
            image = self.image,
            landlord = self.user,
        )
