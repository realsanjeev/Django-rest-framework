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

## REQUEST the endpoint
#### REQUESTS 
Look endpoint properly if `/` is needed or not to pass request body


#### Order
1. **`/api/`** - Simple api through django
2. **`/api/product/`** - Passing model return data to endpoint using `model_to_dict` method
3. **`v1/api/1/`** - GEt the record with primary key(ie. id) =1

