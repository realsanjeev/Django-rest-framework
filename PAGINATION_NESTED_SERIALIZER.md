#### Nested serializer
**Nested Serializers in Django REST Framework**

In Django REST Framework, creating nested serializers involves utilizing two serializer classes, with the second serializer embedded within the first. This can be achieved within a single file or by importing a serializer from another file.

Here's a breakdown of the process:

1. **Defining the First Serializer**

   In a file named `serializers.py`, you can define your serializers. For example:

   ```python
   # api/serializers.py
   from django.contrib.auth import get_user_model
   User = get_user_model()

   class UserPublicSerializer(serializers.ModelSerializer):
       username = serializers.CharField(read_only=True)
       id = serializers.IntegerField(read_only=True)

       class Meta:
           model = User
           fields = [
               "username",
               "id"
           ]
   ```

   Here, the `UserPublicSerializer` is defined to extract specific fields (`username` and `id`) from the `User` model.

2. **Creating the Nested Serializer**

   To create a nested serializer, incorporate the `UserPublicSerializer` within another serializer. This can be done by referencing the `UserPublicSerializer` class and specifying the source for data extraction.

   ```python
   class BookSerializer(serializers.ModelSerializer):
       user_detail = UserPublicSerializer(read_only=True, source="user") 

       class Meta:
           model = Book
           fields = ["user_detail", "id", "title", "desc", "price", "sales_price", "discount"]
   ```

   In this example, the `BookSerializer` includes the nested field `user_detail`, which utilizes the `UserPublicSerializer`. The `source="user"` parameter signifies that the concatenated serializer employs the `user` attribute from the `Book` model as a reference to fetch data.

#### Pagination
Pagination in Django REST Framework allows you to manage large datasets by breaking them into smaller, manageable chunks. By default, pagination is automatically applied when using generic views or viewsets. If you're working with a regular `APIView`, you need to manually implement pagination to ensure a paginated response.

To set up pagination globally, modify your `settings.py`:

```python
REST_FRAMEWORK = {
    # other default settings
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
}
```

However, note that this default setting might not work with the `APIView` class. For working with pagination and `APIView`, you should consider using `generic APIViews` which handle pagination for you.

If you're still interested in using pagination with `APIView`, you can create a custom pagination class. In your project's `pagination.py`:

```python
# books/pagination.py

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

To integrate this custom pagination with an `APIView`, follow these steps:

```python
# books/views.py
class BookAPIView(APIView, LimitOffsetPagination):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAdminUser, IsStaffPermission]
    pagination_class = CustomOffsetPagination

    def get(self, request, *args, **kwargs):
        self.serializer_context = {"request": request}
        instance = self.get_object(*args, **kwargs)
        
        # Initiate paginator in GET request
        paginator = CustomOffsetPagination()
        
        if not instance:
            queryset = Book.objects.all()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = BookSerializer(result_page, many=True, context=self.serializer_context)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = BookSerializer(instance, context=self.serializer_context).data
        return Response({"detail": serializer})
```

Keep in mind that using `generic APIViews` is recommended for ease of pagination handling. This example demonstrates how to implement pagination with a custom pagination class and the `APIView` class.

