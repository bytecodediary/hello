from django.test import TestCase
from .models import CustomUser, Property, PropertyFeature, Owner, Image
# from rest_framework.test import APITestCase
from .serializers import PropertySerializer
from django.test.client import RequestFactory

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
        self.image = Image.objects.create(
            image='path/to/image.png',
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

    def test_property_creation(self):
        self.assertEqual(self.property.title, 'test name')
        self.assertEqual(self.property.status, 'available')

    def test_str(self):
        self.assertEqual(str(self.property), 'test name')

class PropertyFeatureTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='username',
            email='example@gmail.com',
            password='password'
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
        self.feature = PropertyFeature.objects.create(
            property=self.property,
            feature_value='1',
            feature_name='feature 1'
        )

    def test_feature_creation(self):
        self.assertEqual(self.feature.feature_name, 'feature 1')
        self.assertEqual(self.feature.feature_value, '1')

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
        self.image = Image.objects.create(
            image='image.png',
            image_alt='image alt'
        )
        self.owner = Owner.objects.create(
            email='owner@gmail.com',
            phone_number='+254700045555'
        )
        self.property = Property.objects.create(
            title='House 1',
            description="A great house",
            image=self.image,
            landlord=self.owner
        )

    def test_serializer_fields(self):
        serializer = PropertySerializer(instance=self.property)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'title', 'description', 'image', 'landlord'})

    def test_create_property(self):
        data = {
            'title': 'new place',
            'description': 'new description',
            'landlord': self.owner.id,
            'features': [{'feature_name': 'pool', 'feature_value': 1}],
            'images': [{'image_alt': 'front view', 'image': 'image_url'}],
        }
        serializer = PropertySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        property_instance = serializer.save()
        self.assertEqual(property_instance.title, 'new place')
        self.assertEqual(property_instance.features.count(), 1)
        self.assertEqual(property_instance.images.count(), 1)

    def test_invalid_create_data(self):
        invalid_data = {
            'title': '',
            'description': 'description',
            'landlord': self.owner.id,
            'features': [],
            'images': [{'image_alt': 'new image', 'image': 'image_url'}],
        }
        serializer = PropertySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
class PropertyUpdateTest(TestCase):
   
    def setUp(self):
        self.factory = RequestFactory()
        self.owner = Owner.objects.create(
                # property_id=1,
                # name = 'owner 1',
                phone_number = '+254700045555'
        )
        self.image = Image.objects.create(
            image='image.png', image_alt='property image'
        )
        self.property = property.objects.create(
            title='old title', description='old description', image=self.image, owner=self.owner,price=4000000
        )
        PropertyFeature.objects.create(property=self.property, feature_name='old feature', feature_value=1)
        self.properties_id =1
    
    def test_update_property(self):
        property_instance = Property.objects.create(title='old title', city='nakuru', address='123, westside', description='old description', price=4000000)

        PropertyFeature.objects.create(property=property_instance, feature_name='old feature', feature_value=1)
        Image.objects.create(property=property_instance, image_alt='old image', image='old image url')

        updated_data = {
            'title': 'new title',
            'description': 'new description',
            'price': 5000000,
            'city': 'nairobi',
            'owners': self.user,
            'address': '124, westside',
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