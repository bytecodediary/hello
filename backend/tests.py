from django.test import TestCase
from .models import CustomUser, Property, PropertyFeature, Cart, CartItem, Order, OrderItem, Owner, Agent, Transaction, Payment, Client, Image
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .serializers import PropertySerializer

# Create your tests here.
class customuser_test(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='username',
            email = 'email@gmail.com',
            password = 'password',
        )
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'email@gmail.com')
        self.assertequal(self.user.password, 'password')
        self.assertEqual(self.user.username, 'username')
    
class property_test(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'example@gmail.com',
            password = 'password'
        )
        self.image = Image.objects.create(
            image = '/home/trent22/hello/hello/backend/rental_system.png',
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
        property_id = property.id
        self.assertEqual(self.property.title, 'test name')
        self.assertEqual(self.property.status, 'available')
        
    def test_str(self):
        self.assertEqual(self.property.title, 'test name')

class Property_Features_test(TestCase):
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
        self.features = Property_Features.objects.create(
            property = self.features,
            feature_value = '1',
            feature_name = 'feature 1'
        )

        def feature_addtion_test(self):
            self.assertEqual(self.features.feature_name, 'feature 1')
            self.assertEqqual(self.features.feature_value, 1) 
        
        def feature_str_test(self):
            self.asserrtEqual(self.features.feature_name, 'feature 1')
class CartItemTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'example@gmail.com',
            password = 'password',
            username = 'username'
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
        self.cartitem = CartItem.objects.create(
            property = self.property,
            quantity = 3
        )
        def cart_item_creation_test(self):
            self.assertEqual(self.cartitem.quantity, 3)
            self.assertEqual(self.assertEqual.property.landlord.email, 'example@gmail.com')

        def str_test(self):
            self.assertEqual(self.cartitem.property.landlord.username, 'username')

def OrderItemTests(TestCase):
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

class property_feature_test(TestCase):
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
            title ='test name',
            description = 'test description',
            city = 'location',
            status = 'available',
            image = self.image,
            landlord = self.user,
        )
        
        self.features = PropertyFeature.objects.create(
            property = self.property,
            property_name = 'test name',
            property_value = '3'
        )

    def feature_addition_test(self):
        self.assertEqual(self.features.property.title, 'test name')
        self.assertEqual(self.features.proprty_name, 'test name')
        self.assertEqual(self.property.property_value, '3')
    
    def feature_str_test(self):
        self.assertEqual(self.features.property_name, 'test name')

class PropertySerializerTest(TestCase):
    def setUp(self):
        self.image = Image.objects.create(
            image = 'image.png',
            image_alt = '/home/trent22/hello/hello/backend/rental_system.png'
        )

        self.owner = Owner.objects.create(
            email = 'owner@gmail.com',
            phone_number = '+254700045555'
        )

        self.property = Property.objects.create(
            title = 'House 1',
            description = "A great house",
            price = 5000000,
            image = self.image,
            features = self.features,
            owner = self.owner
        )

    def test_serializeer_fields(self):
        serializer = PropertySerializer(instance=self.instance)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['title', 'description', 'price', 'image', 'features', 'owner']))
        
    def test_create_property(self):
        data = {
            'title': 'new place',
            'description': 'new description',
            'price' : 4000000,
            'owner': self.owner.id,
            'features': [{'feature_name': 'pool', 'feature_value': 1}],
            'images': [{'image_alt': 'front view', 'image': 'image_url'}],
        }
        property_id = self.property.id
        serializer = PropertySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        property_instance = serializer.save()
        self.assertEqual(property_instance.title, 'new place')
        self.assertEqual(property_instance.features.count(), 1),
        self.assertEqual(property_instance.images.count(), 1)

    def invalid_create_data_test(self):
        invalid_data = {
            'title': '',
            'description': 'description',
            'price': 'invalid_price',
            'owner': self.owner.id,
            'features': [],
            'image':[{'image_alt': 'new image', 'image':'image_url'}]
        }
        serializer =PropertySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('price', serializer.errors)
        # self.assertIn('features', serializer.errors)
class PropertyUpdateTest(TestCase):
   
    # def setUp(self):
    #     self.owner = Owner.objects.create(
    #             name = 'owner 1',
    #             phone_number = '+254700045555'
    #     )
    #     self.image = Image.objects.create(
    #         image='/home/trent22/hello/hello/backend/rental_system.png', image_alt='property image'
    #     )
    #     self.property = property.objects.create(
    #         title='old title', description='old description', image=self.image, owner=self.owner,price=4000000
    #     )
    #     PropertyFeature.objects.create(property=self.property, feature_name='old feature', feature_value=1)

    
    def test_update_property(self):
        property_instance = Property.objects.create(title='old title', description='old description', price=4000000)

        PropertyFeature.objects.create(property=property_instance, feature_name='old feature', feature_value=1)
        Image.objects.create(property=property_instance, image_alt='old image', image='old image url')

        updated_data = {
            'title': 'new title',
            'description': 'new description',
            'price': 5000000,
            
            'features': [{'feature_name': 'updated pool', 'feature_value': 2}],
            'images': [{'image_alt': 'updated image rear', 'image': 'updated_image_url'}]
        }

        serializer = PropertySerializer(property_instance, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_instance = serializer.save()

        self.assertEqual(updated_instance.title, 'new title')
        self.assertEqual(updated_instance.description, 'new description')
        self.assertEqual(updated_instance.price, 5000000)

        self.assertEqual(updated_instance.property_features.count(), 1)
        self.assertEqual(updated_instance.images.count(), 1)

        feature = updated_instance.property_features.first()
        self.assertEqual(feature.feature_name, 'updated pool')

        image = updated_instance.images.first()
        self.assertEqual(image.image_alt, 'updated image rear')
        self.assertEqual(image.image, 'updated_image_url')

    def test_invalid_update_data(self):
        invalid_data = {
            'title': '',
            'description': 'invalid description',
            'price': 'invalid price',
            'features': [{'feature_name': 'pool', 'feature_value': 1}],
            'images': [{'image_alt':'image update', 'image': 'image_url_update_invalid'}],
        }

        serializer = PropertySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
        self.assertIn('title', serializer.errors)