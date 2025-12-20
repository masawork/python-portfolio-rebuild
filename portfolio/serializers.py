from rest_framework import serializers
from .models import Project, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tech_stack_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'summary', 'description',
            'tech_stack', 'tech_stack_list', 'github_url',
            'demo_url', 'image', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_tech_stack_list(self, obj):
        return obj.get_tech_stack_list()

