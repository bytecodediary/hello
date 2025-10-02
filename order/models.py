from django.db import models
from user.models import CustomUser
from listing.models import generate_unique_slug

class Order(models.Model):
    order_status = (
    ('delivered', 'Delivered'),
    ('returned', 'Returned'),
    ('pending', 'pending'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="order")
    status = models.CharField(choices=order_status, default='pending', max_length=50)
    slug = models.SlugField(blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"order for {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)
    
class OrderItem(models.Model):
    property = models.ForeignKey("listing.Property", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    slug = models.SlugField(unique=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")

    def __str__(self):
        return f"{self.property.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def total(self):
        return sum(item.property.price * item.quantity for item in self.order_items.all())
        
    def __str__(self):
        return f"cart for {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)

class CartItem(models.Model):
    property = models.ForeignKey("listing.Property", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="order_items")
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f"item for {self.cart.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug()
        super().save(*args, **kwargs)
    