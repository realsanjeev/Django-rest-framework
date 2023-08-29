from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Book
        fields = ["pk", "title", "desc", "price", "sales_price", "discount"]

    def get_discount(self, obj):
        # check attribute in instance
        if not hasattr(obj, "get_discount_price"):
            return None
        # or check serializer is instance.
        # Same as above to check serializer instance
        # if not isinstance(obj, Book):
        #     return None
        return obj.get_discount_price()