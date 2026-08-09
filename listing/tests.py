from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import CustomUser, Owner
from .models import Notification, Property, PropertyFeature, Image, PropertyOffer
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
        expected_fields = {
            'slug', 'title', 'owners', 'description', 'price', 'currency',
            'listing_type', 'property_type', 'status', 'moderation_status',
            'bedrooms', 'bathrooms', 'area_sqm', 'city', 'county',
            'neighborhood', 'address', 'listed_at', 'updated_at', 'images',
            'features', 'created_by_name', 'is_featured',
        }
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


class PropertyPermissionsApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = CustomUser.objects.create_user(
            username="customer", email="customer@example.com", password="password"
        )
        self.provider = CustomUser.objects.create_user(
            username="provider", email="provider@example.com", password="password",
            user_type="landlord", provider_status="approved",
        )
        self.other_provider = CustomUser.objects.create_user(
            username="other-provider", email="other@example.com", password="password",
            user_type="agent", provider_status="approved",
        )
        self.property = Property.objects.create(
            title="Published home",
            description="A published home",
            city="Nairobi",
            address="Westlands",
            price=500000,
            created_by=self.provider,
            moderation_status="published",
        )

    def test_anonymous_user_can_browse_published_listings(self):
        response = self.client.get("/api/v1/listings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], self.property.slug)

    def test_unapproved_user_cannot_access_provider_workspace(self):
        self.client.force_authenticate(self.customer)
        response = self.client.get("/api/v1/provider/listings/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_create_listing(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post("/api/v1/listings/", {
            "title": "Unauthorized listing",
            "description": "Should not be accepted",
            "city": "Nairobi",
            "address": "Kilimani",
            "price": 200000,
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approved_provider_creates_pending_listing(self):
        self.client.force_authenticate(self.provider)
        response = self.client.post("/api/v1/listings/", {
            "title": "New listing",
            "description": "A new provider listing",
            "city": "Nairobi",
            "address": "Kilimani",
            "price": 200000,
            "listing_type": "rent",
            "property_type": "apartment",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Property.objects.get(slug=response.data["slug"])
        self.assertEqual(created.created_by, self.provider)
        self.assertEqual(created.moderation_status, "pending_review")

    def test_provider_cannot_modify_another_providers_listing(self):
        self.client.force_authenticate(self.other_provider)
        response = self.client.patch(
            f"/api/v1/listings/{self.property.slug}/",
            {"title": "Tampered listing"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.property.refresh_from_db()
        self.assertEqual(self.property.title, "Published home")

    def test_authenticated_seeker_can_save_and_remove_listing(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post(f"/api/v1/listings/{self.property.slug}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.get("/api/v1/favorites/").data["count"], 1)

        response = self.client.delete(f"/api/v1/listings/{self.property.slug}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_seeker_can_submit_inquiry(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post(
            f"/api/v1/listings/{self.property.slug}/inquiries/",
            {"inquiry_type": "inquiry", "message": "Could I learn more about this home?"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.property.inquiries.count(), 1)
        self.assertEqual(Notification.objects.filter(user=self.provider).count(), 1)

    def test_provider_can_update_inquiry_and_notify_seeker(self):
        self.client.force_authenticate(self.customer)
        inquiry_response = self.client.post(
            f"/api/v1/listings/{self.property.slug}/inquiries/",
            {"inquiry_type": "inquiry", "message": "Please share viewing times."},
            format="json",
        )
        inquiry_id = inquiry_response.data["id"]

        self.client.force_authenticate(self.provider)
        response = self.client.patch(
            f"/api/v1/provider/inquiries/{inquiry_id}/",
            {"status": "contacted", "provider_response": "I can help this afternoon."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "contacted")
        self.assertEqual(Notification.objects.filter(user=self.customer).count(), 1)

    def test_seeker_can_submit_offer_and_provider_can_accept_it(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post(
            f"/api/v1/listings/{self.property.slug}/offers/",
            {
                "offer_type": "offer",
                "amount": "450000.00",
                "message": "I would like to proceed with this property.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        offer = PropertyOffer.objects.get(pk=response.data["id"])
        self.assertEqual(offer.provider, self.provider)
        self.assertEqual(Notification.objects.filter(user=self.provider).count(), 1)

        self.client.force_authenticate(self.provider)
        response = self.client.patch(
            f"/api/v1/provider/offers/{offer.pk}/",
            {"status": "accepted", "provider_response": "Offer accepted."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        offer.refresh_from_db()
        self.assertEqual(offer.status, "accepted")
        self.assertEqual(Notification.objects.filter(user=self.customer).count(), 1)

    def test_provider_cannot_accept_two_offers_for_one_listing(self):
        first = PropertyOffer.objects.create(
            property=self.property,
            seeker=self.customer,
            provider=self.provider,
            amount=400000,
            status="accepted",
        )
        second = PropertyOffer.objects.create(
            property=self.property,
            seeker=self.other_provider,
            provider=self.provider,
            amount=410000,
        )

        self.client.force_authenticate(self.provider)
        response = self.client.patch(
            f"/api/v1/provider/offers/{second.pk}/",
            {"status": "accepted"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        second.refresh_from_db()
        self.assertEqual(second.status, "submitted")
        self.assertEqual(first.status, "accepted")

    def test_seeker_can_withdraw_submitted_offer(self):
        offer = PropertyOffer.objects.create(
            property=self.property,
            seeker=self.customer,
            provider=self.provider,
            amount=420000,
        )

        self.client.force_authenticate(self.customer)
        response = self.client.patch(
            f"/api/v1/account/offers/{offer.pk}/withdraw/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        offer.refresh_from_db()
        self.assertEqual(offer.status, "withdrawn")
        self.assertEqual(Notification.objects.filter(user=self.provider).count(), 1)
