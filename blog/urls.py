from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, blog_list, blog_detail, face_recognition_demo

router = DefaultRouter()
router.register(r'blog', BlogPostViewSet, basename='blogpost')

urlpatterns = [
    path('blog/', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
]

api_urlpatterns = [
    path('', include(router.urls)),
    path('face-recognition/demo/', face_recognition_demo, name='face_recognition_demo'),
]

