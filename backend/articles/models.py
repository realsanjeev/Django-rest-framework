from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class ArticleQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(make_public=True, publish_date__lte=timezone.now())
    
    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(body__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs

class ArticleManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return ArticleQuerySet(self.model, using=self._db)
    
    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

class Article(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=128)
    body = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True, help_text="Use comma separated value")
    make_public = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    objects = ArticleManager()

    def is_public(self):
        if self.publish_date is None:
            return False
        if self.make_public is None:
            return False
        now = timezone.now()
        is_in_past = now >= self.publish_date
        return is_in_past and self.make_public

    def get_tags_list(self):
        if not self.tags:
            return []
        return [x.lower().strip() for x in self.tags.split(',')]
