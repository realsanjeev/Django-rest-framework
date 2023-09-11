from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Article

@register(Article)
class ArticleIndex(AlgoliaIndex):
    fields = [
        "user",
        "title",
        "body",
        "publish_date",
    ]
    tags = "get_tags_list"
    settings = {
        "searchableAttributes": ["title", "body"],
        "attributesForFaceting": ['user'],
        "ranking": ["asc(publish_date)"]
    }
