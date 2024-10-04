from rest_framework import serializers, viewsets, routers
from django.urls import path, include
from .models import CustomUser
from django.contrib.auth.models import Group

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'first_name', 'email', 'last_name']

class ChangeUserTypeSerializer(serializers.ModelSerializer):
    new_user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPES)

    class Meta:
        models = CustomUser
        fields = ['new_user_types']
    
    def update(self, validated_data):
        self.new_user_type = validated_data['new_user_types']
        self.new_user_type.save()
        return self.new_user_type