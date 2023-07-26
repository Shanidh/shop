from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.BigIntegerField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)

class Cart(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="order_cart",
        null=True,)
    products = models.ManyToManyField(Product)    


class ProductRating(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()    