from django.urls import path
from . import views

urlpatterns = [
#     path('', views.simple_api),
#     path('product', views.model_response),
    path('product/',
         views.ProductRetriveCreateAPIView.as_view(),
         name="product-list"),
    path('product/<int:pk>/delete/',
         views.ProductDestroyAPIView.as_view(),
         name="product-delete"),
    path('product/<int:pk>/update/',
         views.ProductUpdateAPIView.as_view(),
         name="product-edit"),
     path('product/<int:pk>/',
          views.ProductDetailAPIView.as_view(),
          name="product-detail")
    
]