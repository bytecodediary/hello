from django.db import models
from django.contrib.auth.models import User, PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.forms import ValidationError
from django.utils import timezone
import datetime

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
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_pending_type_change = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELDS = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def apply_for_type_change(self,  new_type):
        if new_type in dict(self.USER_TYPES).keys():
            self.user_type = new_type
            self.is_pending_type_change = True
            self.save()
            return True
        return False

    def __str__(self):
        return self.email

class Property_Lord(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    landlord = models.ForeignKey(Property_Lord, on_delete=models.CASCADE)
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
        
class Property_features(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=200)
    feature_value = models.IntegerField(max_length=200)

    def __str__(self):
        return self.feature_name
    
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

class Payment(models.Model):
    Transaction_types = (
    ('paid', 'paid'),
    ('refunded', 'refunded'),
    ('adjusted', 'adjusted')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(decimal_places=2, max_digits=10)
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
    time_now = datetime.now()
    t22_years = time_now - datetime.timedelta(days=22*365.25)
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
