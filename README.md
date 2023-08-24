### Set up environment
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
- `JsonResponse`: used to pass json type data to endpoint
- `HttpResponse`: used to pass text/html data to endpoint. We can make it to send json data by changing `header`. But it is quite tedious.

## REQUEST the endpoint
#### REQUESTS 
Look endpoint properly if `/` is needed or not to pass request body


#### Order
1. **`/api/`** - Simple api through django
2. **`/api/product/`** - Passing model return data to endpoint using `model_to_dict` method

