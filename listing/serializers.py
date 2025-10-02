from rest_framework import serializers
from user.serializers import OwnerSerializer
from .models import Property,PropertyFeature, Image,Notification
from fcm_django.models import FCMDevice

class PropertyFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = ['feature_name', 'feature_value']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'image_alt']

class PropertySerializer(serializers.ModelSerializer):
    features = PropertyFeaturesSerializer(many=True, required=False)
    owners = OwnerSerializer(many=True, read_only=True, source='owned_properties')
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Property 
        fields = ['slug', 'title', 'owners', 'description', 'price', 'images', 'city', 'address', 'listed_at', 'updated_at', 'features']
    
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
        field = ['user', 'message']

class NotificationMiniSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'user', 'received_at', 'is_read']