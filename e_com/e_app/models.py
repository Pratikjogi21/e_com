from django.db import models
from django.contrib.auth.models import User
import uuid
class Host(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128) 
    ROLE_CHOICES = (
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        db_table = 'Host_Details'



class Product(models.Model):
    product_id = models.CharField(max_length=100, unique=True)  
    product_name = models.CharField(max_length=255)  
    product_image = models.ImageField(upload_to='') 
    product_price = models.DecimalField(max_digits=10, decimal_places=2) 
    stock = models.PositiveIntegerField(default=0)




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True,default=uuid.uuid4 ) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200) 
    product_price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.PositiveIntegerField() 

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

