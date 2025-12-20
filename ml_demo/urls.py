from django.urls import path
from .views import predict, ml_demo

urlpatterns = [
    path('ml-demo/', ml_demo, name='ml_demo'),
]

api_urlpatterns = [
    path('ml/predict/', predict, name='ml_predict'),
]

