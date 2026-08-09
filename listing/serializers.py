from rest_framework import serializers
from user.serializers import OwnerSerializer
from .models import Favorite, Inquiry, Property, PropertyFeature, Image, Notification
from fcm_django.models import FCMDevice

class PropertyFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = ['feature_name', 'feature_value']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'image_alt', 'is_cover', 'display_order']

class PropertySerializer(serializers.ModelSerializer):
    features = PropertyFeaturesSerializer(many=True, required=False)
    owners = OwnerSerializer(many=True, read_only=True, source='owned_properties')
    images = ImageSerializer(many=True, required=False)
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Property 
        fields = [
            'slug', 'title', 'owners', 'description', 'price', 'currency',
            'listing_type', 'property_type', 'status', 'moderation_status',
            'bedrooms', 'bathrooms', 'area_sqm', 'city', 'county',
            'neighborhood', 'address', 'listed_at', 'updated_at',
            'images', 'features', 'created_by_name', 'is_featured',
        ]
        read_only_fields = ['slug', 'owners', 'listed_at', 'updated_at', 'moderation_status', 'created_by_name']

    def get_created_by_name(self, obj):
        if not obj.created_by:
            return None
        return obj.created_by.get_full_name() or obj.created_by.username
    
    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        images_data = validated_data.pop('images', [])

        property_instance = Property.objects.create(**validated_data)

        for feature_data in features_data:
            PropertyFeature.objects.create(property=property_instance, **feature_data)
        
        for image_data in images_data:
            Image.objects.create(property=property_instance, **image_data)

        return property_instance

    def update(self, instance, validated_data):
        features_data = validated_data.pop('features', None)
        images_data = validated_data.pop('images', None)

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        
        if features_data is not None:
            instance.features.all().delete()
            for feature_data in features_data:
                PropertyFeature.objects.create(property=instance, **feature_data)
        
        if images_data is not None:
            instance.images.all().delete()
            for image_data in images_data:
                Image.objects.create(property=instance, **image_data)

        return instance

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = [
            'user',
            'action',
            'registration_id',
            'name',
            'device_id',
            'type',
            'date_created',
        ]

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['user', 'message']

class NotificationMiniSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'user', 'received_at', 'is_read']


class FavoriteSerializer(serializers.ModelSerializer):
    property_slug = serializers.CharField(source='property.slug', read_only=True)
    property_details = PropertySerializer(source='property', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'property', 'property_slug', 'property_details', 'created_at']
        read_only_fields = ['id', 'property_slug', 'created_at']


class InquirySerializer(serializers.ModelSerializer):
    property_slug = serializers.CharField(source='property.slug', read_only=True)
    seeker_name = serializers.SerializerMethodField(read_only=True)
    seeker_email = serializers.EmailField(source='seeker.email', read_only=True)

    class Meta:
        model = Inquiry
        fields = [
            'id', 'property', 'property_slug', 'inquiry_type', 'message',
            'preferred_start', 'preferred_end', 'status', 'provider_response',
            'seeker_name', 'seeker_email', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'property', 'property_slug', 'status', 'provider_response', 'seeker_name',
            'seeker_email', 'created_at', 'updated_at',
        ]

    def get_seeker_name(self, obj):
        return obj.seeker.get_full_name() or obj.seeker.username

    def validate(self, attrs):
        inquiry_type = attrs.get('inquiry_type', getattr(self.instance, 'inquiry_type', 'inquiry'))
        start = attrs.get('preferred_start')
        end = attrs.get('preferred_end')
        if inquiry_type == 'viewing' and not start:
            raise serializers.ValidationError({'preferred_start': 'A viewing request needs a preferred start time.'})
        if start and end and end <= start:
            raise serializers.ValidationError({'preferred_end': 'The preferred end must be after the start.'})
        return attrs


class InquiryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['status', 'provider_response']
