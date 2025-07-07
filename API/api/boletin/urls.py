from django.urls import path
from .views import NewsletterListCreateAPIView, NewsletterDetailAPIView

urlpatterns = [
    path('newsletters/', NewsletterListCreateAPIView.as_view(), name='newsletter-list'),
    path('newsletters/<int:pk>/', NewsletterDetailAPIView.as_view(), name='newsletter-detail'),
]