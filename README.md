### Set up environment
> branch: "intro_generic_class"
```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
#### Start the project
```
django-admin startproject server .
python manage.py runserver 8000
```
### Django RESTfull
- `JsonResponse`: used to pass `json` type data to endpoint
- `HttpResponse`: used to pass `text/html` data to endpoint. We can make it to send `json` data by changing `header`. But it is quite tedious.
- When passing the `json` without `django-framework` it takes lot to code program that passes the new firld which is obtained by doing some calculation in model data.

#### Django_rest_framework
It is essential to serialize data into JSON format to be sent as a REST API response and deserialize incoming requests to be processed on the backend. The Django Rest Framework offers a variety of tools for sending and receiving data, facilitating the work with REST APIs on the backend. This framework is built on top of the Django framework.

One approach to serialization involves using the `@property` decorator in the `models.py` file. By directly specifying the function's name as a field in the `serializer.py` file, we can achieve serialization as shown below:

```python
# In models.py 
class ModelName(models.Model):
    # ...other code
    @property
    def sales_price(self):
        return '%.2f' % (float(self.price) * 0.7)
```

In serializers:

```python
# serializers.py
class ModelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelName
        fields = [...otherfields, "sales_price"]
```

Alternatively, we can add a method in the model without using a decorator in `models.py`. And we can change how field name in response is changed from the method name. This allows more things that can be done in serializer to enruch the serializer. Such `example` is shown below:

```python
class MyModelSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()
    # ...other code
    fields = [...otherfields, 'discount']

    def get_discount(self, obj):
        # check attribute in instance
        if not hasattr(self, "id"):
            return None
        # or check serializer is instance. 
        # Same as above to check serialixer instance
        if not isinstance(self, Book):
            return None
        return obj.get_discount_price()
```

In this example, the `calculate_discount` method is assumed to be present in the model, and if it exists, the method's result is included in the serialized data. Additionally, this approach ensures that any discrepancies between the model's attributes and the serialization process are handled effectively.

### Class View
#### Generic View
In order to retrieve data from a model, certain attributes such as `lookup_field`, `queryset`, and `serializer_class` need to be defined. This ensures the correct retrieval of data. Here's the explanation and a corrected version of the provided code:

```python
# Explanation:
# To retrieve data from a model, several attributes such as 'lookup_field', 'queryset',
# and 'serializer_class' must be defined. These attributes ensure that data can be
# retrieved accurately and serialized properly.

from rest_framework import generics

class BookDetailAPIView(generics.RetrieveAPIView):
    # 'lookup_field' determines the field used for looking up the object in the URL.
    lookup_field = 'pk'  # The default lookup field is "pk", which refers to the primary key.

    # 'queryset' specifies the set of objects from which data is retrieved.
    queryset = Book.objects.all()  # Replace 'Book' with your actual model class.

    # 'serializer_class' defines the serializer used to convert model data into JSON.
    serializer_class = BookSerializer  # Replace 'BookSerializer' with your actual serializer class.
```

In order to handle different HTTP methods (GET, POST, PUT, DELETE) for requests in the same URL endpoint, you can utilize a `Mixin` class along with a `View` class. The following is an example of how you can achieve this:

```python
from rest_framework import generics, mixins

class BookDetailAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    lookup_field = 'pk'
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

In this example, the `BookDetailAPIView` class uses mixins to handle different methods (GET, PUT, DELETE) in the same URL endpoint. It inherits from `generics.GenericAPIView` to provide a common base for handling these methods. The `get`, `put`, and `delete` methods correspond to the respective HTTP methods and use the appropriate mixin methods (`retrieve`, `update`, `destroy`) to perform the actions.

### Authentication and Permission In Rest API
```python
from rest_framework import permissions, authentication
class BookAPIView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```
#### Authentication
- `SessionAuthentication` means user will be authentication until user log out or session expire

#### Permission
- `IsAuthenticatedOrReadOnly` allows user `GET` method while other methods are not allowed. Only authenticated user are allowed other Method, i.e, `POST`, `PUT`, `PATCH` and `DELETE`.
- `AllowAny` allows user all methods without authentication within which it is defined
- `IsAuthenticated` only allows authentication user to perform any method operation
- `IsAdminUser` only allows admin to perform any operation in api. 
- `DjangoModelPermissions` allows the authentication from django login auth. But it allows `GET` permission regardless. See Documentation
## REQUEST the endpoint
#### REQUESTS 
Look endpoint properly if `/` is needed or not to pass request body


#### Order
1. **`/api/`** - Simple api through django
2. **`/api/product/`** - Passing model return data to endpoint using `model_to_dict` method
3. **`v1/api/1/`** - GEt the record with primary key(ie. id) =1

