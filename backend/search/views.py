from rest_framework import generics, status
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer

from . import client

class SearchAlgoliaListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        public = request.GET.get('public')
        public = str(request.GET.get('public'))  != "0"
        # print("*"*10)
        # print("Public: ", public)
        # print("*"*10)
        query = request.GET.get('q')
        tags = request.GET.get('tags') or None
        if not query:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        results = client.perform_search(query,
                                        tags=tags,
                                        user=user,
                                        public=public)
        return Response(results)

class SearchListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get("q")
        results = Book.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results  = qs.search(q, user=user)
        return results
