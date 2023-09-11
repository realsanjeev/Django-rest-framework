from rest_framework import generics

from django.shortcuts import render

from articles.models import Article
from articles.serializer import ArticleSerializer
# Create your views here.
class ArticleCreateListAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDeleteAPIView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

article_list_create_view = ArticleCreateListAPIView.as_view()

article_update_view = ArticleUpdateAPIView.as_view()

article_delete_view = ArticleDeleteAPIView.as_view()