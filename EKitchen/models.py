from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    first = models.CharField(max_length=20)
    last = models.CharField(max_length=20)
    dob = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=120)
    email = models.EmailField(max_length=255, blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=120)
    image = models.CharField(max_length=120)
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=1.0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    availability = models.IntegerField()
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    ORDER_STATUS = (
        ('Paid', 'Paid'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Delivering', 'Delivering'),
        ('Delivered', 'Delivered'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled')
    )
    status = models.CharField(choices=ORDER_STATUS, max_length=20)
