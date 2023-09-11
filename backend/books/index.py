from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Book

@register(Book)
class BookIndex(AlgoliaIndex):
    # should_index = 'is_public'
    fields = [
        'title',
        'desc',
        'price',
        'user',
        'public',
    ]
    # get tag list index
    tags = 'get_tag_list'
    settings = {
        'searchableAttributes': ['title', 'content'],
        'attributesForFaceting': ['user', 'public']
    }
