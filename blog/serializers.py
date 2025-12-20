from rest_framework import serializers
from .models import BlogPost
from portfolio.serializers import TagSerializer


class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    body_html = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'body_markdown',
            'body_html', 'summary', 'tags',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'slug']

    def get_body_html(self, obj):
        return obj.get_body_html()

