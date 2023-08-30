from rest_framework import serializers
from api.serializers import UserPublicSerializer


from books.validations import validate_len
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    user_detail = UserPublicSerializer(read_only=True, source="user") 
    discount = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(
        validators=[validate_len]
    )
    
    class Meta:
        model = Book
        fields = ["user_detail", "id", "title", "desc", "price", "sales_price", "discount"]

    def get_discount(self, obj):
        if not hasattr(obj, "get_discount_price"):
            return None
        return obj.get_discount_price()
    
    def validate_title(self, value):
        request = self.context.get("request")
        user = request.user
        qs = Book.objects.filter(
            user=user, 
            title__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(f"{value} already exists")
        return value
    

