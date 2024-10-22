from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.forms import ValidationError

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    REQUIRED_FIELDS = ['username', 'first_name']

    def apply_for_type_change(self,  new_type):
        if new_type in dict(self.USER_TYPES).keys():
            self.user_type = new_type
            self.is_pending_type_change = True
            self.save()
            return True
        return False

    def __str__(self):
        return self.email

class Owner(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owners')
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    properties = models.ForeignKey("listing.Property", on_delete=models.CASCADE, related_name='owned_properties')

    def __str__(self):
        return self.phone_number.as_e164 # displays in international format

class Client(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='clients', default='')
    phone_number = PhoneNumberField(unique=True, blank=False, null=False, default="+25470000000")
    dob = models.DateTimeField()
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number.as_e164 
    
class Agent(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agents')
    dob = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    listings = models.ManyToManyField("listing.Property")
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.phone_number.as_e164
    
    def validate_years(self):
        time_now = datetime.now()
        t22_years = time_now - datetime.timedelta(days=22*365.25)
        if self.dob < t22_years:
            return ValidationError("Age is below 22 years")
        return self.dob
 