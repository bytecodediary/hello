from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser,Payment,Property,CartItem,Cart,Property_Features, Order, OrderItem, Agent, Client, Property_Lord,  Image, Transaction, Notification
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
    
class PropertyFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property_Features
        fields = ['feature_name', 'feature_value']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'image_alt']

class PropertySerializer(serializers.ModelSerializer):
    features = PropertyFeaturesSerializer(many=True, required=False)
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property 
        fields = ['slug', 'title','description', 'price', 'image', 'city', 'address', 'listed_at', 'updated_at', 'features']
    
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

class CartItemSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source="property.title", read_only=True)
    slug = serializers.SlugField()

    class Meta:
        model = CartItem
        fields = ['slug', 'property_name', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = CustomUserSerializer()
    slug =serializers.SlugField()
   
    class Meta:
        model = Cart
        fields = ['slug', 'total_price', 'items', 'user']
    
    def get_total_price(self, obj):
        total = sum(item.quantity * item.property.price for item in obj.items.all())
        return total

class OrderItemSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    property_name = serializers.CharField(source="property.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['slug', 'quantity', 'property_name']
    
    

class OrderSerializer(serializers.ModelSerializer):
    orders = OrderItemSerializer(source="order_items" ,many=True, read_only=True)
    slug = serializers.SlugField()
    user = CustomUserSerializer(source="order", read_only=True)

    class Meta:
        model = Order
        fields = ['slug', 'user', 'created_at', 'updated_at']

class AgentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(source='CustomUser.username', read_only=True)

    class Meta:
        model = Agent
        fields = ['id', 'user', 'phone_number', 'dob', 'listings', 'is_available']