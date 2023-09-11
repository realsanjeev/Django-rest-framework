from rest_framework import generics

from articles.models import Article
from articles.serializer import ArticleSerializer

# Create your views here.
class ArticleCreateListAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.body:
            instance.body = instance.title

class ArticleDeleteAPIView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

class ArticleSearchListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Article.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results =qs.search(q, user=user)
        return results
    

article_list_create_view = ArticleCreateListAPIView.as_view()

article_update_view = ArticleUpdateAPIView.as_view()

article_delete_view = ArticleDeleteAPIView.as_view()

article_search_view = ArticleSearchListView.as_view()