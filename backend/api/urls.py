from django.urls import path
from . import views

urlpatterns = [
    path('', views.simple_api),
    path('product', views.model_response)
]