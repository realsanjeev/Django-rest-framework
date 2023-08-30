from rest_framework import generics
from books.models import Book
from books.serializers import BookSerializer

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
    
