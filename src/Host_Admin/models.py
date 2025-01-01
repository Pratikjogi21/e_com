from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_id = models.CharField(max_length=100, unique=True)  
    product_name = models.CharField(max_length=255)  
    product_image = models.ImageField(upload_to='') 
    product_price = models.DecimalField(max_digits=10, decimal_places=2) 
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"