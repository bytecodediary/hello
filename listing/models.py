from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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
        "order.Order".objects.filter(slug=slug).exists() or
        "order.Cart".objects.filter(slug=slug).exists() or
        Property.objects.filter(slug=slug).exists() or
        "listing.Payment".objects.filter(slug=slug).exists() or 
        "payment.Transaction".objects.filter(slug=slug).exists() or
        "order.OrderItem".objects.filter(slug=slug).exists() or
        "order.CartItem".objects.filter(slug=slug).exists()
    )


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
    stock = models.IntegerField(default=1)
    slug = models.SlugField(unique=True, blank=True)
    

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

class Notification(models.Model):
    message = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:50]

