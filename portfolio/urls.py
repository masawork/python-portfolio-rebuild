from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, home, project_list, project_detail

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', home, name='home'),
    path('projects/', project_list, name='project_list'),
    path('projects/<int:pk>/', project_detail, name='project_detail'),
]

api_urlpatterns = [
    path('', include(router.urls)),
]

