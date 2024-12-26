from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=100, unique=True)  # Unique identifier for the product
    product_name = models.CharField(max_length=255)  # Name of the product
    product_image = models.ImageField(upload_to='product_images/')  # Image field for the product
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product

    def __str__(self):
        return self.product_name
