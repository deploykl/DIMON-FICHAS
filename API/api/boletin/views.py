from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Newsletter
from .serializers import NewsletterSerializer
from django_filters.rest_framework import DjangoFilterBackend

class NewsletterListCreateAPIView(generics.ListCreateAPIView):
    queryset = Newsletter.objects.filter(is_published=True).select_related('autor')
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['autor__username']  # Filtrar por autor

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)  # Asigna el usuario autenticado

class NewsletterDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]