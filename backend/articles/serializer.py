from rest_framework import serializers

from articles.models import Article
class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True, source='user')
    view_url = serializers.HyperlinkedIdentityField(view_name="article-update", lookup_field="pk")
    class Meta:
        model = Article
        fields = [
            "author",
            "title",
            "body",
            "tags",
            "publish_date",
            "view_url",
        ]

    def get_endpoint(self, obj):
        pass