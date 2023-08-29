import json
from django.http import JsonResponse
from django.forms.models import model_to_dict

from rest_framework import generics, mixins
from api.serializers import ProductSerializer
from api.models import Product

def display_dash_console(statement: str):
    print("*"*4,statement,"*"*4)


def simple_api(request, *args, **kwargs):
    # Decode the request body
    body = request.body.decode('utf-8')

    # Parse JSON data from the decoded body
    try:
        data = json.loads(body)
    except Exception as e:
        print("Exceptipn", e)
        data = {}

    # Get query parameters as a dictionary
    query_params = request.GET.dict()
    content_header = request.headers
    print(request)

    # Combine parsed JSON data and query parameters
    data["query_params"] = query_params
    # data["content_header"] = content_header

    print("body:", body)
    print("data:", data)

    return JsonResponse(data)

def model_response(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
         data["id"] = model_data.id
         data["title"] = model_data.title
         data["content"] = model_data.content
         data["price"] = model_data.price
        #  data = model_to_dict(model_data, fields=["id", "price","title"])
         return JsonResponse(data)
    return JsonResponse({"err": "The database is not reponding properly"})

class ProductRetriveCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)

class ProductDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    print("Update initiated")

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
