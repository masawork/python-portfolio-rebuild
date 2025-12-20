from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, contact_form

router = DefaultRouter()
router.register(r'contact', ContactMessageViewSet, basename='contact')

urlpatterns = [
    path('contact/', contact_form, name='contact'),
]

api_urlpatterns = [
    path('', include(router.urls)),
]

