from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, default=99.0, max_digits=7)
