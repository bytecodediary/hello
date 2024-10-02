from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.forms import ValidationError
from django.utils import timezone
import datetime
import requests

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('tenant', 'tenant'),
        ('agent', 'agent'),
        ('landlord', 'landlord'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='tenant')


class Landlord(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.IntegerField(max_length=12)

    def __str__(self):
        return self.name.username

class Image(models.Model):
    image = models.ImageField(upload_to="media/product_images")
    image_alt = models.TextField()
    

    def __str__(self):
        return self.image_alt
    
class Property(models.Model):
    status_choices =(
    ("sold", "Sold"),
    ("pending", "Pending"),
    ("available", "Available"),
    )
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    city = models.CharField(max_length=50)
    status = models.TextChoices(default=status_choices)
    address = models.CharField(max_length=50)
    listed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.IntegerField()
    slug = models.SlugField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + self.status



    
class CartItem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    property_name = models.ForeignKey(Property, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.username
 
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(decimal_places=2, default=0, max_digits=10)
    cart_items = models.ManyToManyField(CartItem, on_delete=models.CASCADE)
        
    def total_price(self):
        return f"{self.price} x {self.product_amount} in the cart"

class Transaction(models.Model):
    Transaction_types = (
    ('paid', 'paid'),
    ('refunded', 'refunded'),
    ('adjusted', 'adjusted')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(decimal_places=2, max_digits=10)
    transaction_type = models.CharField(max_length=50, choices=Transaction_types)
    description = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.transaction_type} by {self.user.username}"

class Notification(models.Model):
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:50]
    
    def is_read(self):
        return self.is_read == False

class client(models.Model):
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.tenant.username
    
def validate_years(request):
    dob = Agent.objects.filter(Dob=dob, user=request.user)
    now = datetime.now()
    t22_years = now - datetime.timedelta(days=22*365.25)
    if dob < t22_years:
        return ValidationError(request, "Age is below 22 years")
    return dob


class Agent(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Dob = models.DateTimeField(default=validate_years)
    is_available = models.BooleanField(default=True)
    listings = models.ManyToManyField(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.Dob
    

class Payment(models.Model):
    amount = models.IntegerField(default=0)
    date_paid = models.DateTimeField(auto_now=True)
    transaction_desc = models.CharField(max_length=200)
    slug = models.SlugField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"order for {self.user.username}"
    
class Order_Item(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    slug = models.SlugField()
    order_item = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{property.name}"
