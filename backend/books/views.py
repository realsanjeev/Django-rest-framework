from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from books.serializers import BookSerializer
from books.models import Book

class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # lookup_field = pk #pk