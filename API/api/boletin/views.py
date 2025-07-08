from rest_framework import generics, permissions, viewsets
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Newsletter, NewsletterImage
from .serializers import NewsletterSerializer, NewsletterImageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class BoletinViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        newsletter = self.get_object()
        # Permitir múltiples imágenes en la misma solicitud
        images = request.FILES.getlist('imagenes')
        response_data = []
        
        for image in images:
            data = {'imagen': image}
            if 'es_portada' in request.data:
                data['es_portada'] = request.data['es_portada']
                
            image_serializer = NewsletterImageSerializer(
                data=data,
                context={'request': request}
            )
            
            if image_serializer.is_valid():
                image_serializer.save(newsletter=newsletter)
                response_data.append(image_serializer.data)
            else:
                return Response(image_serializer.errors, status=400)
                
        return Response(response_data, status=201)

    @action(detail=True, methods=['delete'], url_path='delete-image/(?P<image_pk>[^/.]+)')
    def delete_image(self, request, pk=None, image_pk=None):
        newsletter = self.get_object()
        try:
            image = newsletter.imagenes.get(pk=image_pk)
            image.delete()
            return Response(status=204)
        except NewsletterImage.DoesNotExist:
            return Response({'error': 'Imagen no encontrada'}, status=404)