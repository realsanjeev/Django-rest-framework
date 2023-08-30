from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.query import QuerySet

User = settings.AUTH_USER_MODEL

class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    
    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontents=query)
        qs = self.filter(lookup)
        if user is not None:
            qs = qs.filter(user=user)
        return qs

class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return ProductQuerySet(self.model, using=self._db)
    
    def search(self, query, user=None):
        return self.get_queryset().is_public().search(query, user=user)

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=128)
    desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=9.99)
    public = models.BooleanField(default=True)

    @property
    def sales_price(self):
        return '%.2f' % (float(self.price) * 0.8)
    
    def get_discount_price(self):
        return '%.2f' % (float(self.price) *0.2)
    
    def __str__(self) -> str:
        return self.title