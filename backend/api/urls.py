from django.urls import path
from . import views
from articles import views as article_view

urlpatterns = [
#     ****Product urls*******
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
          name="product-detail"),
#     ******Articles urls*****
     path('article/', article_view.article_list_create_view, name="article-list-create"),
     path('article/<int:pk>/', article_view.article_update_view, name="article-update"),
     path('article/<int:pk>/delete', article_view.article_delete_view, name="article-delete"),
]