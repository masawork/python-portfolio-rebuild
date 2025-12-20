from django.shortcuts import render, get_object_or_404
from django.db import models
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Tag
from .serializers import ProjectSerializer, TagSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_published=True)
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tags']
    search_fields = ['title', 'summary', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


def home(request):
    projects = Project.objects.filter(is_published=True)[:6]
    return render(request, 'portfolio/home.html', {'projects': projects})


def project_list(request):
    tag_slug = request.GET.get('tag')
    search_query = request.GET.get('q', '')
    
    projects = Project.objects.filter(is_published=True)
    
    if tag_slug:
        projects = projects.filter(tags__slug=tag_slug)
    
    if search_query:
        projects = projects.filter(
            models.Q(title__icontains=search_query) |
            models.Q(summary__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )
    
    tags = Tag.objects.all()
    return render(request, 'portfolio/project_list.html', {
        'projects': projects,
        'tags': tags,
        'current_tag': tag_slug,
        'search_query': search_query,
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, is_published=True)
    return render(request, 'portfolio/project_detail.html', {'project': project})

