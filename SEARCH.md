#### Searching in the Model

The code below outlines a way to perform searches within a model using a custom queryset and manager. In this case, the model is `Book`.

```python
# books/models.py
from django.db.models import Q
from django.db.models.query import QuerySet
class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    
    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(desc__icontains=query)
        public_qs = self.is_public().filter(lookup)
        
        if user is not None:
            user_qs = self.filter(user=user).filter(lookup)
            qs = (public_qs | user_qs).distinct()
        else:
            qs = public_qs
        
        return qs

class ProductManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return ProductQuerySet(self.model, using=self._db)
    
    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

class Book(models.Model):
    # Other fields ...

    objects = ProductManager()
```

#### Viewset for Search

The following code showcases a viewset used to query the search functionality for the `Book` model. This viewset utilizes the `SearchListView` class, extending the `generics.ListAPIView` class from Django REST framework.

```python
# books/views.py
class SearchListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        results = Book.objects.none()

        if query:
            user = self.request.user if self.request.user.is_authenticated else None
            results = qs.search(query, user=user)
        
        return results
```

In summary, these code snippets illustrate how to implement search functionality within the `Book` model using custom querysets, managers, and a viewset. The search can be performed based on the provided query parameter "q" and, if applicable, filtered for user-specific results when a user is authenticated.