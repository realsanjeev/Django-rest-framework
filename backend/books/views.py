from rest_framework import status, generics

from books.serializers import BookSerializer
from books.models import Book
Book.objects.all().defer()
class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # lookup_field = 'pk' 

class BookCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        # serializer.save(user=request.request.user)
        title = serializer.validated_data.get("title")
        desc = serializer.validated_data.get("desc") or None
        if desc is None:
            desc = title
        # save the data with changes in desc
        serializer.save(desc=desc)

class BookDestroyerAPIView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateAPIView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer