from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class ArticleManager(models.Manager):
	def public(self):
		now = timezone.now()
		return self.get_queryset().filter(make_public=True, publish_data__lte=now)

# Create your models here.
class Article(models.Model):
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=128)
	body = models.TextField(blank=True, null=True)
	tags = models.TextField(blank=True, null=True, help_text="Use comman separated value")
	make_public = models.BooleanField(default=False, null=True, blank=True)
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

	def is_public(self):
		if self.publish_date is None:
			return False
		if self.make_public is None:
			return False
		now = timezone.now()
		is_in_past = now >= self.publish_date
		return is_in_past and self.make_public
	
	def get_tag_list(self):
		if not self.tags:
			return []
		return [x.lower().strip() for x in self.tags.split(',')]
