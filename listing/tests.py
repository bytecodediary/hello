from django.test import TestCase
from user.models import CustomUser, Owner
from .models import Property, PropertyFeature, Image, Notification
# from rest_framework.test import APITestCase
from .serializers import PropertySerializer
from django.test.client import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class CustomUserTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='username',
            email='email@gmail.com',
            password='password'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'email@gmail.com')
        self.assertNotEqual(self.user.password, 'password')  # Password should be hashed
        self.assertEqual(self.user.username, 'username')
class PropertyTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='username',
            email='example@gmail.com',
            password='password'
        )
        self.property = Property.objects.create(
            title='test name',
            description='test description',
            city='location',
            status='available',
            address='test address',
            price=100000,
            stock=1,
        )
        self.image = Image.objects.create(
            image='path/to/image.png',
            image_alt='test image alt',
            property=self.property,
        )

    def test_property_creation(self):
        self.assertEqual(self.property.title, 'test name')
        self.assertEqual(self.property.status, 'available')

    def test_str(self):
        self.assertEqual(str(self.property), 'test name')

class PropertyFeatureTest(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            title='test name',
            description='test description',
            city='location',
            address='test address',
            price=100000,
        )
        self.feature = PropertyFeature.objects.create(
            property=self.property,
            feature_value=1,
            feature_name='feature 1'
        )

    def test_feature_creation(self):
        self.assertEqual(self.feature.feature_name, 'feature 1')
        self.assertEqual(self.feature.feature_value, 1)

    def test_str(self):
        self.assertEqual(str(self.feature), 'feature 1')

# class property_feature_test(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create(
#             email = 'example@gmail.com',
#             password = 'password',
#             username='username',
#         )

#         self.image = Image.objects.create(
#             image = 'image.png',
#             image_alt = 'test image alt'
#         )

#         self.property = Property.objects.create(
#             title ='test name',
#             description = 'test description',
#             city = 'location',
#             status = 'available',
#             image = self.image,
#             landlord = self.user,
#         )
        
#         self.features = PropertyFeature.objects.create(
#             property = self.property,
#             property_name = 'test name',
#             property_value = '3'
#         )

#     def feature_addition_test(self):
#         self.assertEqual(self.features.property.title, 'test name')
#         self.assertEqual(self.features.proprty_name, 'test name')
#         self.assertEqual(self.property.property_value, '3')
    
#     def feature_str_test(self):
#         self.assertEqual(self.features.property_name, 'test name')

class PropertySerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='owner',
            email='owner@gmail.com',
            password='password'
        )
        self.property = Property.objects.create(
            title='House 1',
            description="A great house",
            city='Nairobi',
            address='123 Main St',
            price=500000,
        )
        self.owner = Owner.objects.create(
            owner=self.user,
            properties=self.property,
            phone_number='+254700045555'
        )
        self.image = Image.objects.create(
            image='image.png',
            image_alt='image alt',
            property=self.property
        )

        PropertyFeature.objects.create(
            property=self.property,
            feature_name='pool',
            feature_value=5
        )

    def test_serializer_fields(self):
        serializer = PropertySerializer(instance=self.property)
        data = serializer.data
        expected_fields = {'slug', 'title', 'owners', 'description', 'price', 'images', 'city', 'address', 'listed_at', 'updated_at', 'features'}
        self.assertEqual(set(data.keys()), expected_fields)

    def test_create_property(self):
        data = {
            'title': 'new place',
            'description': 'new description',
            'price': 300000,
            'city': 'Nairobi',
            'address': '456 Elm St',
            'features': [{'feature_name': 'pool', 'feature_value': 1}],
            'images': [],
        }
        serializer = PropertySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        property_instance = serializer.save()
        self.assertEqual(property_instance.title, 'new place')
        self.assertEqual(property_instance.features.count(), 1)
        self.assertEqual(property_instance.images.count(), 0)

    def test_invalid_create_data(self):
        invalid_data = {
            'title': '',
            'description': 'description',
            'price': 200000,
            'city': 'Nairobi',
            'address': '789 Oak St',
            'features': [],
            'images': [],
        }
        serializer = PropertySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
class PropertyUpdateTest(TestCase):
   
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='updater',
            email='updater@gmail.com',
            password='password'
        )
        self.property = Property.objects.create(
            title='old title',
            description='old description',
            city='nakuru',
            address='123, westside',
            price=4000000,
        )
        self.owner = Owner.objects.create(
            owner=self.user,
            properties=self.property,
            phone_number='+254700045555'
        )
        PropertyFeature.objects.create(property=self.property, feature_name='old feature', feature_value=1)
        Image.objects.create(property=self.property, image_alt='old image', image='old image url')
    
    def test_update_property(self):
        updated_data = {
            'slug': self.property.slug,
            'title': 'new title',
            'description': 'new description',
            'price': 5000000,
            'city': 'nairobi',
            'address': '124, westside',
            'features': [{'feature_name': 'updated pool', 'feature_value': 2}],
            'images': [],
        }

        serializer = PropertySerializer(self.property, data=updated_data)
        
        self.assertTrue(serializer.is_valid())
        updated_instance = serializer.save()

        self.assertEqual(updated_instance.title, 'new title')
        self.assertEqual(updated_instance.description, 'new description')
        self.assertEqual(updated_instance.price, 5000000)

        self.assertEqual(updated_instance.features.count(), 1)
        self.assertEqual(updated_instance.images.count(), 0)

        feature = updated_instance.features.first()
        self.assertEqual(feature.feature_name, 'updated pool')

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