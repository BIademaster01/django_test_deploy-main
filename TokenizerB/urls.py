from django.urls import path
from .views import tokenize_text

urlpatterns = [
    path('tokenize/', tokenize_text, name='tokenize_text'),
]
