"""
URL configuration for portfolio project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include('portfolio.urls')),
    path('api/', include('blog.urls')),
    path('api/', include('contact.urls')),
    path('api/', include('ml_demo.urls')),
    path('', include('portfolio.urls')),
    path('', include('blog.urls')),
    path('', include('ml_demo.urls')),
    path('', include('contact.urls')),
]

# API URL patterns
from portfolio.urls import api_urlpatterns as portfolio_api
from blog.urls import api_urlpatterns as blog_api
from contact.urls import api_urlpatterns as contact_api
from ml_demo.urls import api_urlpatterns as ml_api

urlpatterns += [
    path('api/', include(portfolio_api)),
    path('api/', include(blog_api)),
    path('api/', include(contact_api)),
    path('api/', include(ml_api)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

