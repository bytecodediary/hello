from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass

status_choices =(
    ("sold", "Sold"),
    ("pending", "Pending"),
    ("available", "Available"),
)
class Property(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    city = models.CharField(max_length=50)
    status = models.TextChoices(default=status_choices)
    address = models.CharField(max_length=50)
    listed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.IntegerField()
    slug = models.SlugField()

    def __str__(self):
        return self.title + self.status


class Image(models.Model):
    image = models.ImageField(upload_to="media/product_images")
    image_alt = models.TextField()
    property = models.ForeignKey(property, on_delete=models.CASCADE)

    def __str__(self):
        return self.image_alt
class CartItem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    property_name = models.ForeignKey(Property, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
         return self.user.username
 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(decimal_places=2, default=0, max_digits=10)
    cart_items = models.ManyToManyField(CartItem, on_delete=models.CASCADE)
        
    def total_price(self):
        return f"{self.price} x {self.product_amount} in the cart"

class Transaction(models.Model):
    slug = models.SlugField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(decimal_places=2, default=0, max_digits=10)

     

