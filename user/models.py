from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, email,password=None, default='customer', **extra_fields):
        if not email:
            raise ValueError("email must be set")
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
        ('landlord', 'landlord'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_pending_type_change = models.BooleanField(default=False)
    PROVIDER_STATUS_CHOICES = (
        ('none', 'None'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    provider_status = models.CharField(max_length=20, choices=PROVIDER_STATUS_CHOICES, default='none')
    requested_provider_type = models.CharField(max_length=20, choices=USER_TYPES, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name']

    def apply_for_type_change(self,  new_type):
        provider_types = {'agent', 'proplord', 'landlord'}
        if new_type in provider_types:
            self.requested_provider_type = new_type
            self.provider_status = 'pending'
            self.is_pending_type_change = True
            self.save()
            return True
        return False

    @property
    def can_manage_listings(self):
        return self.is_staff or (
            self.user_type in {'agent', 'proplord', 'landlord'}
            and self.provider_status == 'approved'
        )

    def __str__(self):
        return self.email

    def get_full_name(self):
        return " ".join(part for part in (self.first_name, self.last_name) if part).strip()

    def get_short_name(self):
        return self.first_name or self.username


class ProviderApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    PROVIDER_TYPES = (
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='provider_applications')
    requested_type = models.CharField(max_length=20, choices=PROVIDER_TYPES)
    organization_name = models.CharField(max_length=120, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    message = models.TextField(max_length=2000, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    review_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_provider_applications',
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user', 'status']),
        ]

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
 
class Tenant(models.Model):
    name = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="tenant_profile")
    email = models.EmailField()
    phone_number = PhoneNumberField(unique=False, blank=True, null=True)
    lease_agreement = models.CharField(max_length=255, blank=True)
    rent_status = models.ForeignKey(
        "payment.Payment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tenant_profiles",
    )

    @property
    def has_paid(self):
        if self.rent_status:
            return True
        return self.name.user_payments.filter(payment_mode="mpesa").exists()

    def __str__(self):
        return self.name.username

class Verification(models.Model):
    STATUS = [
        ['pending', 'Pending'],
        ['verified', 'Verified'],
        ['rejected', 'Rejected'],
    ]
    
    status = models.CharField(default="pending", max_length=20, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expires = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires:
            self.expires = timezone.now() + datetime.timedelta(days=1)
        super().save(*args, **kwargs)
    
    def is_token_expired(self):
        return bool(self.expires and timezone.now() >= self.expires and not self.is_verified)
    
    def is_failed(self):
        if self.is_token_expired():
            self.status = "rejected"
        return self.status
    
    # def __str__(self):
    #     return f"verified {self.user.email} - {"verified" if self.is_verified else "pending"}"

class Appointment(models.Model):
    STATUS = [
        ['pending', 'Pending'],
        ['failed', 'failed'],
        ['successful', 'Successful'],
        ['unset', 'Unset'],
    ]

    appointment_status = models.CharField(max_length=20, default='unset', choices=STATUS )
    appointment_date = models.DateTimeField()
    set_at = models.DateTimeField(auto_now_add=True)
    property_set = models.ForeignKey('listing.Property', on_delete=models.CASCADE, related_name='appointment_property')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=300)

    def clean_appointment_date(self):
        if not self.appointment_date:
            raise ValidationError("An appointment date is required.")
        if self.appointment_date <= timezone.now():
            raise ValidationError("An appointment must be scheduled in the future.")
        return self.appointment_date

    def __str__(self):

        return self.user.username
        return self.user.email
