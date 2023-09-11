from rest_framework import serializers
from rest_framework.reverse import reverse

from django.contrib.auth import get_user_model
from api.models import Product

User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source="username")
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            "name",
            "id"
        ]

class ProductSerializer(serializers.ModelSerializer):
    view_url = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.HyperlinkedIdentityField(view_name="product-edit", lookup_field="pk")
    owner = serializers.CharField(write_only=True)
    body = serializers.CharField(source="content")

    class Meta:
        model = Product
        fields = ["title",
                "body",
                "price",
                "view_url",
                "edit_url",
                "owner"]

    def create(self, validated_data):
        owner = validated_data.pop("owner")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        owner = validated_data.pop("owner")
        return super().update(instance, validated_data)

    def get_view_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("product-detail", kwargs={'pk': obj.pk}, request=request)
