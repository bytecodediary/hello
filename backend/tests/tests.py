from django.test import TestCase
from .models import CustomUser, Property, Property_Features, Cart, CartItem, Order, Order_Item, Property_Lord, Agent, Transaction, Payment, client, Image

# Create your tests here.
class customuser_test(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'email@gmail.com',
            password = 'password',
        )
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'email@gmail.com')
        self.assertequal(self.user.password, 'password')
    
class property_test(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'example@gmail.com',
            password = 'password'
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

    def test_property_creation(self):
        self.assertEqual(self.property.title, 'test name')
        self.assertEqual(self.property.status, 'available')
        self.assertEqual(self.property.landlord.email, 'example.gmail.com')
        
    def test_str(self):
        self.assertEqual(self.property.title, 'test name')

class property_feature_test(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'example@gmail.com',
            password = 'password'
        )

        self.property = Property.objects.create(
            title ='test name',

        )