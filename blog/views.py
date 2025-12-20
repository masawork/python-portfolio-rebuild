from django.shortcuts import render, get_object_or_404
from django.db import models
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogPost
from .serializers import BlogPostSerializer
from portfolio.models import Tag


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tags']
    search_fields = ['title', 'body_markdown', 'summary']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


def blog_list(request):
    tag_slug = request.GET.get('tag')
    search_query = request.GET.get('q', '')
    
    posts = BlogPost.objects.filter(is_published=True)
    
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    if search_query:
        posts = posts.filter(
            models.Q(title__icontains=search_query) |
            models.Q(body_markdown__icontains=search_query) |
            models.Q(summary__icontains=search_query)
        )
    
    tags = Tag.objects.all()
    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'tags': tags,
        'current_tag': tag_slug,
        'search_query': search_query,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'blog/blog_detail.html', {'post': post})

