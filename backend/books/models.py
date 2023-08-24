from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=128)
    desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=9.99)

    @property
    def get_sale_price(self):
        return '%.2f' % (float(self.price) * 0.8)
    
    