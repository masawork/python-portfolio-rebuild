from django.shortcuts import render, get_object_or_404
from django.db import models
from django.http import JsonResponse
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogPost
from .serializers import BlogPostSerializer
from portfolio.models import Tag

# 顔認証ライブラリのインポート（オプショナル）
try:
    from .face_recognition_demo import process_camera_stream, validate_camera_url
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False


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
    # 顔認証のブログ記事かどうかを判定
    is_face_recognition_post = post.slug == 'face-recognition-system'
    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'is_face_recognition_post': is_face_recognition_post,
        'face_recognition_available': FACE_RECOGNITION_AVAILABLE
    })


@api_view(['POST'])
def face_recognition_demo(request):
    """
    顔認証デモ用のAPIエンドポイント
    """
    if not FACE_RECOGNITION_AVAILABLE:
        return Response({
            'success': False,
            'error': '顔認証ライブラリがインストールされていません。opencv-python、face-recognition、dlibが必要です。'
        }, status=503)
    
    camera_url = request.data.get('camera_url', '')
    
    if not camera_url:
        return Response({
            'success': False,
            'error': 'カメラURLが指定されていません'
        }, status=400)
    
    # URLの検証
    if not validate_camera_url(camera_url):
        return Response({
            'success': False,
            'error': '無効なカメラURLです。HTTP/HTTPS/RTSP URL、またはローカルカメラ番号（0-9）を指定してください。'
        }, status=400)
    
    # ローカルカメラの場合は数値に変換
    if camera_url.isdigit():
        camera_url = int(camera_url)
    
    # 顔認証処理
    result = process_camera_stream(camera_url)
    
    if result['success']:
        return Response(result)
    else:
        return Response(result, status=400)

