from rest_framework import serializers
from rest_framework.reverse import reverse

from api.models import Product

class ProductSerializer(serializers.ModelSerializer):
    view_url = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.HyperlinkedIdentityField("product-edit", lookup_field="pk")
    # suppose you need owner field. But donot want to show in api response anything about owner
    owner = serializers.CharField(write_only=True)
    class Meta:
        model = Product
        fields = ["title", "content", "price", "view_url", "edit_url", "owner"]

    # since there is no owner in model itself. 
    # To save serializer data. REmove owner data.
    def create(self, validated_data):
        # it can be done in views itself
        owner = validated_data.pop("owner")
        print(f"owner: {owner} and new validated data: {validated_data}")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        owner = validated_data.pop("owner")
        return super().update(instance, validated_data)

    def get_view_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("product-detail", kwargs={'pk': obj.pk}, request=request)


