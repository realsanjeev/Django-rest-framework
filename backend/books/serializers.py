from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        field= ["id", "title", "desc", "price", "get_sale_price"]