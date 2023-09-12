### Nested Serializers

**Using Nested Serializers in Django REST Framework**

In Django REST Framework (DRF), nested serializers allow you to include one serializer within another. This is useful when you want to represent related models in a single API response. You can define nested serializers in the same file or import them from another module.

#### 1. Define the Base Serializer

Create your base serializer in `serializers.py`. For example, a simple `UserPublicSerializer` to expose limited user information:

```python
# api/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "id"]
```

This serializer selects only the `username` and `id` fields from the `User` model.

#### 2. Create the Nested Serializer

To nest this serializer within another, reference it as a field in a second serializer:

```python
class BookSerializer(serializers.ModelSerializer):
    user_detail = UserPublicSerializer(read_only=True, source="user")

    class Meta:
        model = Book
        fields = ["user_detail", "id", "title", "desc", "price", "sales_price", "discount"]
```

Here, `user_detail` is a nested field using `UserPublicSerializer`. The `source="user"` tells DRF to fetch data from the `user` attribute of the `Book` model.

---

### Pagination

Pagination in DRF helps manage large datasets by splitting them into smaller chunks. Generic views and viewsets automatically support pagination, but with `APIView` you need to handle it manually.

#### 1. Global Pagination

You can configure default pagination in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
}
```

**Note:** This works automatically with generic views, but `APIView` requires explicit pagination handling.

#### 2. Custom Pagination with `APIView`

Define a custom pagination class in `pagination.py`:

```python
# books/pagination.py
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link()
            },
            "count": self.count,
            "results": data
        })
```

Integrate it into an `APIView`:

```python
# books/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .pagination import CustomOffsetPagination
from .serializers import BookSerializer
from .models import Book
from rest_framework import permissions

class BookAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        paginator = CustomOffsetPagination()
        queryset = Book.objects.all()
        page = paginator.paginate_queryset(queryset, request)
        serializer = BookSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)
```

While this approach works, using **generic APIViews** like `ListAPIView` or `ListCreateAPIView` is recommended since they handle pagination automatically.
