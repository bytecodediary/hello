from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.apps import apps
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
    Order = apps.get_model('order', 'Order')
    Cart = apps.get_model('order', 'Cart')
    Payment = apps.get_model('payment', 'Payment')
    Transaction = apps.get_model('payment', 'Transaction')
    OrderItem = apps.get_model('order', 'OrderItem')
    CartItem = apps.get_model('order', 'CartItem')
    
    return (
        Order.objects.filter(slug=slug).exists() or
        Cart.objects.filter(slug=slug).exists() or
        Property.objects.filter(slug=slug).exists() or
        Payment.objects.filter(slug=slug).exists() or 
        Transaction.objects.filter(slug=slug).exists() or
        OrderItem.objects.filter(slug=slug).exists() or
        CartItem.objects.filter(slug=slug).exists()
    )

class Property(models.Model):
    LISTING_TYPE_CHOICES = (
        ("sale", "For sale"),
        ("rent", "For rent"),
    )
    PROPERTY_TYPE_CHOICES = (
        ("house", "House"),
        ("apartment", "Apartment"),
        ("townhouse", "Townhouse"),
        ("land", "Land"),
        ("commercial", "Commercial"),
        ("other", "Other"),
    )
    status_choices =(
    ("sold", "Sold"),
    ("pending", "Pending"),
    ("available", "Available"),
    )
    MODERATION_STATUS_CHOICES = (
        ("draft", "Draft"),
        ("pending_review", "Pending review"),
        ("published", "Published"),
        ("rejected", "Rejected"),
        ("archived", "Archived"),
    )
    title = models.CharField(max_length=50)
    description = models.TextField()
    city = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=status_choices, default='available')
    address = models.CharField(max_length=50)
    listed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="KES")
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default="sale")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default="house")
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    area_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    county = models.CharField(max_length=80, blank=True)
    neighborhood = models.CharField(max_length=100, blank=True)
    stock = models.IntegerField(default=1)
    slug = models.SlugField(unique=True, blank=True)
    moderation_status = models.CharField(
        max_length=20,
        choices=MODERATION_STATUS_CHOICES,
        default="published",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_listings",
    )
    moderated_at = models.DateTimeField(null=True, blank=True)
    moderated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="moderated_listings",
    )
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        
        super().save(*args, **kwargs)

    def save_stock(self, *args, **kwargs):
        if self.stock < 1:
            self.stock = 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        indexes = [
            models.Index(fields=["moderation_status", "listing_type"]),
            models.Index(fields=["city", "county"]),
            models.Index(fields=["price"]),
            models.Index(fields=["created_by"]),
        ]

class Image(models.Model):
    image = models.ImageField(upload_to="properties/%Y/%m/")
    image_alt = models.TextField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    is_cover = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return self.image_alt
       
class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features')
    feature_name = models.CharField(max_length=200)
    feature_value = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.feature_name

class Notification(models.Model):
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:50]


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "property"], name="unique_user_property_favorite"),
        ]
        ordering = ["-created_at"]


class Inquiry(models.Model):
    TYPE_CHOICES = (
        ("inquiry", "Inquiry"),
        ("viewing", "Viewing request"),
    )
    STATUS_CHOICES = (
        ("new", "New"),
        ("contacted", "Contacted"),
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("declined", "Declined"),
        ("closed", "Closed"),
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inquiries")
    seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="property_inquiries")
    inquiry_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="inquiry")
    message = models.TextField(max_length=2000)
    preferred_start = models.DateTimeField(null=True, blank=True)
    preferred_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    provider_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["property", "status"]),
            models.Index(fields=["seeker", "status"]),
        ]


class PropertyOffer(models.Model):
    TYPE_CHOICES = (
        ("offer", "Offer"),
        ("reservation", "Reservation request"),
    )
    STATUS_CHOICES = (
        ("submitted", "Submitted"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("withdrawn", "Withdrawn"),
        ("expired", "Expired"),
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="offers")
    seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="property_offers",
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_property_offers",
    )
    offer_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="offer")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="KES")
    message = models.TextField(max_length=2000, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    provider_response = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["property", "status"]),
            models.Index(fields=["seeker", "status"]),
            models.Index(fields=["provider", "status"]),
        ]
