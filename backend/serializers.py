from rest_framework import serializers, viewsets, routers
from django.contrib.auth import authenticate
from .models import CustomUser,Payment,Property
from django.contrib.auth.models import Group

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'first_name', 'email', 'last_name']

        def create(self, **validated_data):
            user = CustomUser(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user

class ChangeUserTypeSerializer(serializers.ModelSerializer):
    new_user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPES)

    class Meta:
        model = CustomUser
        fields = ['new_user_type']
    
    def update(self, instance, validated_data):
        new_user_type = validated_data['new_user_type']
        instance.apply_for_type_change(new_user_type)
        return instance

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get['email']
        password = data.get['password']

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if user is None:
            raise serializers.ValueError('invalid email or password')

        data['user'] = user
        return data
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property 
        fields = ['slug', 'title','description', 'price', 'image', 'city', 'address', 'listed_at', 'updated_at']
    
    def create(self,request, **validated_data):
        return Property.objects.create(**validated_data)

    def update(self, instance, **validated_data):
        instance.title = validated_data.get('name', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['price']