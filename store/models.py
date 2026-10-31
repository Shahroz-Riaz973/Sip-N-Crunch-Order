from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_TYPES = (
        ('retail', 'Retail / Single Cup Sale'),
        ('bulk', 'Cafe Wholesale Box'),
    )
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=10, choices=CATEGORY_TYPES, default='retail')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2) # Aik cup ki price
    stock_cups = models.IntegerField(default=0) # Total individual cups available
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} (Per Cup)"

class B2BClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    ntn_number = models.CharField(max_length=50, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tracking_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    is_b2b_order = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.tracking_id} - {self.full_name} [{self.status}]"

class SampleRequest(models.Model):
    cafe_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    estimated_usage = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='New Request')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sample Request: {self.cafe_name} ({self.city})"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.product_name} (Order #{self.order.tracking_id})"