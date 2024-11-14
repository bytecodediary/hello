from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Agent, Client, Owner, CustomUser, Verification, Appointment, Tenant




class OwnerSerializer(serializers.ModelSerializer):
    property_details = serializers.SerializerMethodField()
    property = serializers.PrimaryKeyRelatedField(read_only=True, source='property.id')
    user = serializers.StringRelatedField()

    class Meta:
        model = Owner
        fields = ['id', 'property', 'user', 'property_details', 'phone_number' ]
    
    def get_property_details(self, obj):
        # Implement this method to return property details if needed
        return obj.property.title if obj.property else None

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',  'email', 'password'] #'first_name', 'last_name',
        read_only_fields = ['id']

    def create(self, validated_data):
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

class LoginSerializer(serializers.Serializer):  # Use Serializer instead of ModelSerializer
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')  # Use parentheses instead of brackets
        password = data.get('password')

        # print(f"attempting to validate with: {email}")
        # Authenticate the user
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid email or password')  # Use ValidationError instead of ValueError

        data['user'] = user
        return data

class AgentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(source='CustomUser.username', read_only=True)

    class Meta:
        model = Agent
        fields = ['id', 'user', 'phone_number', 'dob', 'listings', 'is_available']

class ClientSerializer(serializers.ModelSerializer):
    tenant = CustomUserSerializer(source='CustomUser.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'tenant', 'phone_number', 'has_paid']

      

class AppointmentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(source="CustomUser.username", read_only=True)

    class Meta:
        model = Appointment
        fields = ["user", "appointment_date", "appointment_status", "set_at", "property_set", "purpose"]


class VerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Verification
        fields = ['status', 'token', 'is_verified', 'expires', 'created_at', 'user']
        read_only_fields = ['token', 'is_verified', 'created_at']
    
    def validate(self, data):
        verification_instance = self.instance
        if verification_instance:
            if verification_instance.is_token_expired():
                raise serializers.ValidationError('Token expired')
            
            if verification_instance and verification_instance.is_verified:
                raise serializers.ValidationError('User with this token already verified')

        return data
    def save(self, **kwargs):
        instance = super().save(**kwargs)
        if not instance.is_verified and not instance.is_token_expired():
            instance.is_verified = True
            instance.status = "verified"
        elif not instance.is_verified and instance.is_token_expired():
            instance.status = "rejected"
        else:
            instance.status = "pending"
        instance.save()
        return instance

class TenantSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(source="CustomUser.username", read_only=True)

    class  Meta:
        model = Tenant
        fields = ['user', 'name', 'email', 'phone_number', 'lease_agreement', 'rent_status']

    