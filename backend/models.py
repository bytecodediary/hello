from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.forms import ValidationError
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
import string
import random

def generate_unique_slug():
    length = 24
    characters = string.ascii_lowercase + string.digits

    while True:
        slug = ''.join(random.choices(characters, k=length))
        if not slug_in_any_model(slug):
            return slug  # Return the unique slug once found

def slug_in_any_model(slug):
    return (
        Order.objects.filter(slug=slug).exists() or
        Cart.objects.filter(slug=slug).exists() or
        Property.objects.filter(slug=slug).exists() or
        Payment.objects.filter(slug=slug).exists() or 
        Transaction.objects.filter(slug=slug).exists() or
        OrderItem.objects.filter(slug=slug).exists()
    )

class CustomUserManager(BaseUserManager):
    def create_user(self, email,password=None, default='customer', **extra_fields):
        if not email:
            return ValueError("email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('customer', 'customer'),
        ('agent', 'agent'),
        ('proplord', 'property_lord'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_pending_type_change = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def apply_for_type_change(self,  new_type):
        if new_type in dict(self.USER_TYPES).keys():
            self.user_type = new_type
            self.is_pending_type_change = True
            self.save()
            return True
        return False

    def __str__(self):
        return self.email


class Property(models.Model):
    status_choices =(
    ("sold", "Sold"),
    ("pending", "Pending"),
    ("available", "Available"),
    )
    title = models.CharField(max_length=50)
    description = models.TextField()
    city = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=status_choices, default='available')
    address = models.CharField(max_length=50)
    listed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.IntegerField()
    slug = models.SlugField(unique=True, blank=True)
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

class Owner(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    properties = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='owned_properties')

    def __str__(self):
        return self.phone_number.as_e164 # displays in international format

class Image(models.Model):
    image = models.ImageField(upload_to="media/product_images")
    image_alt = models.TextField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images", default='')
    
    def __str__(self):
        return self.image_alt
       
class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=200)
    feature_value = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.feature_name
 
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.property.price * item.quantity for item in self.order_items.all())
        
    def __str__(self):
        return f"cart for {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.save:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

class CartItem(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="order_items")

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    Transaction_types = (
    ('paid', 'paid'),
    ('refunded', 'refunded'),
    ('adjusted', 'adjusted')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    transaction_type = models.CharField(max_length=50, choices=Transaction_types)
    description = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f"{self.transaction_type} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

class Transaction(models.Model):
    amount = models.IntegerField(default=0)
    date_paid = models.DateTimeField(auto_now=True)
    transaction_desc = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="transactions")

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

class Notification(models.Model):
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:50]

class Client(models.Model):
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True, blank=False, null=False, default="+25470000000")
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number.as_e164

    
class Agent(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dob = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    listings = models.ManyToManyField(Property)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.phone_number.as_e164
    
    def validate_years(self):
        time_now = datetime.now()
        t22_years = time_now - datetime.timedelta(days=22*365.25)
        if self.dob < t22_years:
            return ValidationError("Age is below 22 years")
        return self.dob

class Order(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return f"order for {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)
    
class OrderItem(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    slug = models.SlugField(unique=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")

    def __str__(self):
        return f"{self.property.title}"
    
    def save(self, *args, **kwargs):
        if not self.save:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)
