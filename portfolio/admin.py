from django.contrib import admin
from .models import Project, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_at']
    list_filter = ['is_published', 'tags', 'created_at']
    search_fields = ['title', 'summary', 'description']
    prepopulated_fields = {}
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at']

