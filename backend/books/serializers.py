from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Book
        fields = ["id", "title", "desc", "price", "sales_price", "discount"]

    def get_discount(self, obj):
        # check attribute in instance
        if not hasattr(self, "id"):
            return None
        # or check serializer is instance. 
        # Same as above to check serialixer instance
        if not isinstance(self, Book):
            return None
        return obj.get_discount_price()