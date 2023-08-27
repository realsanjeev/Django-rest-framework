### Set up environment
> branch: "default-setting_mixins"
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
### Django RESTful
- **`JsonResponse`**: This function is employed to send data in the `json` format to an endpoint. It's a straightforward way to structure and transmit JSON data within the response.

- **`HttpResponse`**: This function is used to transmit data in the `text/html` format to an endpoint. While it can be adjusted to send `json` data by modifying the HTTP headers, this approach can be cumbersome.

- When dealing with data that requires additional processing or calculations in your model, sending JSON data without utilizing the Django framework can involve a substantial amount of coding.

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

In `serializers.py`:

```python
# serializers.py
class ModelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelName
        fields = [...otherfields, "sales_price"]
```

Alternatively, we can add a method in the model without using a decorator in `models.py`. And we can change how field name in response is changed from the method name. This allows more things that can be done in serializer to enrich the serializer. Such `example` is shown below:

```python
class MyModelSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()
    # ...other code
    fields = [...otherfields, 'discount']

    def get_discount(self, obj):
        # check attribute in instance
        if not hasattr(obj, "id"):
            return None
        # or check serializer is instance. 
        # Same as above to check serialixer instance
        if not isinstance(obj, Book):
            return None
        return obj.get_discount_price()
```


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

class BookDetailAPIView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
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

### Authentication and Permissions in REST API

```python
from rest_framework import permissions, authentication

class BookAPIView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

#### Authentication

- The `SessionAuthentication` class signifies that a user remains authenticated until they log out or their session expires.

- By default, the authentication header is in the format `Authentication: Token tokenaeskds2...`. To customize the keyword used in the header, modify the `authentication.py` file from `TokenAuthentication`. Once changed, import the altered class into your `views`. Keep in mind that the authentication response will continue to be in the form `{'token': 'sal..'}`. However, when sending a header to request a resource, the header should be formatted as `{'Authorization': f'Bearer {token}'}`, where `Bearer` is the updated keyword.

#### Permissions

Permissions control the actions that different users can perform within a REST API:

- The `IsAuthenticatedOrReadOnly` permission grants users permission to use the `GET` method while restricting other methods. For instance, only authenticated users are permitted to use methods like `POST`, `PUT`, `PATCH`, and `DELETE`.

- The `AllowAny` permission allows unrestricted access to all methods without requiring authentication, if placed within the designated scope.

- The `IsAuthenticated` permission exclusively permits authenticated users to perform any operation.

- The `IsAdminUser` permission confines API operations to administrators only.

- The `DjangoModelPermissions` permission is aligned with the Django authentication system. However, it grants permission for the `GET` method by default. For a more comprehensive understanding, refer to the documentation.

##### Custom Permissions

**Remember, less permissions are better than more. Prioritize minimizing permissions for a better code of conduct.**

Permissions can be customized to suit your needs and should adhere to the principle of least privilege. Such custom permissions are defined in `app-name/permissions.py`:

```python
# api/permissions.py
from rest_framework import permissions

class IsStaffPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user
        print(user.get_all_permissions())
        if not user.is_staff:
            return False
        return super().has_permission(request, view)
```
#### Default REST Framework Settings and Mixins

These configurations are applied when you wish to utilize default settings across your entire project's API. To implement this, add the following to your `settings.py` file:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'books.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ]
}
```

We can streamline the process by organizing permission mixins within a separate file named eg. `permission_mixins.py`. This approach offers the advantage of simplifying view creation. Define a custom permission class within `permission_mixins.py`, and then, when creating views, inherit from both the desired `viewclass` from `rest_framework.views` and the custom permission class from `permission_mixins`.

This eliminates the need to explicitly define `permission_classes` within `views.py`, especially when fixed permissions are consistently employed. This approach promotes modularization and reduces redundancy in your codebase.

## REQUEST the endpoint
#### Requests
- Pay careful attention to whether a trailing `/` is required when passing a request body to an endpoint. This distinction is crucial for accurate endpoint navigation.

- Remember that for responses obtained from headers, you need to include `rest_framework.authtoken` in the `INSTALLED_APPS` section.

##### Endppoints

1. **`/api/`** - This endpoint provides a simple API utilizing Django's functionality.
2. **`/api/product/`** - Utilize the `model_to_dict` method to transmit model-generated data to the endpoint.
3. **`v1/api/1/`** - Retrieve the record with a primary key (e.g., id) equal to 1.
4. **`v1/api/auth/`** - Access the authentication endpoint to obtain a token for authentication purposes.
